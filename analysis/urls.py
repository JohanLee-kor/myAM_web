from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^member/login',include('member.urls')),
    # url(r'^analysis/',include('analysis.'))
    url(r'^main/$',views.main,name='main'),
    url(r'^(?P<analysisType>[A-Za-z0-9]+)/$', views.analysisShare, name='analysisShare'),#analysis_type 0: R3I, 1: R10T, 2: BOX
    url(r'^delete/$',views.deleteShare,name='delete'),
]
