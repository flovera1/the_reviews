from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView
from accounts.views import UserList 
from accounts.views import UserDetail
from accounts.views import UserCreateAPIView
from accounts.views import UserLoginAPIView
from rest_framework.authtoken import views
from .views import (
	reviews_list,
	reviews_create,
	reviews_detail,
	reviews_update,
	reviews_delete,
	)
from rest_framework import routers
#from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^reviews/$', CreateView.as_view(), name="create"),
	url(r'^reviews/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
	url(r'^users/$', UserList.as_view()),
	#url(r'^api/auth/token/', obtain_jwt_token),
	#url(r'^api-token-auth/', views.obtain_auth_token),
	url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
	url(r'^login/$', UserLoginAPIView.as_view(), name = 'login'),
	url(r'^register/$', UserCreateAPIView.as_view(), name = 'register'),

	#
	url(r'^$', reviews_list, name='list'),
    url(r'^create/$', reviews_create),
    url(r'^(?P<slug>[\w-]+)/$', reviews_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', reviews_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', reviews_delete)

]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]