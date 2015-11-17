from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from myAM_web.myAM.TradeAstock import Trade
from myAM_web.myAM.account import Account
from datetime import timedelta, timezone, datetime

from .models import Share, AMuser
import pythoncom
import time
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
	# myTrade = request.session.get['myTrade',False]
	myAcnt = Account()
	pythoncom.CoInitialize()
	myTrade = Trade(myAcnt)
	if myTrade is False:
		return HttpResponse("myTrade session is over")

	m = AMuser.objects.get(am_id=request.session['am_id'])

	myTrade.logIn(m.am_id,m.am_pass)
	cospiInfo = myTrade.getStockMarketInfo('001')#COSPI
	cosdaqInfo = myTrade.getStockMarketInfo('301')#COSDAQ
	myTrade.logOut()
	del myTrade

	# 3. 위의 정보들을 context에 삽입후 main.html에 띄우기 
	context['shareList']=shareList
	context['cospi']=cospiInfo
	context['cosdaq']=cosdaqInfo

	return render(request, 'main.html',context)

def analysisShare(request, analysisType):#analysis_type 0: R3I, 1: R10T, 2: BOX
	context={}
	#0. 세션 확인(로그인 여부 확인)
	isLogin =  request.session.get('am_id', False)
	if isLogin is False:
		return HttpResponseRedirect(reverse('home'))

	#1. DB 에 접근하여  analysis_type 에 따른 share 가져오기
	shareList = Share.objects.filter(analysis_type=analysisType)

	#2. 유추 할수 있는 데이터(최초 도출 일로 부터 얼마나 지났는지, 최초  price 와 얼마나 차이가 나는지) 계산
	priceDict={}
	# daysDict={}
	m = AMuser.objects.get(am_id=request.session['am_id'])
	myAcnt = Account()
	pythoncom.CoInitialize()
	myTrade = Trade(myAcnt)
	if myTrade is False:
		return HttpResponse("myTrade session is over")

	# pythoncom.CoInitialize()
	myTrade.logIn(m.am_id,m.am_pass)
	for share in shareList:
		print(share.code)
		time.sleep(0.1)
		price =myTrade.getNowStockPrc(share.code) #return (price, cgdgree)
		# print("price", price[0])
		priceDict[share.code]=price[0]
	myTrade.logOut()
	del myTrade
	#t8430의 reprice가 현재값을 나타내고 있다면 해당 값으로 확인 아니라도 해당 TR로 구현

	#3. #2에서의 정보를 context에 삽입후 analysis.html에 띄우기
	context['shareList']=shareList
	context['priceDict']=priceDict
	context['analysis_type']=analysisType
	return render(request, 'analysis.html', context)




























