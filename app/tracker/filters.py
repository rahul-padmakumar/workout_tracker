from django.apps import apps
from django_filters.rest_framework import FilterSet, ChoiceFilter

class ExerciseFilter(FilterSet):
    """Filter for Exercise model."""

    equipments = ChoiceFilter(
        field_name='equipment',
        choices=apps.get_model('tracker', 'Exercise').EQUIPMENT_TYPES,
    )
    difficulty_levels = ChoiceFilter(
        field_name='difficulty',
        choices=apps.get_model('tracker', 'Exercise').DIFFICULTY_LEVELS,
    )

    class Meta:
        model = apps.get_model('tracker', 'Exercise')
        fields = {
            'name': ['icontains'],
            'muscle_groups__name': ['icontains'],
            'body_part__name': ['icontains'],
            'body_part__id': ['exact'],
            'muscle_groups__id': ['exact'],
        }