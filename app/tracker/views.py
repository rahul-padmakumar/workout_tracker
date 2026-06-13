from core.utils.base_response import SuccessResponse
from core.utils.permissions import IsFullAuthToken
from tracker.serializers import ExerciseSerializer
from rest_framework import generics
from django.apps import apps
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExerciseFilter
# Create your views here.


class ExerciseListView(generics.ListAPIView):
    """View to list all exercises."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]
    queryset = apps.get_model(
        'tracker',
        'Exercise'
    ).objects.prefetch_related(
        'muscle_groups',
        'body_part'
    ).filter(is_active=True)
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExerciseFilter

    def get(self, request, *args, **kwargs):
        """List all exercises."""
        return SuccessResponse(
            data=self.list(request, *args, **kwargs).data,
        )
