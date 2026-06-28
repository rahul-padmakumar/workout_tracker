

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
from django.apps import apps


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


class ProgramWorkoutSerializer(serializers.ModelSerializer):
    """Serializer for program workout for fetching within workout detail"""

    class Meta:
        model = ProgramWorkout
        fields = [
            'program',
            'week_number',
            'day_of_week'
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
    exercise_name = serializers.CharField(source='exercise.name')
    muscle_groups = MuscleGroupSerializer(
        source='exercise.muscle_groups',
        many=True
    )
    body_part = BodyPartSerializer(source='exercise.body_part', many=True)

    class Meta:
        model = WorkoutSets
        fields = [
            'id',
            'exercise_name',
            'muscle_groups',
            'body_part',
            'set_number',
            'repetitions',
            'weight_kg',
            'rest_time_sec',
            'duration_sec',
            'distance_m',
        ]
        read_only_fields = ['id']


class WorkoutDetailReadSerializer(serializers.ModelSerializer):
    """Serializer for workout detail retrieval"""
    sets = WorkoutSetSerializer(source='workout_sets', many=True)
    program_workout = ProgramWorkoutSerializer(
        source='workout_programs',
        many=True
    )

    class Meta:
        model = Workout
        fields = [
            'name',
            'date',
            'duration_min',
            'notes',
            'sets',
            'program_workout'
        ]
        read_only_fields = [
            'name',
            'date',
            'duration_min',
            'notes',
            'sets',
            'program_workout'
        ]


class WorkoutSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSets
        fields = [
            'id',
            'exercise',
            'workout',
            'set_number',
            'repetitions',
            'weight_kg',
            'rest_time_sec',
            'duration_sec',
            'distance_m',
        ]
        read_only_fields = [
            'id',
            'workout'
        ]


class WorkoutCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workouts"""
    sets = WorkoutSetCreateSerializer(source='workout_sets', many=True)
    program_id = serializers.IntegerField(write_only=True)
    week_number = serializers.IntegerField(write_only=True)
    day_of_week = serializers.IntegerField(write_only=True)

    class Meta:
        model = Workout
        fields = [
            'id',
            'name',
            'date',
            'duration_min',
            'notes',
            'sets',
            'program_id',
            'week_number',
            'day_of_week',
        ]
        read_only_fields = [
            'id'
        ]

    def create(self, validated_data):
        print(validated_data)
        workout_sets_data = validated_data.pop('workout_sets')
        program_id = validated_data.pop('program_id')
        week_number = validated_data.pop('week_number')
        day_of_week = validated_data.pop('day_of_week')

        print(f"Hello {validated_data}")

        workout_model = apps.get_model(
            'tracker',
            'Workout'
        )
        workout = workout_model.objects.create(**validated_data)

        program_model = apps.get_model(
            'tracker',
            'ProgramWorkout'
        )

        program = apps.get_model(
            'tracker',
            'Program'
        ).objects.get(id=program_id)

        program_model.objects.create(
            workout=workout,
            week_number=week_number,
            day_of_week=day_of_week,
            program=program
        )

        workout_set_model = apps.get_model(
            'tracker',
            'WorkoutSets'
        )

        workout_set_model.objects.bulk_create(
            [
                WorkoutSets(workout=workout, **workout_set_data)
                for workout_set_data in workout_sets_data
            ]
        )

        return workout

    def update(self, instance, validated_data):
        workout_sets_data = validated_data.pop('workout_sets', None)
        program_id = validated_data.pop('program_id', None)
        week_number = validated_data.pop('week_number', None)
        day_of_week = validated_data.pop('day_of_week', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if program_id or week_number or day_of_week:
            program_model = apps.get_model(
                'tracker',
                'ProgramWorkout'
            )
            program_workout = program_model.objects.get(
                workout=instance
            )
            if program_id:
                program = apps.get_model(
                    'tracker',
                    'Program'
                ).objects.get(id=program_id)
                if program != program_workout.program:
                    program_workout.program = program
            if week_number:
                program_workout.week_number = week_number
            if day_of_week:
                program_workout.day_of_week = day_of_week
            program_workout.save()

        if workout_sets_data is not None:
            instance.workout_sets.all().delete()

            workout_set_model = apps.get_model(
                'tracker',
                'WorkoutSets'
            )

            workout_set_model.objects.bulk_create(
                [
                    WorkoutSets(workout=instance, **workout_set_data)
                    for workout_set_data in workout_sets_data
                ]
            )

        return instance
