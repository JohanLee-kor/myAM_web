from TradeAstock import Trade
from account import Account
from company import Company
import time

import copy
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'

from analysis.models import Share, StockMarket
from datetime import datetime, timezone

if __name__=="__main__":
    myAcnt = Account()
    myTrade = Trade(myAcnt)
    myTrade.logIn('YJP_AM','qkrdPwl!eoqkr@')
    # myTrade.getMyStockAcntInfo()
    # print("my orderable money: %s"%(myAcnt.mnyOrdAbleAmt))
    cospiInfo = myTrade.getStockMarketInfo('001')
    print(cospiInfo['hname'])
    print(cospiInfo['gubun'])
    cospiInfo['hname']='johan'

    # myTrade.logOut()

    # myTrade.logIn('YJP_AM','qkrdPwl!eoqkr@')
    # s=StockMarket(gubun='0')#1: cospi, 2: cosdaq

    today=datetime.now(timezone.utc)

    StockMarket.objects.update_or_create(gubun='1', market_date__year=today.year,
                    market_date__month=today.month, market_date__day=today.day,defaults=cospiInfo )
    # myAcnt.updateInfo(10000, 100, 1)
    # print("my orderable money: %s"%(myAcnt.mnyOrdAbleAmt))

    #myAsset=0
    #myRsset=0
    #for corp in myTrade.myStockList.values():
    #    stockPrcFstn=myTrade.getNowStockPrc(corp.stockCode)
    #    evalAmt=stockPrcFstn[0]*corp.bnsBaseBalQty
    #    orgAmt=corp.avgPrice*corp.bnsBaseBalQty
    #    myAsset+=evalAmt
    #    myRsset+=orgAmt
    #    print("%s, 현재가: %s 코드번호: %s, 평가금액: %s 손익률 :%s\n"%(corp.stockName, stockPrcFstn[0], corp.stockCode, evalAmt,corp.pnlRat))
    #    time.sleep(1)

    #print('=================================================\n')
    #print("my asset from only stock:",myAsset,myRsset,myAsset-myRsset)
    #print("stock result amt: ",myAsset+myAcnt.mnyOrdAbleAmt)

    #print('=================================================\n')

    # nCandidates = 35 - len(myTrade.myStockList)
    # print("nCandidates: ", nCandidates)
    # if nCandidates > 0:
    #     candidates = myTrade.getCandidateStocks(nCandidates)
    #     for code in candidates.keys():
    #         if code not in myTrade.myStockList.keys():
    #             myTrade.myStockList[code]=candidates[code]


    # for corp in myTrade.myStockList.values():
    #     corp.printInfo()
    #     print("\n")

    # for corp in myTrade.myStockList.values():
    #     corp.printInfo()
    #     myTrade.buy(corp, 10)
    #     print("\n")
    #     time.sleep(2)

    
    # fstTrDict = myTrade.getStockFirstTrDateDict()
    # print(str(fstTrDict))
    # fstTrDict['111545']=1238387347
    # myTrade.setStockFirstTrDateDict()

    # myCorp = Company()
    # myCorp.stockCode='1111111'
    # myCorp.stockName='myCorporation'
    # myCorp.updateInfo(10000, 10, 1)
    # myCorp.printInfo()
    # myCorp.updateInfoByPrc(12000)
    # myCorp.printInfo()
    # myCorp.updateInfo(12000, 5, 0)
    # myCorp.printInfo()
    # myCorp.updateInfo(14000, 5, 0)
    # myCorp.printInfo()


    # candistocks = myTrade.getCandidateStocks3(1000)
    # print("len of candistocks : ", len(candistocks))
    # for stock in candistocks.values():
    #     stock.printInfo()
    #     print("\n")
    
    

    
    
