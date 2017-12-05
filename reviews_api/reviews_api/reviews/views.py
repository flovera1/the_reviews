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
from accounts.api.serializers import UserSerializer
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


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset 		 = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

def reviews_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	form = ReviewsForm(request.POST or None, request.FILES or None)
	'''if form.is_valid():
		instance 	  = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	'''
	context = {
		"form": form,
	}
	return render(request, "reviews_form.html", {})



def reviews_detail(request, slug=None):
	instance = get_object_or_404(Reviews, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	context = {
		"company": instance.company,
		"pub_date": instance.pub_date,
		"user_name": instance.user_name,
		"comment": instance.comment,
		"rating": instance.rating,
		"title": instance.title,
		"summary": instance.summary,
		"ip": instance.ip,

	}
	return render(request, "post_detail.html", context)

def reviews_list(request):
	today = timezone.now().date()
	queryset_list = Reviews.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Reviews.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "reviews_list.html", context)


def reviews_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Reviews, slug=slug)
	form     = ReviewsForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "reviews_form.html", context)



def reviews_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Reviews, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("reviews:list")