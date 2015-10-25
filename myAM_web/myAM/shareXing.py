import win32com.client
#import yjauthentication
import pythoncom
import Log
import time
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myAM_web.settings'
from analysis.models import Share, AMuser # code to TEST DB

from XASessionEventClass import XASessionEvents
from XAQueryEventClass import XAQueryEvents
#from company import Company
#from account import Account
import common.xingINFO as xing

class myXing(object):
	"""docstring for myXing"""
	def __init__(self, arg):
		super(myXing, self).__init__()
		self.arg = arg

	def logIn(self, u_id, u_pass):
        #It makes an authentification by Xing API

 		self.user=AMuser.objects.get(am_id = u_id,am_pass= u_pass)

		inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
 		inXASession.ConnectServer(xing.server_addr, xing.server_port)
		inXASession.Login(self.user.xing_id, self.user.xing_pass, self.user.xing_certificate_pass, xing.server_type, 0)

		while XASessionEvents.logInState == 0:
			pythoncom.PumpWaitingMessages()
            
		print("Log in Success")
