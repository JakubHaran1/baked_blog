from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AuthorModel(models.Model):
    name = models.CharField(max_length=15, verbose_name=("Imię"))
    second_name = models.CharField(max_length=25, verbose_name=("Nazwisko"))
    email = models.EmailField(max_length=254, verbose_name="Email")

    class Meta:
        verbose_name_plural = "Autorzy"

    def __str__(self):
        return f"{self.name} {self.second_name}"


class TagModel(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Tagi"

    def __str__(self):
        return f"{self.tag}"


class PostModel(models.Model):
    title = models.CharField(max_length=150, verbose_name="Tytuł:")
    author = models.ForeignKey(
        AuthorModel, verbose_name=("Autor:"), on_delete=models.CASCADE)
    slug = models.SlugField()
    date = models.DateField(auto_now_add=True, verbose_name="Data:")
    excerpt = models.TextField(verbose_name="skrót", validators=[
                               MinLengthValidator, MaxLengthValidator(250)])
    ingredients = models.TextField(
        validators=[MinLengthValidator(5)], verbose_name="Składniki:")

    ingredients = models.TextField(
        validators=[MinLengthValidator(5)], verbose_name="Składniki:", null=True)
    prepare = models.TextField(
        validators=[MinLengthValidator(5)], verbose_name="Sposób przygotowania:", null=True)
    image = models.ImageField(upload_to="dishes")
    tags = models.ManyToManyField(TagModel, verbose_name=("Tag:"))

    class Meta:
        verbose_name_plural = "Posty"

    def __str__(self) -> str:
        return f"{self.title}: {self.author}, {self.date}"


# Create your models here.
