from django.db import models
from django.conf import settings

# Create your models here.
class BodyPart(models.Model):
    """Model representing a body part."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
    
class MuscleGroup(models.Model):
    """Model representing a muscle group."""
    name = models.CharField(max_length=100, unique=True)
    body_parts = models.ForeignKey(BodyPart, related_name='muscle_groups', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.body_parts.name})"


class Exercise(models.Model):
    """Model representing an exercise."""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    EQUIPMENT_TYPES = [
        ('cable', 'Cable'),
        ('body_weight', 'Body Weight'),
        ('resistance_band', 'Resistance Band'),
        ('kettlebell', 'Kettlebell'),
        ('dumbbell', 'Dumbbell'),
        ('barbell', 'Barbell'),
        ('other', 'Other'),
        ('lever_plate_loaded', 'Lever Plate Loaded Machine'),
        ('lever_selectorized', 'Lever Selectorized Machine'),
        ('smith_machine', 'Smith Machine'),
        ('sled', 'Sled'),
    ]
    name = models.CharField(max_length=100, unique=True)
    preparation = models.TextField(blank=True)
    execution = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    muscle_groups = models.ManyToManyField(MuscleGroup, related_name='exercises')
    equipment = models.CharField(max_length=50, choices=EQUIPMENT_TYPES, default='body_weight')
    body_part = models.ManyToManyField(BodyPart, related_name='exercises', blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Difficulty: {self.difficulty})"


class Program(models.Model):
    """Model representing a workout program."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration_in_weeks = models.PositiveIntegerField(default=4)

    def __str__(self):
        return f"{self.name}"
    

class Workout(models.Model):
    """Model representing a workout session."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    duration_min = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    

class ProgramWorkout(models.Model):
    """Model representing the association between a workout and a program."""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_workouts')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_programs')
    week_number = models.PositiveIntegerField()
    day_of_week = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.program.name} - Week {self.week_number}, Day {self.day_of_week}"
    
class WorkoutSets(models.Model):
    """Model representing the sets performed in a workout."""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_sets')
    set_number = models.PositiveIntegerField(null=True, blank=True)
    repetitions = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.FloatField(blank=True, null=True)
    rest_time_sec = models.PositiveIntegerField(default=0)
    duration_sec = models.PositiveIntegerField(null=True, blank=True)
    distance_m = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name} Set {self.set_number}"
