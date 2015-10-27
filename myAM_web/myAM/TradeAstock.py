import win32com.client
#import yjauthentication
import pythoncom
import Log
import time
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'
#from analysis.models import Share # code to TEST DB
from analysis.models import AMuser

from XASessionEventClass import XASessionEvents
from XAQueryEventClass import XAQueryEvents
from company import Company
from account import Account
import common.xingINFO as xing


#Trade class invokes Xing API
class Trade:
    def __init__(self, account):
        self.myStockList = {}
        self.stockFirstTrDateDict = {}
        self.myStockAcnt = account
        #self.inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        
    def logIn(self, u_id, u_pass):
        #It makes an authentification by Xing API

        self.user=AMuser.objects.get(am_id = u_id,am_pass= u_pass)

        inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        inXASession.ConnectServer(xing.server_addr, xing.server_port)
        inXASession.Login(self.user.xing_id, self.user.xing_pass, self.user.xing_certificate_pass, xing.server_type, 0)

        while XASessionEvents.logInState == 0:
            pythoncom.PumpWaitingMessages()
            
        print("Log in Success")
        
    def buy(self,myCompany, buy_qty):
        #It makes Xing API buy some stocks a specific of company
        
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res")
        
        #real buy codes
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_number)
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_pw)

        #practice buy code
        #inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_prac_number)
        #inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_prac_pw)

        #isuNo = myCompany.stockCode
        #if 'A' not in isuNo :
        #    isuNo='A'+isuNo
        
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, myCompany.stockCode)# real
        #inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, isuNo)#practice
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, buy_qty) #buy_qty만큼
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, 0)#지정가일 경우 가격을, 시장가일 경우 0을 입력
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, '2')#매도 1 매수 2
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdprcPtnCode', 0, '03')#지정가 00, 시장가 03, 조건부지정가 05, 최유리지정가 06, 최우선지정가 07, 장개시전시간외 61, 시간외종가 81, 시간외단일가 82
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'MgntrnCode', 0, '000')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'LoanDt', 0, '0')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdCndiTpCode', 0, '0')
        
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

            
        #under codes to remember that this is first trade
        if XAQueryEvents.querySuccess  is 40: #under '0' means TR error
            Log.mkLog("TradeAstock","%s  %s  %s units bought"%(myCompany.stockName, myCompany.stockCode, buy_qty))
            if myCompany.stockCode not in self.stockFirstTrDateDict: #This stock trade is first trade
                self.stockFirstTrDateDict[myCompany.stockCode]=int(time.time())
                Log.mkLog("TradeAstock", "%s %s first buy tr"%(myCompany.stockName, myCompany.stockCode))
            else:
                Log.mkLog("TradeAstock", "%s %s already buy tr"%(myCompany.stockName, myCompany.stockCode))
        else:
            Log.mkLog("TradeAstock", "buy TR is failed")

        return XAQueryEvents.querySuccess
        
    def sell(self, myCompany, sell_qty):
        #It makes Xing API sell some stocks a specific of company
        
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res")
        
        #real buy codes
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_number)
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_pw)
        
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, myCompany.stockCode)
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, sell_qty) #잔고 수량 전부
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, 0)#지정가일 경우 가격을, 시장가일 경우 0을 입력
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, '1')#매도 1 매수 2
        #지정가 00, 시장가 03, 조건부지정가 05, 최유리지정가 06, 최우선지정가 07, 장개시전시간외 61, 시간외종가 81, 시간외단일가 82
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdprcPtnCode', 0, '03')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'MgntrnCode', 0, '000')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'LoanDt', 0, '0')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdCndiTpCode', 0, '0')
        
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        #under codes to remember that this is first trade
        if XAQueryEvents.querySuccess is 39: #Not 39 is error
            if myCompany.stockCode in self.stockFirstTrDateDict: #This stock trade is over
                print("sell %s:  %s success"%(myCompany.stockName, sell_qty))
                Log.mkLog("TradeAstock","sell %s:  %s success"%(myCompany.stockName, sell_qty))
        else:
            print("sell all : TR is failed")
            Log.mkLog("TradeAstock", "TR is failed")
        return XAQueryEvents.querySuccess

    def sellAll(self, myCompany):
        #It makes Xing API sell some stocks a specific of company
        
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res")
        
        #real buy codes
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_number)
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_pw)

        #practice buy code
        #inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_prac_number)
        #inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_prac_pw)

        # isuNo = myCompany.stockCode
        # if 'A' not in isuNo :
        #     isuNo='A'+isuNo
        
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, myCompany.stockCode)
        # inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, isuNo)#practice
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, myCompany.bnsBaseBalQty) #잔고 수량 전부
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, 0)#지정가일 경우 가격을, 시장가일 경우 0을 입력
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, '1')#매도 1 매수 2
        #지정가 00, 시장가 03, 조건부지정가 05, 최유리지정가 06, 최우선지정가 07, 장개시전시간외 61, 시간외종가 81, 시간외단일가 82
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdprcPtnCode', 0, '03')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'MgntrnCode', 0, '000')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'LoanDt', 0, '0')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdCndiTpCode', 0, '0')
        
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        #under codes to remember that this is first trade
        if XAQueryEvents.querySuccess is 39: #Not 39 is error
            if myCompany.stockCode in self.stockFirstTrDateDict: #This stock trade is over
                del self.stockFirstTrDateDict[myCompany.stockCode]
            else:
                print("해당 부분이 호출 되면 기능에 문제가 있음: stockFirstTrDateDict update가 제대로 안되는 것")
        else:
            print("sell all : TR is failed")
        return XAQueryEvents.querySuccess


    def sellAllPrc(self, myCompany, price):
        #It makes Xing API sell some stocks a specific of company
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res")
        
        #real buy codes
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, self.user.account_number)
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, self.user.account_pw)
        
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, myCompany.stockCode)
        # inXAQuery.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, isuNo)#practice
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, myCompany.bnsBaseBalQty) #잔고 수량 전부
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, price)#지정가일 경우 가격을, 시장가일 경우 0을 입력
        inXAQuery.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, '1')#매도 1 매수 2
        #지정가 00, 시장가 03, 조건부지정가 05, 최유리지정가 06, 최우선지정가 07, 장개시전시간외 61, 시간외종가 81, 시간외단일가 82
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdprcPtnCode', 0, '00')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'MgntrnCode', 0, '000')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'LoanDt', 0, '0')
        inXAQuery.SetFieldData('CSPAT00600InBlock1', 'OrdCndiTpCode', 0, '0')
        
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        #under codes to remember that this is first trade
        if XAQueryEvents.querySuccess is 39: #Not 39 is error
            if myCompany.stockCode in self.stockFirstTrDateDict: #This stock trade is over
                del self.stockFirstTrDateDict[myCompany.stockCode]
            else:
                print("해당 부분이 호출 되면 기능에 문제가 있음: stockFirstTrDateDict update가 제대로 안되는 것")
        else:
            print("sell all : TR is failed")
        return XAQueryEvents.querySuccess



    def getStockFirstTrDateDict(self):
        #최초거래일자 파일로 부터 stockFirstTrDateDict 설정하는 함수 stockFirstTrDateDict를 반환 한다
        try:
            f = open("StockTrDate.jh", 'r')
            lines=f.readlines()

            for line in lines:
                tokens = line.split() #tokens[0] : code,     tokens[1] : chekedDate, tokens[2] :  alive
                code = tokens[0]
                chkedDate = int(tokens[1])
                self.stockFirstTrDateDict[code] = chkedDate          
            
            f.close()
        except IOError:
            print("There is no file")

        return self.stockFirstTrDateDict



