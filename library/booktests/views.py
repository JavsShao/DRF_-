from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serializers import BookInfoSerializer
from .models import BookInfo


