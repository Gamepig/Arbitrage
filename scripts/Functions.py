import mysql.connector
import json
from web3 import HTTPProvider, Web3

web3_polygon_rpc = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))
AaveOracleV3_address = web3_polygon_rpc.toChecksumAddress("0xb023e699F5a33916Ea823A16485e259257cA8Bd1")
with open("../scripts/AaveOracleV3ABI.json") as f:
    AaveOracleV3ABI = json.load(f)
    AaveOracleV3ABI = AaveOracleV3ABI['result']
AaveOracleV3_Contract = web3_polygon_rpc.eth.contract(address=AaveOracleV3_address, abi=AaveOracleV3ABI)

def TokenAddress(Token):
    return {
        'MATIC': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        'DAI': '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063',
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'WBTC': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
        'WETH': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
        'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
        'LINK': '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39',
        'UNI': '0xb33EaAd8d922B1083446DC23f610c2567fB5180f',
        'AAVE': '0xD6DF932A45C0f255f85145f286eA0b292B21C90B',
        'SUSHI': '0x0b3F868E0BE5597D5DB7fEB59E1CADBb0fdDa50a',
        'BAL': '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3',
        'DPI': '0x85955046DF4668e1DD369D2DE9f3AEB98DD2A369',
        'stMATIC': '0x3A58a54C066FdC0f2D55FC9C89F0415C92eBf3C4',
        'MaticX': '0xfa68FB4628DFF1028CFEc22b4162FCcd0d45efb6',
        'EURS': '0xE111178A87A3BFf0c8d18DECBa5798827539Ae99',
        'jEUR': '0x4e3Decbb3645551B8A19f0eA1678079FCB33fB4c',
        'agEUR': '0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4',
        'miMATIC': '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1'
    }.get(Token, 'error')
    
def ReservesList(Token):
    match Token:
        case '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063':
            return 'DAI',18
        case '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39':
            return 'LINK',18
        case '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174':
            return 'USDC',6
        case '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6':
            return 'WBTC',8
        case '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619':
            return 'WETH',18
        case '0xc2132D05D31c914a87C6611C10748AEb04B58e8F':
            return 'USDT',6
        case '0xD6DF932A45C0f255f85145f286eA0b292B21C90B':
            return 'AAVE',18
        case '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270':
            return 'WMATIC',18
        case '0x172370d5Cd63279eFa6d502DAB29171933a610AF':
            return 'CRV',18
        case '0x0b3F868E0BE5597D5DB7fEB59E1CADBb0fdDa50a':
            return 'SUSHI',18
        case '0x385Eeac5cB85A38A9a07A70c73e0a3271CfB54A7':
            return 'GHST',18
        case '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3':
            return 'BAL',18
        case '0x85955046DF4668e1DD369D2DE9f3AEB98DD2A369':
            return 'DPI',18
        case '0xE111178A87A3BFf0c8d18DECBa5798827539Ae99':
            return 'EURS',2
        case '0x4e3Decbb3645551B8A19f0eA1678079FCB33fB4c':
            return 'jEUR',18
        case '0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4':
            return 'agEUR',18
        case '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1':
            return 'miMATIC',18
        case '0x3A58a54C066FdC0f2D55FC9C89F0415C92eBf3C4':
            return 'stMATIC',18
        case '0xfa68FB4628DFF1028CFEc22b4162FCcd0d45efb6':
            return 'MaticX',18
        case '0x03b54A6e9a984069379fae1a4fC4dBAE93B3bCCD':
            return 'wstETH',18
        
def insertProfitRecord(pair,DEX,amount,profit,GAS,GasUSD,ReturnAmount,TokenPriceUSD,ReturnQuote):
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sqlstr = f"INSERT INTO arbfinder.ProfitRecord (pair,DEX,amount,profit,GAS,GasUSD,ReturnAmount,TokenPriceUSD,ReturnQuote) VALUES ('{pair}','{DEX}',{amount},{profit},{GAS},{GasUSD},{ReturnAmount},{TokenPriceUSD},{ReturnQuote})"
    db_cursor.execute(sqlstr)
    db_connection.commit()
    db_connection.close()
    
def getAssetsPricesAaveOracleV3(Tokens): #(變數使用Token Address)
    TokenList = {}
    Price = AaveOracleV3_Contract.functions.getAssetsPrices(Tokens).call()
    x = 0
    for Token in Tokens:
        TokenName = ReservesList(Token)
        TokenList[TokenName[0]] = Price[x]/10**8
        x += 1
    return TokenList

def getOraclePriceFeed(Token):
    ContractInfor = getOraclePriceFeedContractAddress(Token)
    ContractAddress = web3_polygon_rpc.toChecksumAddress(ContractInfor[0])
    decimals = ContractInfor[1]
    with open("../scripts/ChainlinkPriceOraclesABI.json") as f:
        ABI = json.load(f)
        ABI = ABI['result']
        8. 

    Contract = web3_polygon_rpc.eth.contract(address=ContractAddress, abi=ABI)
    Price = Contract.functions.latestAnswer().call()
    return Price

def getOraclePriceFeedContractAddress(Token):
    decimals = 8
    match Token:
        case 'DAI':
            return '0x4746DeC9e833A82EC7C2C1356372CcF2cfcD2F3D', decimals
        case 'LINK':
            return '0xd9FFdb71EbE7496cC440152d43986Aae0AB76665',decimals
        case 'USDC':
            return '0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7',decimals
        case 'WBTC':
            return '0xDE31F8bFBD8c84b5360CFACCa3539B938dd78ae6',decimals
        case 'WETH':
            return '0xF9680D99D6C9589e2a93a78A04A279e509205945',decimals
        case 'USDT':
            return '0x0A6513e40db6EB1b165753AD52E80663aeA50545',decimals
        case 'AAVE':
            return '0x72484B12719E23115761D5DA1646945632979bB6',decimals
        case 'WMATIC':
            return '0xAB594600376Ec9fD91F8e885dADF0CE036862dE0',decimals
        case 'CRV':
            return '0x336584C8E6Dc19637A5b36206B1c79923111b405',decimals
        case 'SUSHI':
            return '0x49B0c695039243BBfEb8EcD054EB70061fd54aa0',decimals
        case 'GHST':
            return '0xDD229Ce42f11D8Ee7fFf29bDB71C7b81352e11be',decimals
        case 'BAL':
            return '0xD106B538F2A868c28Ca1Ec7E298C3325E0251d66',decimals
        case 'agEUR':
            return '0x9b88d07B2354eF5f4579690356818e07371c7BeD',decimals
        case 'miMATIC':
            return '0xd8d483d813547CfB624b8Dc33a00F2fcbCd2D428',decimals
        case 'stMATIC':
            return '0x97371dF4492605486e23Da797fA68e55Fc38a13f',decimals
        case 'MaticX':
            return '0x5d37E4b374E6907de8Fc7fb33EE3b0af403C7403',decimals
        case 'DPI':
            return '0xC70aAF9092De3a4E5000956E672cDf5E996B4610',decimals
        case _:
            return 'error'