#특정 주식의 최초거래 일자를 파일형식으로 저장하기 위한 함수
    def setStockFirstTrDateDict(self):
        try:
            f = open("StockTrDate.jh",'w')
            for tr in self.stockFirstTrDateDict.items():
                row="%s\t%s\n"%(tr[0],tr[1])
                f.write(row)

            f.close()

        except IOError:
            print("There is no file")

            
#Xing API CSPAQ12300 으로 부터 내가 보유한 주식 정보 그리고 CSPAQ12200 으로 자산 정보를 가져온다.
    def getMyStockAcntInfo(self):
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ12300.res")
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'RecCnt', 0, 1)
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'AcntNo', 0, self.user.account_number)
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'Pwd', 0, self.user.account_pw)
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'BalCreTp', 0, 0) #0: 전체, 1: 현물, 9: 선물대용
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'CmsnAppTpCode', 0, 1)#0: 수수료 미적용, 1: 수수료 적용
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'D2balBaseQryTp', 0, 1)#0: 전부조회, 1: 잔고 0 이상만 조회
        inXAQuery.SetFieldData('CSPAQ12300InBlock1', 'UprcTpCode', 0, 0)#0: 평균단가, 1: BEP단가
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        nCount = inXAQuery.GetBlockCount('CSPAQ12300OutBlock3')
        #내가 소유한 주식 정보 얻기
        for i in range(nCount):
            code = inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'IsuNo', i)
            name = inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'IsuNm', i)
            balqty = int(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'BalQty', i))
            bnsbasebalqty = int(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'BnsBaseBalQty', i))
            sellpnlamt = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'SellPnlAmt', i))
            pnlrat = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'PnlRat', i)) * 100
            avgprc = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'AvrUprc', i))
            sellableqty = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'SellAbleQty', i))
            balevalamt = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'BalEvalAmt', i))
            evalpnl = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'EvalPnl', i))
            ordableamt = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'OrdAbleAmt', i))
            prdayprice = float(inXAQuery.GetFieldData('CSPAQ12300OutBlock3', 'PrdayCprc', i))
        
            c=Company()
            
            c.stockCode = code[1:] #주식번호
            c.stockName = name #주식회사 이름
            c.balQty = balqty #잔고수량
            c.bnsBaseBalQty = bnsbasebalqty #매매기준 잔고 수량
            c.sellPnlAmt = sellpnlamt#매도손익금액
            c.pnlRat = pnlrat #손익률
            c.avgPrice = avgprc #평균단가
            c.sellAbleQty = sellableqty #매도가능수량
            c.balEvalAmt = balevalamt#잔고평가금액
            c.evalPnl = evalpnl#평가손익
            c.ordAbleAmt = ordableamt#주문가능금액
            c.prdayPrice = prdayprice#전일가
            
            self.myStockList[c.stockCode] = c


        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ12200.res")
        inXAQuery.SetFieldData('CSPAQ12200InBlock1', 'RecCnt', 0, 1)
        inXAQuery.SetFieldData('CSPAQ12200InBlock1', 'AcntNo', 0, self.user.account_number)
        inXAQuery.SetFieldData('CSPAQ12200InBlock1', 'Pwd', 0, self.user.account_pw)
        inXAQuery.SetFieldData('CSPAQ12200InBlock1', 'BalCreTp', 0, 0) #0: 전체, 1: 현물, 9: 선물대용
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        #나의 자산 정보 갖고 오기
        #self.myStockAcnt.mnyOrdAbleAmt = float(inXAQuery.GetFieldData('CSPAQ12200OutBlock2', 'MgnRat100pctOrdAbleAmt', 0))
        self.myStockAcnt.mnyOrdAbleAmt = float(inXAQuery.GetFieldData('CSPAQ12200OutBlock2', 'D2Dps', 0))
        self.myStockAcnt.mnyoutAbleAmt = float(inXAQuery.GetFieldData('CSPAQ12200OutBlock2', 'MnyoutAbleAmt', 0))
        self.myStockAcnt.investOrgAmt = float(inXAQuery.GetFieldData('CSPAQ12200OutBlock2', 'InvstOrgAmt', 0))

        print("set myStockList variable")

    def getNowStockPrc(self, code):
        print("get a stock price on now time")
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1102.res")
        inXAQuery.SetFieldData('t1102InBlock', 'shcode', 0, code)

        inXAQuery.Request(False)
        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get FieldData
        price = float(inXAQuery.GetFieldData('t1102OutBlock', 'price', 0))
        openp = float(inXAQuery.GetFieldData('t1102OutBlock', 'open', 0))
        dvo = float(inXAQuery.GetFieldData('t1102OutBlock', 'dvol1', 0))
        svo = float(inXAQuery.GetFieldData('t1102OutBlock', 'svol1', 0))
        cgdgree = 0
        if dvo != 0:
            cgdgree= svo / dvo * 100#체결강도
       

        return (price, cgdgree)

    def getCandidateStocks(self, nCandidates):
        print("request candidate stocks from Xing")
        #--------------------------------------------------------------------
        # Get some stocks which have a specific scope of price(10000~20000)
        #--------------------------------------------------------------------
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
        inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 2)#to get stock companies at cosdaq
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get Stock list
        stockList = []
        nCount = inXAQuery.GetBlockCount('t8430OutBlock')
        print("All count of cosdaq company ",nCount)
        for i in range(nCount):     
            jnilclose = float(inXAQuery.GetFieldData('t8430OutBlock', 'jnilclose', i))
            if jnilclose <= 20000 and jnilclose >= 10000 :
                name = inXAQuery.GetFieldData('t8430OutBlock', 'hname', i)
                shcode = inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i)

                c=Company()
                c.stockCode = shcode #주식번호
                c.stockName = name #주식회사 이름
                
                stockList.append(c)
                del c

        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which is going up during 5 days.
        #--------------------------------------------------------------------
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1305.res")
        newStockList=[]
        upLmtdiff = 10.0
        nIndex = 0
        daysKeepGup = '10'#to get stock info duing this days variable
        dwmcode = '1'# day: 1, week: 2, month: 3

        print("number of stock to estimate: ", len(stockList))
        for stock in stockList:
            time.sleep(1)
            inXAQuery.SetFieldData('t1305InBlock', 'shcode',0,stock.stockCode)
            inXAQuery.SetFieldData('t1305InBlock', 'dwmcode',0,dwmcode)
            inXAQuery.SetFieldData('t1305InBlock', 'cnt',0,daysKeepGup)#to get stock info duing 5 days
            inXAQuery.Request(False)

            while XAQueryEvents.queryState == 0:
                pythoncom.PumpWaitingMessages()

            XAQueryEvents.queryState = 0

            nCount = inXAQuery.GetBlockCount('t1305OutBlock1')
            
            diff = 0.0
            pre_openPrc=-1
            pre_closePrc=-1
            flg = True

            if nCount is not int(daysKeepGup):
                continue

            for i in reversed(range(nCount)):
                diff += float(inXAQuery.GetFieldData('t1305OutBlock1', 'diff', i))
                openPrc = float(inXAQuery.GetFieldData('t1305OutBlock1', 'open', i))
                closePrc = float(inXAQuery.GetFieldData('t1305OutBlock1', 'close', i))

                if i <= 5 : 
                    if pre_openPrc == -1 :#This is first loop
                        pre_openPrc = openPrc
                        pre_closePrc = closePrc
                        continue
                    else:
                        if openPrc > pre_openPrc and closePrc > pre_closePrc :
                            pre_openPrc = openPrc
                            pre_closePrc = closePrc
                            continue
                        else:
                            flg = False

            if flg or diff > upLmtdiff:
                print("nCount: ", nCount)
                newStockList.append(stock)
                Log.mkLog("TradeAstock:getCandidateStocks","name: %s, code: %s, diff: %s"%(stock.stockName, stock.stockCode, diff))

        del stockList

        #--------------------------------------------------------------------
        #codes to order candidates list (not yet, 2015-07-25)
        #--------------------------------------------------------------------

        
        print("length of candidates : ", len(newStockList))
        candidates = newStockList[:nCandidates]
        candidatesDict={}

        for stock in candidates: #make list to dict
            candidatesDict[stock.stockCode]=stock
        
        return candidatesDict

    def getCandidateStocks2(self, nCandidates):

        Log.mkLog("TradeAstock:getCandidateStocks2","Get candidate stocks from Xing API")
        #--------------------------------------------------------------------
        # Get some stocks which have a specific scope of price(10000~20000)
        #--------------------------------------------------------------------
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
        inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 2)#to get stock companies at cosdaq
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get Stock list
        stockList = []
        nCount = inXAQuery.GetBlockCount('t8430OutBlock')
        print("All count of cosdaq company ",nCount)
        for i in range(nCount):     
            jnilclose = float(inXAQuery.GetFieldData('t8430OutBlock', 'jnilclose', i))
            if jnilclose <= 20000 and jnilclose >= 10000 :
                name = inXAQuery.GetFieldData('t8430OutBlock', 'hname', i)
                shcode = inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i)

                c=Company()
                c.stockCode = shcode #주식번호
                c.stockName = name #주식회사 이름
                
                stockList.append(c)
                del c

        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which is going up during 10 days.
        #--------------------------------------------------------------------
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1305.res")
        newStockList=[]
        upLmtdiff = 10.0
        nIndex = 0
        daysKeepGup = '10'#to get stock info duing this days variable
        dwmcode = '1'# day: 1, week: 2, month: 3

        print("number of stock to estimate: ", len(stockList))
        for stock in stockList:
            time.sleep(1)
            inXAQuery.SetFieldData('t1305InBlock', 'shcode',0,stock.stockCode)
            inXAQuery.SetFieldData('t1305InBlock', 'dwmcode',0,dwmcode)
            inXAQuery.SetFieldData('t1305InBlock', 'cnt',0,daysKeepGup)#to get stock info duing 'daysKeepGup' days
            inXAQuery.Request(False)

            while XAQueryEvents.queryState == 0:
                pythoncom.PumpWaitingMessages()

            XAQueryEvents.queryState = 0

            nCount = inXAQuery.GetBlockCount('t1305OutBlock1')
            
            if nCount is not int(daysKeepGup):
                continue

            total_diff = 0.0

            for i in reversed(range(nCount)):
                diff = float(inXAQuery.GetFieldData('t1305OutBlock1', 'diff', i))

                if (i is 1 and diff <= 0) or diff < -20 or diff > 20 : #If down growth is break on the day before or diff value is bigger than 20 or smaller than -20
                    total_diff = -1
                    break
                total_diff += diff

            if total_diff > upLmtdiff:
                newStockList.append(stock)
                Log.mkLog("TradeAstock:getCandidateStocks","name: %s, code: %s, total_diff: %s"%(stock.stockName, stock.stockCode, total_diff))

        del stockList

        #--------------------------------------------------------------------
        #codes to order candidates list (not yet, 2015-07-25)
        #--------------------------------------------------------------------

        
        print("length of candidates : ", len(newStockList))
        candidates = newStockList[:nCandidates]
        candidatesDict={}

        for stock in candidates: #make list to dict
            candidatesDict[stock.stockCode]=stock
        
        return candidatesDict

    def getCandidateStocks3(self, nCandidates):#R3I Algorithm

        Log.mkLog("TradeAstock:getCandidateStocks3","Get candidate stocks from Xing API")
        #--------------------------------------------------------------------
        # Get some stocks which have a specific scope of price(10000~20000)
        #--------------------------------------------------------------------
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
        inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 2)#to get stock companies at cosdaq
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get Stock list
        stockList = []
        nCount = inXAQuery.GetBlockCount('t8430OutBlock')
        print("All count of cosdaq company ",nCount)
        for i in range(nCount):     
            jnilclose = float(inXAQuery.GetFieldData('t8430OutBlock', 'jnilclose', i))
            # if jnilclose <= 20000 and jnilclose >= 10000 :#get all of cosdaq stock company
            if jnilclose <= 10000 :
                name = inXAQuery.GetFieldData('t8430OutBlock', 'hname', i)
                shcode = inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i)

                c=Company()
                c.stockCode = shcode #주식번호
                c.stockName = name #주식회사 이름
                
                stockList.append(c)
                del c

        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which is going up 3days and figure out high price for one month
        #--------------------------------------------------------------------
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1305.res")
        newStockList=[]
        nIndex = 0
        days = '30'#to get stock info duing this days variable
        gap = 3
        dwmcode = '1'# day: 1, week: 2, month: 3

        print("number of stock to estimate: ", len(stockList))
        totstkList = len(stockList)
        for stock in stockList:
            time.sleep(6)
            curstk = stockList.index(stock)+1
            print("%s / %s======percent: %s"%(curstk, totstkList , int(curstk/totstkList * 100)))
            inXAQuery.SetFieldData('t1305InBlock', 'shcode',0,stock.stockCode)
            inXAQuery.SetFieldData('t1305InBlock', 'dwmcode',0,dwmcode)
            inXAQuery.SetFieldData('t1305InBlock', 'cnt',0,days)#to get stock info duing 'days' days
            inXAQuery.Request(False)

            while XAQueryEvents.queryState == 0:
                pythoncom.PumpWaitingMessages()

            XAQueryEvents.queryState = 0

            nCount = inXAQuery.GetBlockCount('t1305OutBlock1')
            
            if nCount is not int(days):
                continue

            total_diff = 0.0
            price_month=[]
            flag = True

            for i in reversed(range(nCount)):
                price_month.append(int(inXAQuery.GetFieldData('t1305OutBlock1', 'close',i)))

            stdPrice_month = int(max(price_month)*0.8)

            for i in reversed(range(gap)):
                price = int(inXAQuery.GetFieldData('t1305OutBlock1', 'close',i))
                diff = float(inXAQuery.GetFieldData('t1305OutBlock1', 'diff', i))
                total_diff +=diff
                if price <= stdPrice_month and diff > 0 and diff <= 10:
                    pass
                else:
                    flag = False

            if flag:
                newStockList.append(stock)
                Log.mkLog("TradeAstock:getCandidateStocks","name: %s, code: %s, total_diff: %s"%(stock.stockName, stock.stockCode, total_diff))

        del stockList

        #--------------------------------------------------------------------
        #codes to order candidates list (not yet, 2015-07-25)
        #--------------------------------------------------------------------

        
        print("length of candidates : ", len(newStockList))
        candidates = newStockList[:nCandidates]
        candidatesDict={}

        for stock in candidates: #make list to dict
            candidatesDict[stock.stockCode]=stock
        
        return candidatesDict

    def getCandiStkInBox(self, nCandidates):
        Log.mkLog("TradeAstock:getCandiStkInBox","Get candidate stocks in box from Xing API")
        #--------------------------------------------------------------------
        # Get some stocks which have a specific scope of price(10000~20000)
        #--------------------------------------------------------------------
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
        inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 2)#to get stock companies at cosdaq
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get Stock list
        stockList = []
        nCount = inXAQuery.GetBlockCount('t8430OutBlock')
        print("All count of cosdaq company ",nCount)
        for i in range(nCount):     
            jnilclose = float(inXAQuery.GetFieldData('t8430OutBlock', 'jnilclose', i))
            
            name = inXAQuery.GetFieldData('t8430OutBlock', 'hname', i)
            shcode = inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i)

            c=Company()
            c.stockCode = shcode #주식번호
            c.stockName = name #주식회사 이름
                
            stockList.append(c)
            del c

        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which was going up and down in specific price scope
        #--------------------------------------------------------------------
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1305.res")
        newStockList=[]
        days = '10'#to get stock info duing this days variable
        dwmcode = '1'# day: 1, week: 2, month: 3

        print("number of stock to estimate: ", len(stockList))
        totstkList = len(stockList)
        for stock in stockList:
            time.sleep(6)
            curstk = stockList.index(stock)+1
            print("%s / %s======percent: %s"%(curstk, totstkList , int(curstk/totstkList * 100)))
            inXAQuery.SetFieldData('t1305InBlock', 'shcode',0,stock.stockCode)
            inXAQuery.SetFieldData('t1305InBlock', 'dwmcode',0,dwmcode)
            inXAQuery.SetFieldData('t1305InBlock', 'cnt',0,days)#to get stock info duing 'days' days
            inXAQuery.Request(False)

            while XAQueryEvents.queryState == 0:
                pythoncom.PumpWaitingMessages()

            XAQueryEvents.queryState = 0

            nCount = inXAQuery.GetBlockCount('t1305OutBlock1')
            
            #If 'nCount' is smaller than days, pass this 'stock'
            if nCount is not int(days):
                continue

            flag = True
            low_mean = 0
            high_mean = 0

            for i in reversed(range(nCount)):
                low = int(inXAQuery.GetFieldData('t1305OutBlock1', 'low',i))
                high = int(inXAQuery.GetFieldData('t1305OutBlock1', 'high',i))
                low_mean +=low
                high_mean+=high

                box_gap = high-low
                print("value of box_gap:  ",box_gap)
                
                if box_gap <=1500 and box_gap >=1000:
                    continue
                else:
                    flag = False
                    break

            if flag:
                low_mean /= 10
                high_mean /=  10
                newStockList.append(stock)
                Log.mkLog("getCandiStkInBox","name: %s, code: %s, low_mean: %s, high_mean: %s"%(stock.stockName, stock.stockCode, low_mean, high_mean))

        del stockList

        #--------------------------------------------------------------------
        #codes to order candidates list (not yet, 2015-07-25)
        #--------------------------------------------------------------------

        
        print("length of candidates : ", len(newStockList))
        candidates = newStockList[:nCandidates]
        candidatesDict={}

        for stock in candidates: #make list to dict
            candidatesDict[stock.stockCode]=stock
        
        return candidatesDict

    def  isBoxShare(self, XAQuery):
        nCount = XAQuery.GetBlockCount('t1305OutBlock1')
            
            #If 'nCount' is smaller than days, pass this 'stock'
        if nCount < 10 :
            return False

        flag = True
        low_mean = 0
        high_mean = 0

        for i in range(10):
            low = int(XAQuery.GetFieldData('t1305OutBlock1', 'low',i))
            high = int(XAQuery.GetFieldData('t1305OutBlock1', 'high',i))
            low_mean +=low
            high_mean+=high

            box_gap = high-low
            print("value of box_gap:  ",box_gap)
                
            if box_gap <=1500 and box_gap >=1000:
                continue
            else:
                flag = False
                break

            return flag

    def isR10TShare(self, XAQuery):
        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which is going up during 10 days.
        #--------------------------------------------------------------------
        nCount = XAQuery.GetBlockCount('t1305OutBlock1')
        upLmtdiff = 10.0
            
        if nCount < 10:
            return False

        total_diff = 0.0

        for i in range(10):
            diff = float(XAQuery.GetFieldData('t1305OutBlock1', 'diff', i))
            if (i is 1 and diff <= 0) or diff < -20 or diff > 13#20 : #If down growth is break on the day before or diff value is bigger than 20 or smaller than -20
                total_diff = -1
                break
            total_diff += diff

        if total_diff > upLmtdiff:
            return True
        else:
            return False

    def isR3IShare(self, XAQuery):
        #--------------------------------------------------------------------
        # Distinguish stocks to buy stocks which is going up 3days and figure out high price for one month
        #--------------------------------------------------------------------
        nCount = XAQuery.GetBlockCount('t1305OutBlock1')
            
        if nCount is not 30:
            return False

        total_diff = 0.0
        gap = 3
        price_month=[]
        flag = True

        for i in reversed(range(nCount)):
            price_month.append(int(XAQuery.GetFieldData('t1305OutBlock1', 'close',i)))

        stdPrice_month = int(max(price_month)*0.8)

        for i in reversed(range(gap)):
            price = int(XAQuery.GetFieldData('t1305OutBlock1', 'close',i))
            diff = float(XAQuery.GetFieldData('t1305OutBlock1', 'diff', i))
            total_diff +=diff
            if price <= stdPrice_month and diff > 0 and diff <= 10:
                pass
            else:
                flag = False

        return flag

    def get3CandidateShareList(self):
        ''''This method is used to get three kinds of candidate share.
            First is BOX Algorithm, second is R3I Algorithm, third is R10T Algorithm '''
        #--------------------------------------------------------------------
        # Get some stocks which have a specific scope of price(10000~20000)
        #--------------------------------------------------------------------
        inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
        inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 0)#0 get all, 1 COSPI, 2 COSDAQ
        inXAQuery.Request(False)

        while XAQueryEvents.queryState == 0:
            pythoncom.PumpWaitingMessages()

        XAQueryEvents.queryState = 0

        # Get Stock list
        stockList = []
        nCount = inXAQuery.GetBlockCount('t8430OutBlock')
        print("All count of company ",nCount)
        for i in range(nCount):     
            jnilclose = float(inXAQuery.GetFieldData('t8430OutBlock', 'jnilclose', i))
            # if jnilclose <= 20000 and jnilclose >= 10000 :#get all of cosdaq stock company
            # if jnilclose <= 10000 :
            name = inXAQuery.GetFieldData('t8430OutBlock', 'hname', i)
            shcode = inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i)
            recprice = int(inXAQuery.GetFieldData('t8430OutBlock', 'recprice', i))

            c=Company()
            c.stockCode = shcode #주식번호
            c.stockName = name #주식회사 이름
            c.initPrice = recprice#기준가
                
            stockList.append(c)
            del c

        inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1305.res")
        BOX_list=[]
        R3I_list=[]
        R10T_list[]
        days = '30'#to get stock info duing this days variable
        dwmcode = '1'# day: 1, week: 2, month: 3

        print("number of stock to estimate: ", len(stockList))
        totstkList = len(stockList)
        for stock in stockList:
            time.sleep(6)
            curstk = stockList.index(stock)+1
            print("%s / %s======percent: %s"%(curstk, totstkList , int(curstk/totstkList * 100)))
            inXAQuery.SetFieldData('t1305InBlock', 'shcode',0,stock.stockCode)
            inXAQuery.SetFieldData('t1305InBlock', 'dwmcode',0,dwmcode)
            inXAQuery.SetFieldData('t1305InBlock', 'cnt',0,days)#to get stock info duing 'days' days
            inXAQuery.Request(False)

            while XAQueryEvents.queryState == 0:
                pythoncom.PumpWaitingMessages()

            XAQueryEvents.queryState = 0

            if self.isBoxShare(inXAQuery):
                BOX_list.append(stock)

            if self.isR3IShare(inXAQuery):
                R3I_list.append(stock)

            if self.isR10TShare(inXAQuery):
                R10T_list.append(stock)

        return (BOX_list, R3I_list, R10T_list)
