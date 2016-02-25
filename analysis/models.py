from django.db import models
from datetime import datetime, timezone, timedelta

# Create your models here.
class Share(models.Model):
	"""This class a model means purchase candidate share from some analysis algorithms"""
	analysis_type = models.CharField(max_length=15) #R3I, R10T, BOX
	name = models.CharField(max_length=50) #name of stock
	code = models.CharField(max_length=10) #code os stock
	init_price = models.IntegerField(default=0)#initial price of stock derived from analysis algorithm
	now_price = models.IntegerField(default=0)#now price of stock
	drv_date = models.DateTimeField('date derived',auto_now_add = True)#date derived from analysis algorithm
	# drv_date = models.DateTimeField('date derived',default=datetime.now())

	#share.save() 를 통해 now_price를 저장 할때마다 drv_date가 갱신됨.. 해당 문제 해결해야함
	#해결 방법 1. auto_now_add 파라미터를 True로 넘겨서 생성될때만 기억
	#해결 방법 2. default=timezone.now

	def __str__(self):
		return "%s, %s, %s, %s, %s, %s"%(self.analysis_type, self.name, self.code, self.init_price,self.now_price, self.drv_date)

	def getDays(self):
		return (datetime.now(timezone.utc)-self.drv_date).days
		# return (datetime.now()-self.drv_date).days
	def getDate(self):
		return self.drv_date+timedelta(hours=9)
	def getDiffPrc(self):
		return int(self.now_price-self.init_price)
		
class AMuser(models.Model):
	"""This class a model means my Asset Manager user"""
	am_id = models.CharField(max_length=10)
	am_pass = models.CharField(max_length=30)
	account_number = models.CharField(max_length=14)
	account_pw = models.CharField(max_length=4)
	xing_id = models.CharField(max_length=10)
	xing_pass = models.CharField(max_length=8)
	xing_certificate_pass = models.CharField(max_length=10)

	def __str__(self):
		return "amiD; %s, am-pass: %s, Acnt_number:%s, Acnt_pw: %s, xing_id: %s, xing_pass: %s, xing_certificate_pass: %s"%(self.am_id, self.am_pass, self.account_number, self.account_pw, self.xing_id, self.xing_pass, self.xing_certificate_pass)

class StockMarket(models.Model):#COSPI: 001, COSDAQ: 301
	'''This class is a model means stock marget information'''
	gubun = models.CharField(max_length=1,default='0')#gubun COSPI : 1, COSDAQ: 2
	hname = models.CharField(max_length=20)#hname
	pricejisu = models.IntegerField(default=0)#pricejisu
	jniljisu = models.IntegerField(default=0)#jniljisu
	sign =  models.IntegerField(default=-1)#sign
	change = models.IntegerField(default=-1)#change
	diffjisu = models.IntegerField(default=-1)#diffjisu
	volume = models.IntegerField(default=-1)##volume
	jnilvolume = models.IntegerField(default=-1)#jnilvolume
	volumechange = models.IntegerField(default=-1)#volumechange
	volumerate = models.IntegerField(default=-1)#volumerate
	market_date = models.DateTimeField(auto_now=True)

	def getSign(self):
		return self.attrSwitch('sign',self.sign)

	def attrSwitch(self,attrname, attrcontent):
		return {
				'sign': {1:'상한', 2:'상승', 3:'보합', 4:'하한', 5:'하락'}
			}.get(attrname).get(attrcontent)
