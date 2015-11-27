from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from myAM_web.myAM.TradeAstock import Trade
from myAM_web.myAM.account import Account
import pythoncom

from analysis.models import Share, AMuser
# Create your views here.
def home(request):
	context={}
	return render(request, 'login.html', context)

def login(request):
	m = AMuser.objects.get(am_id=(request.POST['ID']).strip())
	if m.am_pass == request.POST['PW']:
		request.session['am_id'] = m.am_id
		return HttpResponseRedirect(reverse('main'))
	else:
		return HttpResponse("Your username and password didn't match.")
