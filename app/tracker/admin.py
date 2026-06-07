from django.contrib import admin
from tracker.models import (
  BodyPart, MuscleGroup, Exercise,
  Program, Workout, ProgramWorkout, WorkoutSets
)


@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    """Admin page for body parts"""


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    """Admin page for muscle groups"""


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin page for exercises"""
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Admin page for workout programs"""
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin page for workouts"""
    readonly_fields = ['created_at']


@admin.register(ProgramWorkout)
class ProgramWorkoutAdmin(admin.ModelAdmin):
    """Admin page for program workouts"""


@admin.register(WorkoutSets)
class WorkoutSetsAdmin(admin.ModelAdmin):
    """Admin page for workout sets"""
    readonly_fields = ['created_at']
