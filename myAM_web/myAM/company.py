class Company:
    def __init__(self):
        self.stockCode = "" #주식번호
        self.stockName = "" #주식회사 이름
        self.balQty = 0.0 #잔고수량->안 쓸듯
        self.bnsBaseBalQty = 0#매매기준 잔고 수량!!
        self.sellPnlAmt = 0.0#매도손익금액
        self.pnlRat = 0.0 #손익률
        self.avgPrice = 0.0 #평균단가
        self.sellAbleQty = 0.0 #매도가능수량
        self.balEvalAmt = 0.0#잔고평가금액
        self.evalPnl = 0.0#평가손익
        self.ordAbleAmt = 0.0#주문가능금액
        self.prdayPrice = 0.0#전일가
        #self.chkedDate = ""#모니터링 시작한(cheked)날짜

    def updateInfo(self, price = 0, units = 0, trTp = 1):# 0 : 매도(sell), 1: 매수(buy)
        print("calculate some values to estimate a stock")

        if trTp == 1:#buy
            #평균단가
            self.avgPrice = int((self.bnsBaseBalQty*self.avgPrice+units*price)/(self.bnsBaseBalQty+units))
            #잔고수량
            self.bnsBaseBalQty +=units
        elif trTp == 0 : #sell
            if self.bnsBaseBalQty < units:
                return
            #평균단가 변화 없음 
            #잔고수량
            self.bnsBaseBalQty -=units
            
        #매도손익금액
        self.sellPnlAmt = price*self.bnsBaseBalQty - self.avgPrice*self.bnsBaseBalQty

        realSellPrc = int(price*0.99685)
        realBuyPrc = int(self.avgPrice*1.00015)

        #수수료 적용 손익률
        if realBuyPrc > 0:
            self.pnlRat = ((realSellPrc-realBuyPrc)/float(realBuyPrc)) * 100
        #매도가능수량
        self.sellAbleQty = self.bnsBaseBalQty
        #잔고평가금액
        self.balEvalAmt = int(self.bnsBaseBalQty * realSellPrc)
        #평가손익
        self.evalPnl = (realSellPrc-realBuyPrc)*self.bnsBaseBalQty
        print("update Info")

    def updateInfoByPrc(self, price):
        #평균단가 변화 없음 
        #잔고수량 변화 없음
        #매도손익금액
        self.sellPnlAmt = price*self.bnsBaseBalQty - self.avgPrice*self.bnsBaseBalQty

        realSellPrc = int(price*0.99685)
        realBuyPrc = int(self.avgPrice*1.00015)

        #수수료 적용 손익률
        if realBuyPrc > 0 :
            self.pnlRat = ((realSellPrc-realBuyPrc)/float(realBuyPrc)) * 100
        #매도가능수량 변화 없음
        #잔고평가금액
        self.balEvalAmt = int(self.bnsBaseBalQty * realSellPrc)
        #평가손익
        self.evalPnl = (realSellPrc-realBuyPrc)*self.bnsBaseBalQty
        print("update info by price")

    def getDiffRat(self):
        return self.pnlRat
    
    def printInfo(self):
        print("주식번호 : ",self.stockCode)
        print("주식회사 이름 : ",self.stockName)
        print("매매기준 잔고수량 : ",self.bnsBaseBalQty)
        print("매도손익금액 : ",self.sellPnlAmt)
        print("손익률 : ",self.pnlRat)
        print("평균단가 : ",self.avgPrice)
        print("매도가능수량 : ",self.sellAbleQty)
        print("잔고평가금액 : ",self.balEvalAmt)
        print("평가손익 : ",self.evalPnl)
        print("주문가능금액 : ",self.ordAbleAmt)
        print("전일가 : ",self.prdayPrice)
