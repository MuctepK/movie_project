from django.contrib import admin

# Register your models here.
from webapp.models import Movie, Genre, Actor, Director, MovieGenre, MovieDirection, MovieCast, Rating


class GenreInline(admin.TabularInline):
    model = MovieGenre
    extra = 1


class DirectorInline(admin.TabularInline):
    model = MovieDirection
    extra = 1


class ActorInline(admin.TabularInline):
    model = MovieCast
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'photo', 'duration', 'release_date', 'country']
    inlines = (GenreInline, DirectorInline, ActorInline)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Rating)