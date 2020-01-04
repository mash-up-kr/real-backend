from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DreamListCreateAPIView, DreamRetrieveUpdateDestroyAPIView, ResultCreateUpdateAPIView, \
    DreamHistoryListAPIView

urlpatterns = format_suffix_patterns([
    path('', DreamListCreateAPIView.as_view(), name='dream_list'),
    path('history/', DreamHistoryListAPIView.as_view(), name='dream_list'),
    path('<int:pk>/', DreamRetrieveUpdateDestroyAPIView.as_view(), name='dream_detail'),
    path('<int:pk>/result/', ResultCreateUpdateAPIView.as_view(), name='dream_detail'),
])
