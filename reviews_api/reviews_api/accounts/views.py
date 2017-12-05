# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
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
    
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
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
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm
from accounts.api.serializers import UserLoginSerializer

from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from accounts.api.serializers import UserSerializer, UserCreateSerializer
from rest_framework import generics

from rest_framework.views import APIView


def login_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "form.html", {"form":form, "title": title})


def register_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset         = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset         = User.objects.all()



class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class   = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data               = request.data #request.post
        serializer         = UserLoginSerializer(data = data)   
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)   
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)