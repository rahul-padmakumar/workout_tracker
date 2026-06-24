

from tracker.models import (
  BodyPart,
  Exercise,
  MuscleGroup,
  Program,
  Workout,
  WorkoutSets,
  ProgramWorkout,
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


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for workout data"""
    class Meta:
        model = Workout
        fields = [
            'id',
            'name',
            'date',
            'duration_min',
            'notes',
            'created_at'
        ]
        read_only_field = [
            'id',
            'created_at'
        ]


class ProgramWorkoutDetailSerializer(serializers.ModelSerializer):
    """ Serializer for program workout """
    workout_id = serializers.IntegerField(source="workout.id")
    name = serializers.CharField(source='workout.name')
    date = serializers.DateTimeField(source='workout.date')
    duration_min = serializers.IntegerField(source='workout.duration_min')

    class Meta:
        """Meta for indicating model"""
        model = ProgramWorkout
        fields = [
            'workout_id',
            'name',
            'date',
            'duration_min',
            'week_number',
            'day_of_week'
        ]
        read_only_fields = [
            'workout_id',
            'name',
            'date',
            'duration_min',
            'week_number',
            'day_of_week'
        ]


class ProgramReadSerializer(serializers.ModelSerializer):
    """Serializer for reading a particular program data"""
    workouts = ProgramWorkoutDetailSerializer(
        source='program_workouts', many=True
    )

    class Meta:
        model = Program
        fields = [
            'name',
            'description',
            'created_at',
            'duration_in_weeks',
            'workouts'
        ]
        read_only_fields = [
            'name',
            'description',
            'created_at',
            'duration_in_weeks',
            'workouts'
        ]


class WorkoutSetSerializer(serializers.ModelSerializer):
    """Serializer for workout set"""
    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all()  # pylint: disable=no-member
    )

    class Meta:
        model = WorkoutSets
        fields = [
            'id',
            'workout',
            'exercise',
            'set_number',
            'repetitions',
            'weight_kg',
            'rest_time_sec',
            'duration_sec',
            'distance_m',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'workout']
