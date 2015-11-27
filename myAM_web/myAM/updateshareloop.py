#myAM 
import time
import copy
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'

from company import Company
from TradeAstock import Trade
from account import Account
from analysis.models import Share 

if __name__=="__main__":
    #Log in to Xing server
	myAcnt = Account()
	myTrade = Trade(myAcnt)
	myTrade.logIn('YJP_AM','qkrdPwl!eoqkr@')

	isStop=True
	timeSlice=2#monitor on 10 minutes
	onChour = 15 #time to close market(14 hour)
    
	while(isStop):
		tStamp = time.localtime()#change to time.time()version
		if tStamp.tm_hour*60+tStamp.tm_min >= onChour*60:#change to time.time()version
			isStop = False
			print("Stock trade market is closed")
		else :
			time.sleep(timeSlice * 60)
			shareList = Share.objects.all()
			for share in shareList:
				time.sleep(0.1)
				price = myTrade.getNowStockPrc(share.code)[0]
				share.now_price = price
				share.save()
				