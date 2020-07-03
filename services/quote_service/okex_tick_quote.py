# coding=utf-8
import os,sys
import time
from time import sleep
from datetime import datetime
import json
import requests
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 當前okex市場所有合約
__builtins__.cur_fu_instruments = []
__builtins__.cur_op_instruments = []




def fetch_all_instruments():
    __builtins__.cur_mkt_instruments = []
    headers = {'content-type': 'application/json'}    
    fu_req = "https://www.okex.com/api/futures/v3/instruments"
    response = requests.get(fu_req,headers=headers, timeout=100)
    if('200' in str(response)):
        jsonObj = json.loads(response.text)
        for ins in jsonObj: 
            if( 'BTC' in ins['underlying_index'] ):
                __builtins__.cur_fu_instruments.append( ins['instrument_id'] )
                print(ins['instrument_id'])
                
    op_req = "https://www.okex.com/api/option/v3/instruments/BTC-USD"
    response = requests.get(op_req,headers=headers, timeout=100)
    if('200' in str(response)):
        jsonObj = json.loads(response.text)
        for ins in jsonObj: 
            if( 'BTC' in ins['settlement_currency'] ):
                __builtins__.cur_op_instruments.append( ins['instrument_id'] )
                print(ins['instrument_id'])


# 呼叫
def fetch_tick():
    headers = {'content-type': 'application/json'}
    if(len(__builtins__.cur_fu_instruments)<1):
        fetch_all_instruments()
    for inst in __builtins__.cur_fu_instruments:
        getdepth_req = "https://www.okex.com/api/futures/v3/instruments/"+inst+"/ticker"
        response = requests.get(getdepth_req,headers=headers, timeout=100)
        if('200' in str(response)):
            jsonObj = json.loads(response.text)
            #cb_save_instr_market_data_mongo(jsonObj)
    
    
    for inst in __builtins__.cur_op_instruments:
        getdepth_req = "https://www.okex.com/api/option/v3/instruments/BTC-USD/summary/"+inst
        response = requests.get(getdepth_req,headers=headers, timeout=100)
        if('200' in str(response)):
            jsonObj = json.loads(response.text)
            #cb_save_instr_market_data_mongo(jsonObj)
    




if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    
    # 定時取得市場的所有標的
    scheduler.add_job(lambda:fetch_all_instruments(), 'interval', seconds=43200 , max_instances=100)
    
    # 定時取得市場的所有標的 orderbook
    scheduler.add_job(lambda:fetch_tick(), 'interval', seconds=600 , max_instances=1000) # 600 
    scheduler.start()
    try:
        print('Printing in the main thread.')
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

    
