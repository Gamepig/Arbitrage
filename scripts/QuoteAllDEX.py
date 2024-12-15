from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
import os
import time
from time import sleep
from colorama import Fore, Back, Style
import sys
import json
import decimal
from eth_abi.packed import encode_single_packed
import threading
from threading import Lock
from icecream import ic
from eth_abi.packed import encode_single_packed
from web3.middleware import geth_poa_middleware
from Functions import TokenAddress,ReservesList,insertProfitRecord

web3 = Web3(HTTPProvider('https://rpc.ankr.com/polygon/3056719186807a83c61564283e4bdaec7300a35ff09d2a24dc5696c1186597b3', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://api.zan.top/node/v1/polygon/mainnet/ee55242d0cba4d5a84f2c8cad8645e19',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 240}))
# web3 = Web3(HTTPProvider('http://127.0.0.1:8545/',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.infura.io/v3/cf6843bb016c459baa45b51e564f2c95',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-bor.publicnode.com', request_kwargs={'timeout': 180}))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

Profitable = 0

try:
    if(web3.isConnected() == False):
        print(Fore.RED + 'Network Not connected' + Style.RESET_ALL)
        sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    else:
        print('Network connected')
except Exception as e :
    sleep(5)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

Uniswap_Quoter = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
QuickSwap_Router = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
wmatic = web3.toChecksumAddress('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
weth = web3.toChecksumAddress('0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619')

with open("Uniswap_QuoterABI.json") as f:
    info_json = json.load(f)
Uniswap_QuoterABI = info_json["result"]

with open("Quickswap_QuoterABI.json") as f:
    info_json = json.load(f)
Quickswap_QuoterABI = info_json["result"]

Uniswap_Quotercontract_address = web3.toChecksumAddress(Uniswap_Quoter)
Uniswap_QuoterContract = web3.eth.contract(address=Uniswap_Quotercontract_address, abi=Uniswap_QuoterABI)

QuickRoutercontract_address = web3.toChecksumAddress(QuickSwap_Router)
QuickRouterContract = web3.eth.contract(address=QuickRoutercontract_address, abi=Quickswap_QuoterABI)

AaveOracleV3_address = web3.toChecksumAddress("0xb023e699F5a33916Ea823A16485e259257cA8Bd1")
with open("../scripts/AaveOracleV3ABI.json") as f:
    AaveOracleV3ABI = json.load(f)
    AaveOracleV3ABI = AaveOracleV3ABI['result']
AaveOracleV3_Contract = web3.eth.contract(address=AaveOracleV3_address, abi=AaveOracleV3ABI)

def StartSwap(Token_in, Token_out, amount, DEX, gasPriceCount, eventid):
    pass

def QuoteAllDEX(amount, tokenin, tokenout):
    try:
        path = encode_single_packed("(address,uint24,address)", [tokenin, 500, tokenout])
        quote1 = Uniswap_QuoterContract.functions.quoteExactInput(path, amount).call()
        Quote4 = QuickRouterContract.functions.getAmountsOut(amount, [tokenin, tokenout]).call()

        allprice = {"Uni": quote1, "Quick": Quote4[1]}
        allprice = sorted(allprice.items(), key=lambda kv: kv[1])
        return allprice
    except Exception as e:
        print("QuoteAllDEX")
        print(e)
        # sleep(10)
        os.execv(sys.executable, ['python'] + [sys.argv[0]])
        
def AllSwap(amount,Token_in,Token_out,start_time):
    
    token_in = ReservesList(Token_in)
    token_out = ReservesList(Token_out)
    wmatic = TokenAddress('WMATIC')

    if(token_in[0] == 'USDC' or token_in[0] == 'USDT'):
        Amount = int(amount*1e6)
    elif(token_in[0] == 'WETH'):
        if(amount==10000):
            amount = 10
        elif(amount==25000):
            amount = 25
        elif(amount==50000):
            amount = 50
        elif(amount==100000):
            amount = 100
        elif(amount==250000):
            amount = 250
        Amount = int(amount*1e8)
    else:
        Amount = int(amount*1e18)
        
    quote1 = QuoteAllDEX(Amount, Token_in, Token_out)
    Q1Len = len(quote1) - 1
    quote2 = QuoteAllDEX(quote1[Q1Len][1], Token_out, Token_in)
    t = time.time()
    t1 = time.localtime(t)
    end_time = time.strftime('%Y/%m/%d %H:%M:%S',t1)
    Q2Len = len(quote2) - 1
    ReturnQuote = (quote2[Q2Len][1]) - int(Amount)
    
    if(ReturnQuote>0):   
        if(token_in[0] == 'USDC' or token_in[0] == 'USDT'):
            Amount = int(Amount/1e6)
            ReturnAmount = (ReturnQuote/1e6)
        elif(token_in[0] == 'WETH'):
            Amount = int(Amount/1e8)
            ReturnAmount = (ReturnQuote/1e8)
        else:
            Amount = int(Amount/1e18)
            ReturnAmount = (ReturnQuote/1e18)
        
    # ic(quote1[Q1Len][1],quote2[Q2Len][1],TokenPriceUSD,Amount,pair,dex,ReturnQuote,int(Amount),ReturnAmount,ReturnAmountInPriceUSD,start_time,end_time)
    # print('-------------------------------------------------')
        Tokens = web3.toChecksumAddress(Token_in),web3.toChecksumAddress(wmatic)
        TokenPriceUSDArr = AaveOracleV3_Contract.functions.getAssetsPrices(Tokens).call()
        TokenPriceUSD = TokenPriceUSDArr[0]/1e8
        wmaticPriceUSD = TokenPriceUSDArr[1]/1e8
        pair = f"{token_in[0]}/{token_out[0]}"
        dex = f"{quote1[Q1Len][0]}/{quote2[Q2Len][0]}"
        ReturnAmountInPriceUSD = (ReturnAmount * TokenPriceUSD)
        GasLimit = (1500000)
        gasPrice = web3.fromWei(web3.eth.gas_price,'gwei')
        max_priority_fee = web3.fromWei(web3.eth.max_priority_fee,'gwei')
        GasPrice = int((float(gasPrice + max_priority_fee) * GasLimit) * 1.1)
        GasPrice = web3.fromWei(GasPrice,'gwei')
        GasFeeUSD = round(float(GasPrice)*wmaticPriceUSD, 4)
        ic(ReturnAmount * TokenPriceUSD)
        profit = float(ReturnAmountInPriceUSD) - GasFeeUSD
        ic(profit)
        if(profit>10):
            global Profitable
            Profitable += 1
            insertProfitRecord(pair,dex,Amount,profit,GasPrice,GasFeeUSD,ReturnAmount,TokenPriceUSD,ReturnQuote)

# Amounts = {100000,50000,25000,10000,5000}
Amounts = {25000,10000,5000}
TokenIn = {'USDC'}
TokensOut = {'WMATIC','WETH','WBTC','LINK','DAI','UNI','AAVE'}
# TokensOut = {'WMATIC', 'USDC', 'USDT','WETH','WBTC','LINK','DAI','UNI','AAVE','SUSHI','BAL'}
QList = []
for Token_in in TokenIn:
        for Token_out in TokensOut:
            if(Token_in != Token_out):
                for amount in Amounts:
                    token_in = web3.toChecksumAddress(TokenAddress(Token_in))
                    token_out = web3.toChecksumAddress(TokenAddress(Token_out))
                    QListStr = {"amount":amount,"Token_in":token_in,"Token_out":token_out}
                    QList.append(QListStr)
                    
# sys.exit()
while(True):
    threads = []
    RequestCount = 0
    time_1 = time.time()
    for QListStr in QList:
        t = time.time()
        t1 = time.localtime(t)
        start_time = time.strftime('%Y/%m/%d %H:%M:%S',t1)

        Price_Quote_AllSwap = threading.Thread(target=AllSwap, args=(int(QListStr['amount']), QListStr['Token_in'], QListStr['Token_out'], start_time))
        threads.append(Price_Quote_AllSwap)
        Price_Quote_AllSwap.start()
        
        RequestCount+=1
        print('Request Send:',(RequestCount), end='\r')
        sleep(0.2)

    for t in threads:
        t.join()
    time_2 = time.time()
    TimeUsed = round(time_2 - time_1,2)
    t = time.time()
    t1 = time.localtime(t)
    Finish_Time = time.strftime('%m/%d %H:%M:%S',t1)
    ic(TimeUsed,Profitable,len(threads),Finish_Time)
    print('****************************')
    sleep(4)
        # print(f"{ReservesList(QListStr['Token_in'])}/{ReservesList(QListStr['Token_out'])}   {QListStr['amount']}    {quote}  {t2}")
