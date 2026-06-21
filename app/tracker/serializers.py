

from tracker.models import (
  BodyPart,
  Exercise,
  MuscleGroup,
  Program,
)
from rest_framework import serializers


class BodyPartSerializer(serializers.ModelSerializer):
    """Serializer for BodyPart model."""
    class Meta:
        model = BodyPart
        fields = ['id', 'name']
        read_only_fields = ['id']


class MuscleGroupSerializer(serializers.ModelSerializer):
    """Serializer for MuscleGroup model."""
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name']
        read_only_fields = ['id']


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercise model."""
    muscle_groups = MuscleGroupSerializer(many=True, read_only=True)
    body_part = BodyPartSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'preparation', 'execution', 'comments', 'difficulty',
            'muscle_groups', 'equipment', 'body_part',
            'is_active', 'created_at', 'updated_at', 'video_url'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProgramSerializer(serializers.ModelSerializer):
    """Serializer for program model"""
    class Meta:
        model = Program
        fields = [
            'id', 'name', 'description',
            'created_at',
            'updated_at',
            'duration_in_weeks'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
