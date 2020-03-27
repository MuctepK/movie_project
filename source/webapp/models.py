from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from pytils.translit import slugify


class Movie(models.Model):
    title = models.CharField(verbose_name='Название фильма', max_length=64)
    description = models.TextField(verbose_name='Описание фильма', max_length=2048)
    duration = models.PositiveIntegerField(verbose_name='Длительность фильма',
                                           validators=[MinValueValidator(5), MaxValueValidator(999)])
    release_date = models.DateField(verbose_name='Дата выхода')
    country = models.CharField(verbose_name='Страна выпуска', max_length=5)
    photo = models.ImageField(verbose_name='Постер к фильму', upload_to='movie_images')



    def get_genres(self):
        return [genre.genre for genre in self.genres.all()]

    def get_rating(self):
        reviews = self.reviews_taken.all()
        if reviews:
            return sum([review.rating for review in reviews])/(len(reviews))
        return 0

    def get_actors(self):
        return [actor.actor for actor in self.acted_by.all()]

    def get_directors(self):
        return [director.director for director in self.directed_by.all()]

    def __str__(self):
        return self.title

    def short_description(self):
        return "{}....".format(self.description[:128])

    def year(self):
        return self.release_date.year

    def is_new(self):
        return datetime.now().year - self.year() <= 2


class Genre(models.Model):
    title = models.CharField(verbose_name='Название жанра', max_length=32)
    slug = models.SlugField(verbose_name='Идентификация', editable=True, null=True)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='Связь к фильму', on_delete=models.CASCADE, related_name='genres')
    genre = models.ForeignKey(Genre, verbose_name='Связь к жанру', on_delete=models.CASCADE, related_name='movies')


class Rating(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='Связь к фильму', on_delete=models.CASCADE, related_name='reviews_taken')
    reviewer = models.ForeignKey('auth.User', verbose_name='Связь к пользователю', on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.PositiveIntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(100)])
    text = models.TextField(verbose_name='Текст отзыва',max_length=1024, default='-')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',)
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')


class Director(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)
    patronymic = models.CharField(verbose_name='Отчество', max_length=64, null=True, blank=True)
    biography = models.TextField(verbose_name='Биография', max_length=2048)
    photo = models.ImageField(verbose_name='Фото', upload_to='director_images', null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class MovieDirection(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='Связь к фильму', on_delete=models.CASCADE, related_name='directed_by')
    director = models.ForeignKey(Director, verbose_name='Связь к режиссеру', on_delete=models.CASCADE, related_name='directed_at')


ACTOR_GENDER_CHOICES = [
    ('M', 'Мужской'),
    ('F', 'Женский')
]


class Actor(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)
    patronymic = models.CharField(verbose_name='Отчество', max_length=64, null=True, blank=True)
    biography = models.TextField(verbose_name='Биография', max_length=2048)
    photo = models.ImageField(verbose_name='Фото', upload_to='actor_images', null=True, blank=True)
    gender = models.CharField(verbose_name='Пол', choices=ACTOR_GENDER_CHOICES, default=ACTOR_GENDER_CHOICES[0][0], max_length=1)
    birth_date = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name, )


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='Связь к фильму', on_delete=models.CASCADE, related_name='acted_by')
    actor = models.ForeignKey(Actor, verbose_name='Связь к автору', on_delete=models.CASCADE, related_name='acted_at')