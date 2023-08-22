from django.contrib import admin

from . import models


@admin.register(models.Coach)
class CoachAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TrainingInfo)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'sport_type', 'coach']
    # list_display_links =
    readonly_fields = ['end_time', ]

    def display_coaches(self):
        return ', '.join(coach.get_fullname() for coach in self.coach.all())


@admin.register(models.SportType)
class SportTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProfileImage)
class ProfileImagesAdmin(admin.ModelAdmin):
    pass
