from django.conf.urls import include, url
from myapp import views

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user),
    url(r'^studyguide/(?P<study_guide_id>[0-9]+)/$', views.study_guide),
    url(r'^deleteuser/(?P<user_id>[0-9]+)/$', views.delete_user),
    url(r'^deletestudyguide/(?P<study_guide_id>[0-9]+)/$', views.delete_study_guide),
    url(r'^deletequestion/(?P<question_id>[0-9]+)/$', views.delete_question),
    url(r'^deleteanswer/(?P<answer_id>[0-9]+)/$', views.delete_answer),
    url(r'^editstudyguide/(?P<study_guide_id>[0-9]+)/$', views.edit_study_guide),
    url(r'^savestudyguide/(?P<study_guide_id>[0-9]+)/$', views.save_study_guide),
    url(r'^validate/', views.validate_answers),
    url(r'^$', views.home)
]
