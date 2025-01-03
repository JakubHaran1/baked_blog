from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager


class TagModel(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Tagi"

    def __str__(self):
        return f"{self.tag}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_field):
        if not email or not username or not password:
            raise ValueError("Błąd danych!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_field)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_field)


class CustomUserModel(AbstractUser):
    username = models.CharField(
        verbose_name="Nazwa użytkownika", max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    is_verficated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name="Personel:")
    is_superuser = models.BooleanField(default=False,)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class PostModel(models.Model):
    title = models.CharField(max_length=150, verbose_name="Tytuł:")
    author = models.ForeignKey(
        CustomUserModel, verbose_name=("Autor:"), on_delete=models.CASCADE)
    slug = models.SlugField(primary_key=True)
    date = models.DateField(auto_now_add=True, verbose_name="Data:")
    excerpt = models.TextField(verbose_name="skrót", validators=[
                               MinLengthValidator, MaxLengthValidator(250)])

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


class UserCommentModel(models.Model):
    user = models.ForeignKey(
        CustomUserModel, verbose_name="Użytkownik:", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Treść:", null=False)
    post = models.ForeignKey(
        PostModel, verbose_name="Post:", on_delete=models.CASCADE, related_name="comments")

    class Meta:
        verbose_name_plural = "Komentarze"

    def __str__(self):
        return f"{self.user} | komentuje: {self.post.title}"
