#myAM 
import time
import copy
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'

from company import Company
from TradeAstock import Trade
from account import Account
from analysis.models import Share, StockMarket
from datetime import datetime, timezone

if __name__=="__main__":
    #Log in to Xing server
	myAcnt = Account()
	myTrade = Trade(myAcnt)
	myTrade.logIn('johan','dlskdud79')

	isStop=True
	timeSlice=2#monitor on 2 minutes
	onChour = 15 #time to close market(14 hour)
	# today=datetime.now(timezone.utc)
	today=datetime.now()
    
	while(isStop):
		tStamp = time.localtime()#change to time.time()version
		#시간 확인해 보기 제대로 끝나는 건지
		if tStamp.tm_hour*60+tStamp.tm_min >= onChour*60:#change to time.time()version
			print('hour/min', tStamp.tm_hour, tStamp.tm_min)
			isStop = False
			print("Stock trade market is closed")
		else :
			time.sleep(timeSlice * 60)
			print('start update')
			#stock market
			cospiInfo = myTrade.getStockMarketInfo('001')#get COSPI info
			cosdaqInfo = myTrade.getStockMarketInfo('301')#get COSPI info
			#market_type '1' : COSPI, '2' : COSDAQ

			StockMarket.objects.update_or_create(gubun='1', market_date__year=today.year,
					market_date__month=today.month, market_date__day=today.day,defaults=cospiInfo )

			StockMarket.objects.update_or_create(gubun='2', market_date__year=today.year,
					market_date__month=today.month, market_date__day=today.day,defaults=cosdaqInfo )


			shareList = Share.objects.all()
			for share in shareList:
				time.sleep(0.1)
				price = myTrade.getNowStockPrc(share.code)[0]
				share.now_price = price
				share.save()
