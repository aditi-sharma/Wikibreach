# __author__ = "Aditi Sharma"

from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

import markdown


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=6000)
    source_url = models.URLField(max_length=300)
    breach_date = models.DateField()
    create_user = models.ForeignKey(User, default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-create_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Post, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        super(Post, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_posts():
        posts = Post.objects.all()
        return posts

    def create_tags(self, tags):
        tags = tags.strip()
        tags = tags.strip('\"')
        tag_list = tags.split(',')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       post=self)

    def get_tags(self):
        return Tag.objects.filter(post=self)

    def get_source_url(self):
        return self.source_url

    def get_breach_date(self):
        return self.breach_date

    def get_summary(self):
        if len(self.content) > 255:
            return '{0}...'.format(self.content[:255])
        else:
            return self.title + self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = (('tag', 'post'),)
        index_together = [['tag', 'post'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.tag in count:
                count[tag.tag] += 1
            else:
                count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class UserPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=6000)
    source_url = models.URLField(max_length=300)
    breach_date = models.DateField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    username = models
    create_user = models.ForeignKey(User, default=1)

    tags = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "UserPost"
        verbose_name_plural = "UserPosts"
        ordering = ["-submitted_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(UserPost, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_user_posts():
        userposts = UserPost.objects.all()
        return userposts
