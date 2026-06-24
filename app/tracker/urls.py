from django.urls import path
from .views import (
  ExerciseListView,
  ProgramViewSet,
  WorkoutViewSet,
)
from rest_framework.routers import DefaultRouter

app_name = 'tracker'

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'workouts', WorkoutViewSet, basename='workouts')

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
]

urlpatterns += router.urls
