from discord_webhook import DiscordWebhook
import time as mytime
import json
import os
import time
import requests
#import redis 
import argparse
from datetime import datetime, time, timedelta
from decimal import *
#from web3.auto import Web3
#from web3.auto import w3



def run_query(query):
    request = requests.post('http://hasura.core.cloudchainsinc.com/v1/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



def print_line(string_data):
    # prints w/o new line
    print(string_data, end="\r", flush=True)
    return

parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='enable debug mode, no actual selling/buying will happen', action="store_true")
parser.add_argument('--token', help='token to trade on', default='LTC')
parser.add_argument('--time', help='token to trade on', default=86400)
args = parser.parse_args()

dxendtime = int(datetime.now().timestamp())
dxstarttime = dxendtime - (int(args.time))  # 24hours ago

print('time: {}'.format(dxstarttime))
newlistings = """
query MyQuery {
  uniswappair(limit: 100, order_by: {created_at: desc}) {
    address
    created_at
    tokenObj0 {
      name
      symbol
    }
    tokenObj1 {
      name
      symbol
    }
  }
}
"""
gq_tokenpairs = """
query MyQuery {
  uniswappair {
    tokenObj0 {
      address
      symbol
    }
    tokenObj1 {
      address
      symbol
    }
    token0
    token1
    address
    id
  }
}
"""



tokendict = {}
tokenpairs = run_query(gq_tokenpairs)
tokendata = tokenpairs['data']['uniswappair']

for x in tokendata:
    tcontract = x['address']
    t0symbol = x['tokenObj0']['symbol']
    t0contract = x['tokenObj0']['address']
    t1symbol = x['tokenObj1']['symbol']
    t1contract = x['tokenObj1']['address']
    if (t0symbol or t1symbol) == 'UNI-V2':
        continue
    else:
        tokendict[t0contract] = t0symbol
        tokendict[t1contract] = t1symbol
        tokendict[tcontract] = '{}:{}'.format(t0symbol,t1symbol)
        tokendict[x['id']] = '{}:{}'.format(t0symbol,t1symbol)


def cleanorder(orderamount, decimalsallowed):
    return '{0:.{1}f}'.format(float(orderamount), int(decimalsallowed))

def myFunc(e):
  return len(e)

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float(0)

#print(tokendict)
lastlist = []
trackerlist = []
tradecountdict = {}
#print(rq)
print('start')
rq = run_query(newlistings)

for z in rq['data']['uniswappair']:
    print(z['address'])
    print(z['tokenObj0'])
    print(z['tokenObj1'])
    address = z['address']
    token0 = z['tokenObj0']
    token1 = z['tokenObj1']
    dexURL = 'https://www.dextools.io/app/uniswap/pair-explorer/{}'.format(address)
    webhookurl = 'https://discord.com/api/webhooks/842886931117506561/PpqAGZGRPRFUQKDMxWQ1oCGEnWOUpBUy2fiZpr02DJX7ohVsACsE2SWufLLmMV91Hte2'
    message = '{} {} {} {}'.format(address, token0, token1, dexURL)
    webhook = DiscordWebhook(url=webhookurl, content=message)
    response = webhook.execute()
    

    break