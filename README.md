# Google Translation API client

## How to setup

1 Enable the [Translations API](https://translation.googleapis.com/language/translate/v2)

2 Grant `roles/serviceusage.serviceUsageConsumer` to a "quota" project for the users.

3 Setup virtualenv
```
virtualenv venv
venv/bin/pip install -r requirements.txt
```


## How to use

```
gcloud auth application-default login
venv/bin/python gtr.py
```
