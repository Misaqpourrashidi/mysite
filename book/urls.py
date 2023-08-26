from django.urls import path
from book.views import (
	HomeView,
	CalendarView,
	ArticleDetailView,
	delete_comment,
	delete_reply,
)

urlpatterns = [
	path('', HomeView.as_view(), name="home"),
	path('calendar/', CalendarView.as_view(), name="calendar"),
	path('article/<slug:slug>', ArticleDetailView.as_view(), name="article-detail"),
	path('delete/<int:pk>/<slug:slug>', delete_comment, name='delete'),
	path('delete_reply/<int:pk>/<slug:slug>', delete_reply, name='delete_reply'),
]