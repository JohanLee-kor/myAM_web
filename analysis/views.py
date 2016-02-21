from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from myAM_web.myAM.TradeAstock import Trade
from myAM_web.myAM.account import Account
from datetime import timedelta, timezone, datetime

from .models import Share, AMuser, StockMarket
import pythoncom
import time
# Create your views here.
def main(request):
	context={}
	# 0. 세션 확인(로그인 여부 확인)
	isLogin =  request.session.get('am_id', False)
	if isLogin is False:
		return HttpResponseRedirect(reverse('home'))

	# 1. 디비에 접근하여서  최근일자(10일간)의 후보 주식들 갖고오기
	now = datetime.now(timezone.utc)
	srt = now-timedelta(days=10)
	shareList = Share.objects.filter(drv_date__range=(srt,now))
	
	# 2.  COSPI, COSDAQ 정보 가져오기
	# COSPI: 001, COSDAQ: 301 - Xing API
	# COSPI: 1, COSDAQ: 2 - gubun
	cospiInfo=StockMarket.objects.filter(gubun='1', market_date__range=(srt,now))
	cosdaqInfo=StockMarket.objects.filter(gubun='2', market_date__range=(srt,now))

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

	#2. #1 에서의 정보를 context에 삽입후 analysis.html에 띄우기
	context['shareList']=shareList
	context['analysis_type']=analysisType
	return render(request, 'analysis.html', context)

def deleteShare(request):
	context={}
	delShares = request.POST.getlist('delete')
	share_type=request.POST.get('type',False)
	fromPage = request.META['HTTP_REFERER']
	for share in delShares:
		Share.objects.get(code=share,analysis_type=share_type).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])





























