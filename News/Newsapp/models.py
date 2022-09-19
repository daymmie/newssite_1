
from django.contrib.auth.models import User
from django.db import models


article = 'AR'
news = 'NW'

POSITIONS = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.author_rating = 0
        for post in Post.post_rating.validators:
            self.author_rating += post * 3
        for comment in Comment.comment_rating.validators:
            self.author_rating += comment
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=2,
                                   choices=POSITIONS,
                                   default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=30)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        post_preview = self.post_text[0:125] + '...'
        return f'{post_preview}'

    def like(self, amount=1):
        self.post_rating += amount
        self.save()

    def dislike(self, amount=1):
        self.post_rating -= amount
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self, amount=1):
        self.comment_rating += amount
        self.save()

    def dislike(self, amount=1):
        self.comment_rating -= amount
        self.save()
