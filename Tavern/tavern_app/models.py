from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


NUMBER_OF_PLAYERS_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
)

DIFFICULTY_CHOICES = (
    ("Pokojowa", "Pokojowa"),
    ("Zrównoważona", "Zrównoważona"),
    ("Niebezpieczna", "Niebezpieczna"),
    ("Śmiertelnie groźna", "Śmiertelnie groźna")
)

ADULT_CHOICES = (
    ("TAK", "TAK"),
    ("NIE", "NIE")
)


class MasterSession(models.Model):
    #Owner is always going to be a logged user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=150, blank=False, verbose_name="Tytuł sesji")
    date = models.DateField(blank=False, verbose_name="Data sesji")
    time = models.TimeField(blank=False, verbose_name="Godzina sesji")
    counter_of_players = models.IntegerField(default=0)
    number_of_players = models.IntegerField(choices=NUMBER_OF_PLAYERS_CHOICES, blank=False, verbose_name="Liczba poszukiwanych graczy")
    description = models.TextField(blank=False, verbose_name="Opis sesji")
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, blank=False, verbose_name="Poziom trudności przygody")
    adult_only = models.CharField(max_length=50, choices= ADULT_CHOICES, blank=False, verbose_name="Sesja tylko dla dorosłych")
    other_requirements = models.TextField(blank=False, verbose_name="Inne wymagania")

    def add_user_to_list_of_attendeesMS(self, user):
        registration = MasterSessionRegistration.objects.create(user=user,
                                                                session=self)

    def remove_user_from_list_of_attendeesMS(self, user):
        registration = MasterSessionRegistration.objects.get(user=user,
                                                             session=self)
        registration.delete()


class MasterSessionRegistration(models.Model):
    session = models.ForeignKey(MasterSession, verbose_name='Sesja', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Uczestnik', on_delete=models.CASCADE)


class GamerSession(models.Model):
    #Owner is always going to be a logged user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=150, blank=False, verbose_name="Tytuł sesji")
    date = models.DateField(blank=False, verbose_name="Data sesji")
    time = models.TimeField(blank=False, verbose_name="Godzina sesji")
    description = models.TextField(blank=False, verbose_name="Opis sesji")
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, blank=False, verbose_name="Oczekiwany poziom trudności przygody")
    adult_only = models.CharField(max_length=50, choices=ADULT_CHOICES, blank=False, verbose_name="Sesja tylko dla dorosłych")
    master_requirements = models.TextField(blank=False, verbose_name="Wymagania dotyczące mistrza gry")
    other_requirements = models.TextField(blank=False, verbose_name="Inne wymagania")
    is_master_chosen = models.BooleanField(default=False)

    def add_user_to_list_of_attendeesGS(self, user):
        registration = GamerSessionRegistration.objects.create(user=user,
                                                               session=self)

    def remove_user_from_list_of_attendeesGS(self, user):
        registration = GamerSessionRegistration.objects.get(user=user,
                                                            session=self)
        registration.delete()


class GamerSessionRegistration(models.Model):
    session = models.ForeignKey(GamerSession, verbose_name='Sesja', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Uczestnik', on_delete=models.CASCADE)


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
