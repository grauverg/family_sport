from django.test import TestCase
from datetime import time

from schedule.models import Coach, SportType, TrainingInfo


class ModelsTestCase(TestCase):

    def setUp(self) -> None:
        self.sport_type1 = SportType.objects.create(
            name='Плавание'
        )

        self.coach1 = Coach.objects.create(
            first_name='Евгений',
            last_name='Петрашов',
            middle_name='Георгиевич',
            age=40,
            sport_coaching=self.sport_type1,
            short_description='Крутой тренер!',
            slug_field='petrashov',
            profile_image='coaches/petrashov/DSC00176.JPG'
        )

        self.training1 = TrainingInfo.objects.create(
            start_time=time(10, 0),
            duration=time(1, 30),
            weekdays=[
                TrainingInfo.MONDAY,
                TrainingInfo.WEDNESDAY,
                TrainingInfo.FRIDAY
            ],
            coach=self.coach1,
            sport_type=self.sport_type1
        )

    def test_create_sport_type(self):
        self.assertEqual(self.sport_type1.name, 'Плавание')
        self.assertEqual(self.sport_type1.slug_name, 'plavanie')

    def test_create_coach(self):
        self.assertEqual(self.coach1.first_name, 'Евгений')
        self.assertEqual(self.coach1.last_name, 'Петрашов')
        self.assertEqual(self.coach1.middle_name, 'Георгиевич')
        self.assertEqual(self.coach1.age, 40)
        self.assertEqual(self.coach1.short_description, "Крутой тренер!")
        self.assertIs(self.coach1.sport_coaching, self.sport_type1)
        self.assertEqual(self.coach1.slug_field, 'petrashov')

    def test_assert_equality_training_info(self):
        self.assertEqual(self.training1.start_time.strftime('%H:%M'), '10:00')
        self.assertEqual(self.training1.duration.hour, 1)
        self.assertEqual(self.training1.duration.minute, 30)
        self.assertEqual(self.training1.end_time.strftime('%H:%M'), '11:30')
        self.assertEqual(self.training1.weekdays[0], 'monday')
        self.assertEqual(self.training1.weekdays[1], 'wednesday')
        self.assertEqual(self.training1.weekdays[2], 'friday')
        self.assertIs(self.training1.coach, self.coach1)
        self.assertIs(self.training1.sport_type, self.sport_type1)
