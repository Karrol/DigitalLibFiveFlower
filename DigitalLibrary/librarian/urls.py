from django.conf.urls import url

import librarian.views as views
app_name='librarian'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^librarian_book', views.librarian_book, name='librarian_book'),
    url(r'^librarian_booktype', views.librarian_booktype, name='librarian_booktype'),
    url(r'^librarian_borrow', views.librarian_borrow, name='librarian_borrow'),
    url(r'^librarian_history', views.librarian_history, name='librarian_history'),
    url(r'^librarian_user', views.librarian_user,name='librarian_user'),
    url(r'^librarian_usertype', views.librarian_usertype, name='librarian_usertype'),
    url(r'^librarian_ebook', views.librarian_ebook, name='librarian_ebook'),
    url(r'^librarian_bookshelf', views.librarian_bookshelf, name='librarian_bookshelf'),
    url(r'^librarian_CD', views.librarian_CD, name='librarian_CD'),
    url(r'^add_user_to_database', views.add_user_to_database, name='add_user_to_database'),
    url(r'^change_user_to_database', views.change_user_to_database, name='change_user_to_database'),
    url(r'^delete_user', views.delete_user, name='delete_user'),
]
