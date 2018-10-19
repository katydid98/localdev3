from django.conf.urls import url

from . import views
#from .views import SuccessView

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^question_form$', views.QuestionChoiceCreate.as_view(), name='question'),
    # url(r'^question_form/choices/$', views.ChoicesCreate.as_view(), name='choices'),
    # url(r'^successpage$', views.SuccessView.as_view(), name='successpage'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
