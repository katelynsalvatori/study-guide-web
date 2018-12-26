from django.conf.urls import include, url
from myapp import views

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^studyguide/(?P<study_guide_id>[0-9]+)/$', views.study_guide, name='studyguide'),
    url(r'^deleteuser/(?P<user_id>[0-9]+)/$', views.delete_user, name='deleteuser'),
    url(r'^deletestudyguide/(?P<study_guide_id>[0-9]+)/$', views.delete_study_guide, name='deletestudyguide'),
    url(r'^deletequestion/(?P<question_id>[0-9]+)/$', views.delete_question, name='deletequestion'),
    url(r'^deleteanswer/(?P<answer_id>[0-9]+)/$', views.delete_answer, name='deleteanswer'),
    url(r'^editstudyguide/(?P<study_guide_id>[0-9]+)/$', views.edit_study_guide, name='editstudyguide'),
    url(r'^savestudyguide/(?P<study_guide_id>[0-9]+)/$', views.save_study_guide, name='savestudyguide'),
    url(r'^validate/', views.validate_answers, name='validate'),
    url(r'^$', views.home, name='home')
]
