from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^member/login',include('member.urls')),
    # url(r'^analysis/',include('analysis.'))
    url(r'^main/$',views.main,name='main'),
]
