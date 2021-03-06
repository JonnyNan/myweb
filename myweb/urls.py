"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from books import views as books_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', books_views.index),
    url(r'^login/$', books_views.login),
    url(r'^signup/$', books_views.signup),
    url(r'^realSignup/$', books_views.realSignup),
    url(r'^loginpage/$', books_views.loginpage),
    url(r'^table/$', books_views.table),
    url(r'^search/$', books_views.search),
    url(r'^search_lagou/$', books_views.search_lagou),
    url(r'^login_success/$', books_views.login_success),
]
