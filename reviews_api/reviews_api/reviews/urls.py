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
from .views import Company


from rest_framework import routers

urlpatterns = [
    url(r'^admin/', admin.site.urls),											# admin, check the token_auth

	url(r'^reviews/$', CreateView.as_view(), name="create"),					# create the reviews

	url(r'^reviews/(?P<pk>\d+)/$', DetailsView.as_view(), name="details"),	# chek the review (and delete them)

	url(r'^users/$', UserList.as_view()),										# Reviewer Metadata. Information about the reviers/users! 

	#url(r'^login/$', UserLoginAPIView.as_view(), name = 'login'), 				# login a user

	url(r'^register/$', UserCreateAPIView.as_view(), name = 'register'), 		# register a user 

	url(r'^companies/$', Company.as_view(), name='companies_info')				# Company. information (name of the company) about
																  				# the companies to reviewed
]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]