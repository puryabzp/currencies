from __future__ import absolute_import, unicode_literals
from celery import Celery
import requests


"""This module Provides A simple celery app that get All currencies And return a Customize dictionary for each currency
   For Run app
   First Install Dependenices
   Then, run celery beat :
        celery -A app beat
   Finally:
        celery -A app worker -l INFO     
"""



app = Celery('app')

class Config:
    """Configs Of Celery App
       
       Attributes: 
       Broker_url (str) : Use Redis for Broker
       result_serializer (str) : Accepted json on result
       accept_content (list) : Only Json accepted for result
       enable_utc (boolean) : If we want to use UTC then we must Set True For this 
       timezone (str) : For set timezone
       beat_schedule (dict) : for scheduling of tasks
    
    """
    broker_url = 'redis://localhost:6379/'   
    result_backend = 'redis://localhost:6379/'
    result_serializer = 'json'
    accept_content = ['json']
    enable_utc = True
    timezone = 'Asia/Tehran'
    beat_schedule = {
        'collector': {
            'task': 'app.collector',
            'schedule': 50.0,
            'relative': True

        }
    }
app.config_from_object(Config)  # read config from celeryconfig.py module

api = 'http://api.coincap.io/v2/assets'
api_key = 'da914918-5ed5-4be9-aad3-4df4263b5c8b'
params = {'KEY':api_key}



@app.task
def collector():

    """a task that get all currencies from api that defined and return a result as a result that we want"""

    result = requests.get(api,params=params)
    currencies = result.json()['data']
    return [{"name":i['id'],"symbol":i['symbol'],
        "circulatingSupply":i["supply"],"maxSupply":i["maxSupply"],
        "totalSupply":i["maxSupply"],"volume":i["volumeUsd24Hr"],
        "rank":i["rank"],"marketCap":i["marketCapUsd"],"price":i["priceUsd"]} for i in currencies]  

