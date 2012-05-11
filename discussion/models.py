import os

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, time
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


from notification import models as notification


class Discussion(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/discussions', max_length=255, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('discussion', [self.slug])

    @property
    def notification_label(self):
        return "discussion_remind_%s" % self.slug

    @property
    def notification_display(self):
        return ("Reminder for %s." % self.name)[:50]

    @property
    def notice_type(self):
        """
            Return the notice type for this discussion.
            If it does not exist then the notice type will be created.
        """
        self.create_notice_type()
        return notification.NoticeType.objects.get(label=self.notification_label)

    def create_notice_type(self):
        """Create (or update) a notice type for discussion instance ."""
        notification.create_notice_type(self.notification_label, self.notification_display, "A new post has been added .", default=0)

@receiver(post_save, sender=Discussion)
def create_discussion_notice_type(sender, instance, **kwargs):
    # If display or diary title has changed notification details will be updated or created for new diary.
    instance.create_notice_type()

@receiver(pre_delete, sender=Discussion)
def delete_discussion_notice_type(sender, instance, **kwargs):
    instance.notice_type.delete()


class Post(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    body = models.TextField()
    attachment = models.FileField(upload_to='uploads/posts', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time',)

    def __unicode__(self):
        return 'Post by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )

    @models.permalink
    def get_absolute_url(self):
        return ('discussion_post', [self.discussion.slug, str(self.id)])

    @property
    def attachment_filename(self):
        return self.attachment and os.path.basename(self.attachment.name)

    @property
    def prefix(self):
        return 'post-%d' % (self.pk or 0,)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    body = models.TextField()
    attachment = models.FileField(upload_to='uploads/comments',
                                    blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    @property
    def attachment_filename(self):
        return self.attachment and os.path.basename(self.attachment.name)

    class Meta:
        ordering = ('time',)

    def __unicode__(self):
        return 'Comment by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )

def comment_notifications(sender, created, **kwargs):
    from django.contrib.auth.models import User
    user = User.objects.get(pk=1)
    if notification and created:
        notification.send([user], 'discussion_comment_save', {'user': ''})
models.signals.post_save.connect(comment_notifications, sender=Comment)

