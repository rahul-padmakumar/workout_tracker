from django.contrib import admin # noqa

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import user, user_profile
from django.utils.translation import gettext_lazy as _
from tracker.models import BodyPart, MuscleGroup, Exercise, Program, Workout, ProgramWorkout, WorkoutSets

@admin.register(user.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin page for users"""
    list_display = ['email', 'phone_number', 'is_active', 'is_staff']
    ordering = ['id']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('phone_number',)}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']


@admin.register(user_profile.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Define the admin page for user profiles"""


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
