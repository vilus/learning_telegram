# -*- coding: utf-8 -*-
import logging
import time
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, and_, orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, extract
from sqlalchemy.engine.url import URL


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
        # NOTE: sqlite does not support SELECT ... FOR UPDATE
        session.query(Lock).filter_by(name=name).with_for_update().one()
        session.add(counter)  # session.flush() ??
        res = session.query(Counter).filter(
            and_(
                extract('epoch', Counter.created_at) + Counter.ttl > extract('epoch', func.now()),
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


@contextmanager
def _incr_decr(name, ttl, _sessionmaker):
    num, c_id = _increase_counter(name, ttl, _sessionmaker)
    try:
        yield num
    finally:
        _decrease_counter(c_id, _sessionmaker)


def make_db_url(conf, prefix=''):
    db_url = conf.get('db_url')
    if db_url:
        return db_url

    params = dict()
    params['drivername'] = conf.get(prefix+'db_drivername')
    params['username'] = conf.get(prefix+'db_user')
    params['password'] = conf.get(prefix+'db_password')
    params['host'] = conf.get(prefix+'db_host')
    params['port'] = conf.get(prefix+'db_port')
    params['database'] = conf.get(prefix+'db_name')
    return str(URL(**params))


def get_tools(conf):
    """
    TODO: implement for GCP orm
    params in conf:
        - tools_orm_type: ['sqlalchemy', 'gcp']
        - db_url: for 'sqlalchemy'
        - xxx: for 'gcp' - not implemented yet
    """
    db_url = make_db_url(conf)
    logging.debug('creating db engine with db_url: {0}'.format(db_url))
    engine = create_engine(db_url, echo=conf.get('db_echo', False))
    session_maker = sessionmaker(bind=engine)

    if not engine.dialect.has_table(engine, Counter.__tablename__):
        Base.metadata.create_all(engine)
    # temporary solution
    tools = type('', (object,), {})()

    tools.increase_counter = lambda name, ttl, _sessionmaker=session_maker: \
        _increase_counter(name, ttl, _sessionmaker)

    tools.decrease_counter = lambda counter_id, _sessionmaker=session_maker: \
        _decrease_counter(counter_id, _sessionmaker)

    tools.is_allowed_service = lambda service_name, rate, _sessionmaker=session_maker: \
        _is_allowed_service(service_name, rate, _sessionmaker)

    tools.incr_decr = lambda name, ttl, _sessionmaker=session_maker: \
        _incr_decr(name, ttl, _sessionmaker)

    tools.wait = wait

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
            extract('epoch', func.now()) - extract('epoch', Limiter.last_usage)
        ).filter_by(name=service_name).with_for_update().first()

        if duration*rate >= 1:
            limit.last_usage = func.now()
            session.add(limit)
            return True
    return False
