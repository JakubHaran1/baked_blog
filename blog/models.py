from django.db import models
from django.core.validators import MinLengthValidator


class AuthorModel(models.Model):
    name = models.CharField(max_length=15)
    second_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} {self.second_name}"


class TagModel(models.Model):
    tag = models.CharField(max_length=50)


class PostModel(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        AuthorModel, verbose_name=("autor"), on_delete=models.CASCADE)
    slug = models.SlugField()
    date = models.DateField(auto_now_add=True)
    excerpt = models.CharField(max_length=250)
    content = models.TextField(validators=[MinLengthValidator(5)])
    image = models.ImageField(upload_to=None)
    tags = models.ManyToManyField(TagModel, verbose_name=("tag"))

    def __str__(self) -> str:
        return f"{self.title}: {self.author}, {self.date}"


# Create your models here.
