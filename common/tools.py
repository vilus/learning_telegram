# -*- coding: utf-8 -*-
import time
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, and_, orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


@contextmanager
def session_scope(_Session):
    """Provide a transactional scope around a series of operations."""
    session = _Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create(session, model, **kwargs):
    """return tuple (instance, is_created)"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


Base = declarative_base()


class Counter(Base):
    __tablename__ = 'counter'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    ttl = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, name, ttl):
        self.name = name
        self.ttl = ttl  # through ass :(, but no need to sync time


class Lock(Base):
    __tablename__ = 'lock'
    name = Column(String(64), primary_key=True)

    def __init__(self, name):
        self.name = name


def _increase_counter(name, ttl, _sessionmaker):
    # TODO: create context manager for usage increase - decrease
    with session_scope(_sessionmaker) as session:
        try:
            _, _ = get_or_create(session, Lock, name=name)
        except exc.IntegrityError:
            session.rollback()

        counter = Counter(name, ttl)
        session.query(Lock).filter_by(name=name).with_for_update().one()
        session.add(counter)  # session.flush() ??
        # TODO: need to get rid of converting "datetime" -> "unixepoch" -> "datetime"
        res = session.query(Counter).filter(
            and_(
                func.datetime(func.strftime('%s', Counter.created_at) + Counter.ttl, 'unixepoch') >
                func.datetime(func.strftime('%s', 'now'), 'unixepoch'),
                Counter.name == name
            )
        ).count()
        session.commit()
        c_id = counter.id
        return res, c_id


def _decrease_counter(counter_id, _sessionmaker):
    with session_scope(_sessionmaker) as session:
        try:
            counter = session.query(Counter).filter_by(id=counter_id).one()
            session.delete(counter)
        except orm.exc.NoResultFound:
            pass


def get_tools(conf):
    engine = create_engine(conf['db_url'], echo=conf.get('db_echo', False))
    session_maker = sessionmaker(bind=engine)

    if not engine.dialect.has_table(engine, Counter.__tablename__):
        Base.metadata.create_all(engine)
    # temporary solution
    tools = type('', (object,), {})()
    setattr(tools, 'increase_counter',
            lambda name, ttl, _sessionmaker=session_maker: _increase_counter(name, ttl, _sessionmaker))
    setattr(tools, 'decrease_counter',
            lambda counter_id, _sessionmaker=session_maker: _decrease_counter(counter_id, _sessionmaker))
    setattr(tools, 'is_allowed_service',
            lambda service_name, rate, _sessionmaker=session_maker: _is_allowed_service(service_name,
                                                                                        rate,
                                                                                        _sessionmaker))
    setattr(tools, 'wait', wait)

    return tools


def wait(fn, timeout, check_interval=1):
    """
    waiting until `fn` will return "non empty" result
    :param check_interval: seconds
    :param timeout: seconds
    """
    end_time = time.time() + timeout
    while end_time >= time.time():
        res = fn()
        if res:
            return res
        time.sleep(check_interval)


class Limiter(Base):
    __tablename__ = 'limiter'
    name = Column(String, primary_key=True)
    last_usage = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, name):
        self.name = name


def _is_allowed_service(service_name, rate,  _sessionmaker):
    """
    ala "limiter service" whit no more 1 request per second (separately for each service)
    if need more than 1 request per sec then need implement like 'Token Bucket'
    or store microseconds (also nice to have implementation on redis for performance)
    rate - request per second, example rate 0.0166 ~ 1 request per 60 sec
    """
    assert rate <= 1
    with session_scope(_sessionmaker) as session:
        try:
            _, is_created = get_or_create(session, Limiter, name=service_name)
            if is_created:
                return True
        except exc.IntegrityError:
            session.rollback()
        # may be need to move query to model
        limit, duration = session.query(Limiter).add_columns(
            func.strftime('%s', func.now()) - func.strftime('%s', Limiter.last_usage)
        ).filter_by(name=service_name).with_for_update().first()

        if duration*rate >= 1:
            limit.last_usage = func.now()
            session.add(limit)
            return True
    return False
