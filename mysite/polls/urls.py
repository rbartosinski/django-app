from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/edit/', views.EditQuestionView.as_view(), name='edit'),
    path('<int:question_id>/delete/', views.DeleteQuestionView.as_view(), name='delete'),
    path('<int:question_id>/add_choice/', views.AddChoiceView.as_view(), name='add_choice'),
    path('<int:question_id>/<int:choice_id>/edit_choice/', views.EditChoiceView.as_view(), name='edit_choice'),
    path('<int:question_id>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.VoteView.as_view(), name='vote'),
]

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]
