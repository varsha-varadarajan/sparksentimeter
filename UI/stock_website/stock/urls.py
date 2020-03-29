from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^topg/$', views.topg, name='topg'),
    url(r'^current/$', views.current, name='current'),
    url(r'^today/$', views.today, name='today'),
    url(r'^experts$', views.experts, name='experts'),
    url(r'^company_reviews$', views.company_reviews, name='company_reviews'),
    url(r'^todays_comments$', views.todays_comments, name='todays_comments'),
    url(r'^try_python/$', views.try_python, name='try_python'),
]