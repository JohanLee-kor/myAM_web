class Account:
    def __init__(self, ordAbleAmt = 0, outAbleAmt = 0, orgAmt = 0):
        self.mnyOrdAbleAmt = ordAbleAmt #현금주문가능금액
        self.mnyoutAbleAmt = outAbleAmt #출금가능금액
        self.investOrgAmt = orgAmt  #투자원금
    def updateInfoBySell(self, price, units):
        print("calculate attributes ")
        realSellPrc = int(price*0.99685)
        realSellAmt = realSellPrc * units
        self.mnyOrdAbleAmt += realSellAmt
        self.mnyoutAbleAmt = self.mnyOrdAbleAmt
        
    def updateInfoByBuy(self, price, units):
        print("calculate attributes ")
        realBuyPrc = int(price*1.00015)
        realBuyAmt = realBuyPrc * units
        self.mnyOrdAbleAmt -= realBuyAmt
        self.mnyoutAbleAmt = self.mnyOrdAbleAmt

    def updateInfo(self, price = 0, units = 0, trTp = 1):# 0 : 매도(sell), 1: 매수(buy)
        if trTp == 1: #buy
            self.updateInfoByBuy(price, units)
        elif trTp == 0: #sell
            self.updateInfoBySell(price, units)
