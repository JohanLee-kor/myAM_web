from TradeAstock import Trade
from account import Account
from company import Company
import time
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'
from analysis.models import Share # code to TEST DB

if __name__=="__main__":
    myAcnt = Account()
    myTrade = Trade(myAcnt)
    myTrade.logIn('johan','dlskdud79')
    # myTrade.getMyStockAcntInfo()

    shareList = myTrade.get3CandidateShareList()
    BOX_list=shareList[0]
    R3I_list=shareList[1]
    R10T_list=shareList[2]

    for share in BOX_list:
        Share.objects.get_or_create(analysis_type='BOX', code=share.stockCode, defaults={'init_price':share.initPrice, 'name': share.stockName})

    for share in R3I_list:
        Share.objects.get_or_create(analysis_type='R3I', code=share.stockCode, defaults={'init_price':share.initPrice, 'name': share.stockName})

    for share in R10T_list:
        Share.objects.get_or_create(analysis_type='R10T', code=share.stockCode, defaults={'init_price':share.initPrice, 'name': share.stockName})
        # try:
        #     s = Share.objects.get(analysis_type='R10T', code=share.stockCode)
        # except Share.DoesNotExist:
        #     s = Share(analysis_type='R10T', name=share.stockName, code=share.stockCode, init_price=share.initPrice)
        #     s.save()
