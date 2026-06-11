from django.urls import path
from .views import ExerciseListView

app_name = 'tracker'

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
]
