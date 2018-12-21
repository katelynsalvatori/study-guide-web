from django.conf.urls import patterns, include, url
from myapp import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'django_proj.views.home', name='home'),
#     # url(r'^django_proj/', include('django_proj.foo.urls')),

#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),

#     url(r'^time/', views.current_datetime),
#     url(r'^users/', views.users),
#     url(r'^studyguides/<int:user_id>/', views.study_guides)
# )

urlpatterns = patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user),
    url(r'^studyguide/(?P<study_guide_id>[0-9]+)/$', views.study_guide),
    url(r'^$', views.home),
)
