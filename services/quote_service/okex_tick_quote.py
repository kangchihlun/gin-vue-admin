# coding=utf-8
import os,sys
import time
from time import sleep
from datetime import datetime
import json
import requests
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import grpc

import quote_pb2
import quote_pb2_grpc
#from logger import getJSONLogger
#logger = getJSONLogger('okex-quote-client')

from opencensus.trace.tracer import Tracer
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace.ext.grpc import client_interceptor


# 當前okex市場所有合約
__builtins__.cur_fu_instruments = []
__builtins__.cur_op_instruments = []

hostPort = 'localhost:50051'
try:
    exporter = stackdriver_exporter.StackdriverExporter()
    tracer = Tracer(exporter=exporter)
    tracer_interceptor = client_interceptor.OpenCensusClientInterceptor(tracer, host_port=hostPort)
except:
    tracer_interceptor = client_interceptor.OpenCensusClientInterceptor()

# 存合約市場深度
def cb_save_instr_market_data(jsonObj):
    channel = grpc.insecure_channel(hostPort)
    channel = grpc.intercept_channel(channel, tracer_interceptor)
    stub = quote_pb2_grpc.QuoteServiceStub(channel)
    try:
        response = stub.OnNotifyTicks(quote_pb2.Tick(
            symbol = jsonObj['instrument_id'],
            timestamp = str(jsonObj['timestamp']),
            best_bid_price = str(jsonObj['best_bid']),
            best_bid_amount = str(jsonObj['best_bid_size']),
            best_ask_price = str(jsonObj['best_ask']),
            best_ask_amount = str(jsonObj['best_ask_size'])
        ))
        #logger.info('Request sent.')
    except grpc.RpcError as err:
        #logger.error(err.details())
        #logger.error('{}, {}'.format(err.code().name, err.code().value))
        print(err)


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
            cb_save_instr_market_data(jsonObj)

    
    for inst in __builtins__.cur_op_instruments:
        getdepth_req = "https://www.okex.com/api/option/v3/instruments/BTC-USD/summary/"+inst
        response = requests.get(getdepth_req,headers=headers, timeout=100)
        if('200' in str(response)):
            jsonObj = json.loads(response.text)
            cb_save_instr_market_data(jsonObj)
    




if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    
    # 定時取得市場的所有標的
    scheduler.add_job(lambda:fetch_all_instruments(), 'interval', seconds=1 , max_instances=100)
    
    # 定時取得市場的所有標的 orderbook
    scheduler.add_job(lambda:fetch_tick(), 'interval', seconds=1 , max_instances=1000) # 600 
    scheduler.start()
    try:
        print('Printing in the main thread.')
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

    
