# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
#from posts.api.permissions import IsOwnerOrReadOnly
#from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from django.http import HttpResponse, HttpResponseRedirect, Http404
from accounts.api.serializers import(
	UserCreateSerializer,
	UserLoginSerializer,
	#create_reviews_serializer		
	)
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.filters import(
	SearchFilter,
	OrderingFilter,
	)
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)
from rest_framework.permissions import(
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
# Create your views here.
from rest_framework import generics
from .serializers import ReviewsSerializer
from accounts.api.serializers import UserSerializer, CompanySerializer
from .models import Reviews, Company
from django.contrib.auth.models import User, Group
from rest_framework import permissions
from reviews.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
#create an endpoint for the root of our API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import renderers

from rest_framework import status


try:
    from urllib import quote_plus #python 2
except:
    pass
try:
    from urllib.parse import quote_plus #python 3
except: 
    pass
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import ReviewsForm
from .models import Reviews

User = get_user_model()


def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARD_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip

class CreateView(generics.ListCreateAPIView):
	"""This class defines the create behavior of our rest api."""
	queryset 		   = Reviews.objects.all()
	serializer_class   = ReviewsSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


	def perform_create(self, serializer):
		#serializer.data.ip_address = get_ip(self.request)
		print(serializer.validated_data["ip_address"])
		serializer.validated_data["ip_address"] = get_ip(self.request)
		#serializer..ip_address = get_ip(self.request)
		serializer.save(owner = self.request.user)



	def filter_queryset(self, queryset):
		if self.request.user.is_authenticated():
			queryset = Reviews.objects.filter(owner=self.request.user)
			return queryset
		return Reviews.objects.all()




class DetailsView(generics.RetrieveUpdateDestroyAPIView, RetrieveAPIView):
	"""This class handles the http GET, PUT and DELETE requests."""
	queryset 		 = Reviews.objects.all()
	serializer_class = ReviewsSerializer
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
	



class Company(generics.ListAPIView):
	queryset         = Company.objects.all()
	serializer_class = CompanySerializer




