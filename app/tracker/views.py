from core.utils.base_response import SuccessResponse
from core.utils.permissions import IsFullAuthToken
from tracker.serializers import (
  ExerciseSerializer,
  ProgramSerializer,
)
from rest_framework import generics
from django.apps import apps
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExerciseFilter
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet
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


class ProgramViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]
    queryset = apps.get_model(
        "tracker",
        'Program'
    ).objects.all()
    serializer_class = ProgramSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request, *args, **kwargs):
        return SuccessResponse(
            data=super.get(self, request, args, kwargs).data
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return SuccessResponse(
            data=serializer.data,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse(
            data="Program deleted successfully"
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(
            data=serializer.data,
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
