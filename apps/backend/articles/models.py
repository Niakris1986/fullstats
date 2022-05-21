from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(models.Model):
    title = models.CharField(_('title article'), max_length=200)
    title_trans = models.CharField(_('title article'), max_length=200)
    article = models.IntegerField(_('article article'))
    preview = models.TextField(_('preview article'))
    author = models.ForeignKey(User, models.PROTECT, related_name='articles')
    body = models.TextField(_('body article'))
    short_summary = models.TextField(_('short summary article'))
    views = models.PositiveIntegerField(_('article views'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    article = models.ForeignKey(Article, models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class LikeChoices(models.IntegerChoices):
    POSITIVE = 1
    NEGATIVE = -1
    NEUTRAL = 0


class LikeArticle(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    article = models.ForeignKey(Article, models.CASCADE, related_name='likes')
    rating = models.IntegerField(
        _('article rating'),
        choices=LikeChoices.choices,
        default=LikeChoices.NEUTRAL.value
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
