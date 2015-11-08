from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from myAM_web.myAM.TradeAstock import Trade
from datetime import timedelta, timezone, datetime

from .models import Share
# Create your views here.
def main(request):
	context={}
	# 0. 세션 확인(로그인 여부 확인)
	isLogin =  request.session.get('am_id', False)
        	if isLogin is False:
        		return HttpResponseRedirect(reverse('home'))

	# 1. 디비에 접근하여서  최근일자(3일간)의 후보 주식들 갖고오기
	now = datetime.now(timezone.utc)
	srt = now-timedelta(days=3)
	shareList = Share.objects.filter(drv_date__range=(srt,now))
	
	# 2. 현재 및 어제 COSPI, COSDAQ 정보 가져오기
	# #COSPI: 001, COSDAQ: 301
	myTrade = request.session.get['myTrade',False]
	if myTrade is False:
		return HttpResponse("myTrade session is over")

	cospiInfo = myTrade.getStockMarketInfo('001')#COSPI
	cosdaqInfo = myTrade.getStockMarketInfo('031')#COSDAQ

	# 3. 위의 정보들을 context에 삽입후 main.html에 띄우기 
	context['shareList']=shareList
	context['cospi']=cosdaqInfo
	context['cosdaq']=cosdaqInfo

	return render(request, 'main.html',context)

def analysisShare(request, analysis_type):#analysis_type 0: R3I, 1: R10T, 2: BOX
	context={}
	return render(request, 'analysis.html', context)
