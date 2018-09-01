#coding:utf8
from django.conf.urls import url
from . import views
urlpatterns =[
    #url(r'^books/$',views.BookGenericAPIView.as_view(),name='view_name'),
    url(r'^books/(?P<pk>\d+)/$',views.BookGenericAPIView.as_view(),name='view_name'),
]



