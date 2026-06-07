from django.db import models

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