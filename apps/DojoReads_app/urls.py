from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^books$',views.success),
    url(r'^books/add$',views.add),
    url(r'^books/add_book_review',views.add_book_review),
    url(r'^books/(?P<book_id>\d+)$',views.book_page),
    url(r'^books/(?P<book_id>\d+)/add_review',views.add_review),
    url(r'^users/(?P<user_id>\d+)$',views.user_page)
]