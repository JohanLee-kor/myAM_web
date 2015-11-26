from django.db import models
from datetime import datetime, timezone

# Create your models here.
class Share(models.Model):
	"""This class a model means purchase candidate share from some analysis algorithms"""
	analysis_type = models.CharField(max_length=15) #R3I, R10T, BOX
	name = models.CharField(max_length=50) #name of stock
	code = models.CharField(max_length=10) #code os stock
	init_price = models.IntegerField(default=0)#initial price of stock derived from analysis algorithm
	now_price = models.IntegerField(default=0)#now price of stock
	drv_date = models.DateTimeField('date derived',auto_now = True)#date derived from analysis algorithm

	def __str__(self):
		return "%s, %s, %s, %s, %s, %s"%(self.analysis_type, self.name, self.code, self.init_price,self.now_price, self.drv_date)

	def getDays(self):
		return (datetime.now(timezone.utc)-self.drv_date).days
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
