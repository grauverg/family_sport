from django.urls import path

from . import views


urlpatterns = [
    path('coaches/', views.CoachListView.as_view(), name='coaches_list'),
    path('coaches/<slug:slug>/', views.CoachDetailView.as_view(), name='coach_detail'),
    path('sports/<slug:slug>/', views.SportTypeDetailView.as_view(), name='sport_detail'),
    path('sports/', views.SportTypeListView.as_view(), name='sports_list')
]
