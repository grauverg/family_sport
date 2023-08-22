from django.db import models
from datetime import datetime, date
from transliterate import slugify


def profile_photos(instance, filename):
    return f'coaches/{instance.coach.slug_field}/{filename}'


class Coach(models.Model):
    class Meta:
        verbose_name = "Coach"
        verbose_name_plural = 'Coaches'

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)

    age = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    sport_coaching = models.ForeignKey('SportType', on_delete=models.PROTECT)

    slug_field = models.SlugField(default='', null=False)

    def get_fullname(self):
        return f'{self.last_name} {self.first_name}'

    def get_fullname_with_middle(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def short_description(self):
        if len(f'{self.description}') > 30:
            return f'{self.description[:30]}...'
        return self.description

    def __str__(self):
        return self.get_fullname()


class SportType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TrainingInfo(models.Model):

    class Meta:
        verbose_name_plural = 'TrainingsInfo'

    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    WEEKDAYS = (
        (MONDAY, 'Понедельник'),
        (TUESDAY, 'Вторник'),
        (WEDNESDAY, 'Среда'),
        (THURSDAY, "Четверг"),
        (FRIDAY, "Пятница"),
        (SATURDAY, "Суббота"),
        (SUNDAY, "Воскресенье")
    )

    start_time = models.TimeField()
    duration = models.DurationField()
    weekdays = models.CharField(
        max_length=128,
        choices=WEEKDAYS,
    )
    end_time = models.TimeField()
    coach = models.ForeignKey(Coach, on_delete=models.PROTECT, null=True, blank=True)
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        end_time = datetime.combine(date(1, 1, 1), self.start_time) + self.duration
        self.end_time = end_time.time()

        super(TrainingInfo, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.coach.get_fullname()}, {self.sport_type.name}, {self.start_time}-{self.end_time}'


class ProfileImage(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=profile_photos)

    class Meta:
        verbose_name = 'Profile image'
        verbose_name_plural = 'Profile images'
