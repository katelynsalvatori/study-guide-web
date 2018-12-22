from django.conf.urls import patterns, include, url
from myapp import views

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user),
    url(r'^studyguide/(?P<study_guide_id>[0-9]+)/$', views.study_guide),
    url(r'^deleteuser/(?P<user_id>[0-9]+)/$', views.delete_user),
    url(r'^createstudyguide/(?P<study_guide_id>[0-9]+)/$', views.create_study_guide),
    url(r'^$', views.home)
)
