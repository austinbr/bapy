from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.dashboard),
#     url(r'^(?P<id>\d+)$', views.showCat),
#     url(r'^like/(?P<id>\d+)$', views.likeCat),
    url(r'^joinprocess/(?P<id>\d+)$', views.joinProcess),
    url(r'^destination/(?P<id>\d+)$', views.showDest),
    url(r'^add$', views.travelAdd),
    url(r'^process$', views.travelProcess),
#     url(r'^update$', views.catUpdate),
]