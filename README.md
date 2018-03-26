**draft**
```sh
py.test -n 4 -v .
docker-compose -f docker-compose.yml -f docker-compose.yml up -d
```


```sh
git clone ...
cd learning_telegram
virtualenv .venv && source .venv/bin/activate
pip install -r requirements.txt
export token="your token"
export FLASK_APP=main.py
export FLASK_DEBUG=1
# export $(cut -d= -f1 .mem_sqlite_ha_envs)
flask run --host=0.0.0.0 --port 8080 
```

> via google application engine
```sh
curl https://sdk.cloud.google.com | bash
gcloud init
mkdir lib
sed -i 's/"INSERT_TOKEN"/"your real token"/g' app.yaml
pip install -t lib -r requirements.txt
export token="<your token>"
export hook="/incoming"
export domain="https://<your_project_name>.appspot.com"
dev_appserver.py --env_var token=$token --host 127.0.0.1 .
gcloud app deploy app.yaml
curl -X POST -d '{"url":"https://$domain/$hook"}' -H "Content-Type: application/json" "https://api.telegram.org/bot$token/setWebhook"
```