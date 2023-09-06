from django.db import models
from datetime import datetime, date
from django.utils.html import mark_safe
from PIL import Image

from transliterate import slugify
from django.utils.translation import gettext as _


def profile_photo(instance, filename):
    return f'coaches/{instance.slug_field}/{filename}'


def profile_photos(instance, filename):
    return f'coaches/{instance.coach.slug_field}/{filename}'


def sport_images(instance, filename):
    return f'sport_type/{instance.slug_field}/{filename}'


class Coach(models.Model):
    class Meta:
        verbose_name = "Coach"
        verbose_name_plural = 'Coaches'

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)

    profile_image = models.ImageField(upload_to=profile_photo, default='coaches/default/')

    age = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    sport_coaching = models.ForeignKey('SportType', on_delete=models.PROTECT)

    slug_field = models.SlugField(default='', null=False, blank=True, max_length=20)

    def save(self, *args, **kwargs):
        self.slug_field = slugify(self.last_name)

        image = Image.open(self.profile_image.url)
        width, height = image.size
        if width > 1000 & height > 800:
            image.resize(size=(width // 2, height // 2))
        image.save(f'{self.profile_image.url}', optimize=True)

        super().save(*args, **kwargs)

    def image_tag(self):
        if self.profile_image:
            return mark_safe(
                f"<img src='{self.profile_image.url}' width='250' margin='1' />"
            )
        return 'No image'
    image_tag.short_description = 'Image'

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
    slug_field = models.SlugField(default='', null=False, blank=True, max_length=20)
    description = models.TextField(blank=True)

    main_image = models.ImageField(upload_to=sport_images)

    def get_short_description(self):
        if len(f'{self.description}') > 30:
            return f'{self.description[:30]}...'
        return self.description

    def save(self, *args, **kwargs):
        self.slug_field = slugify(self.name)
        super().save(*args, **kwargs)

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
        (MONDAY, _('Понедельник')),
        (TUESDAY, _('Вторник')),
        (WEDNESDAY, _('Среда')),
        (THURSDAY, _("Четверг")),
        (FRIDAY, _("Пятница")),
        (SATURDAY, _("Суббота")),
        (SUNDAY, _("Воскресенье"))
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

    def __str__(self):
        return self.image

    def save(self, **kwargs):
        current = self.ProfileImage(id=self.id)
        if current.image != self.image:
            current.image.delete()
        super(ProfileImage, self).save(**kwargs)


class SportImages(models.Model):
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=sport_images)
