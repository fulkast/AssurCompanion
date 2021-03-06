from wit import Wit
import json
from dateutil import parser
from datetime import timedelta

# ACCESSTOKEN = 'I2XMHO2GC4SYR4GYO4ZG7732JXIG34XF'
ACCESSTOKEN = '7X3RSRT3YKSWE3CMTMGFD2WOY4E7CRYO'

class MessageParser():
    def __init__(self):
        self.client = Wit(access_token= ACCESSTOKEN)

    def extract_datetime_range(self,message):
        resp = self.client.message(message)
        isnegative  = False
        if "negative" in resp['entities']:
            isnegative = True
        resp = resp['entities']['datetime'][0]
        # resp['timezone']='UTC+01'
        if resp['type'] == 'interval':
            if "from" in resp and "to" not in resp:
                datefrom = parser.parse(resp['from']['value'])
                return datefrom ,self.infer_missingtime(datefrom,resp["from"]["grain"],1),isnegative
            elif "to" in resp and "from" not in resp:
                dateto = parser.parse(resp['to']['value'])

                return self.infer_missingtime(dateto,resp["to"]["grain"],-1), dateto,isnegative
            else:
                datefrom = parser.parse(resp['from']['value'])
                dateto = parser.parse(resp['to']['value'])
                return datefrom,dateto,isnegative

        else:
            datefrom = parser.parse(resp['value'])
            dateto = self.infer_missingtime(datefrom,resp['grain'],1)
            return datefrom,dateto,isnegative

    def infer_missingtime(self,datetime,grain,d):
        if grain == 'hour' or grain == 'minute':
            if d == 1:
                dateto = datetime.replace(hour = 23,minute = 59)
            else:
                dateto = datetime.replace(hour = 0)
        elif grain == 'day':
            dateto = datetime +timedelta(days=1*d)
        elif grain == 'week':
            dateto = datetime +timedelta(days=2*d)
        elif grain == 'month':
            dateto = datetime +timedelta(days=7*d)
        else:
            dateto = datetime +timedelta(hours=1*d)
        return dateto

    def extract_intent(self,message):
        resp = self.client.message(message)
        resp = resp['entities']
        if "export" in resp:
            return "export"
        elif "start" in resp:
            return "start"
        elif "end" in resp:
            return "end"
        elif "datetime" in resp:
            return "times"
        elif "faul_occured" in resp:
            return "shit_happens"
        else:
            return "None"






