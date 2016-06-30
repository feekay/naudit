"""audit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from teams import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^entries/$', views.entries_view),
    url(r'^edit/(?P<entry_id>[\d]+)/$', views.edit_entry),
    url(r'^entries/(?P<entry_id>[\d]+)/$', views.entry),
    url(r'^counts/$', views.emp_entries),
    url(r'^entries/$', views.entries_view),
    url(r'^pending/(?P<entry_id>[\d]+)/$', views.entry,{'pending':True}),
    url(r'^companies/$', views.companies_view),
    url(r'^members/$', views.members_view),
    url(r'^routes/$', views.routes_view),
    url(r'^pending/$', views.pending_view),
    url(r'^add_company/$', views.add_company),
    url(r'^add_member/$', views.add_member),
    url(r'^add_route/$', views.add_route),
    url(r'^add_entry/$', views.add_entry),
    url(r'^settings/$', views.settings),
    url(r'^suggest_member/$', views.suggest_member),
    url(r'^messages/get/$', views.get_messages),
    url(r'^messages/send/$', views.send_message),
    url(r'^messages/$', views.messages),
    url(r'^activity/$', views.activity),
    url(r'^quiz/$', views.quiz),
    url(r'^add_quiz/$', views.add_quiz)
]
