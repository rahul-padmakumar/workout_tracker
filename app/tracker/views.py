from core.utils.permissions import IsFullAuthToken
from tracker.serializers import ExerciseSerializer
from rest_framework import generics
from django.apps import apps
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view
# Create your views here.


class ExerciseListView(generics.ListAPIView):
    """View to list all exercises."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]
    queryset = apps.get_model('tracker', 'Exercise').objects.filter(is_active=True)
    serializer_class = ExerciseSerializer