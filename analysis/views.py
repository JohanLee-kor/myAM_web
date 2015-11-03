from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from myAM_web.myAM.TradeAstock import Trade

from .models import Share
# Create your views here.
def main(request):
	context={}
	return render(request, 'main.html', context)

def analysisShare(request, analysis_type):#analysis_type 0: R3I, 1: R10T, 2: BOX
	context={}
	return render(request, 'analysis.html', context)
