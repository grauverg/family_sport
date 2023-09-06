from django import forms
from django.contrib import admin

from . import models


@admin.register(models.SportType)
class SportTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('slug_field', )
    pass


@admin.register(models.Coach)
class CoachAdmin(admin.ModelAdmin):

    fields = [
        'image_tag',
        'profile_image',
        'first_name',
        'middle_name',
        'last_name',
        'age',
        'description',
        'sport_coaching',
        'slug_field',
    ]

    readonly_fields = ['slug_field', 'image_tag']
    list_display = ['get_fullname', 'age', 'sport_coaching', ]


@admin.register(models.TrainingInfo)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'sport_type', 'coach']
    # list_display_links =
    readonly_fields = ['end_time', ]

    def display_coaches(self):
        return ', '.join(coach.get_fullname() for coach in self.coach.all())


@admin.register(models.ProfileImage)
class ProfileImagesAdmin(admin.ModelAdmin):
    pass
