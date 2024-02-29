from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_group_users = models.IntegerField()
    max_group_users = models.IntegerField()

    @classmethod
    def already_subscribed(cls, user):
        return cls.objects.filter(group__groupmembership__user=user).exists()

    def subscribe(self, user):
        if self.already_subscribed(user):
            return 'Вы уже записаны на этот продукт'

        groups = Group.objects.filter(product=self)

        if not groups or self.start_date < timezone.now():
            return 'На данный момент нет групп c датой старта в ближайшее время'

        sorted_groups = sorted(
            groups,
            key=lambda group: group.groupmembership_set.count()
        )

        for group in sorted_groups:
            if group.groupmembership_set.count() < self.max_group_users:
                GroupMembership.objects.create(user=user, group=group)
                break
        else:
            return 'Все группы набиты битком'


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_link = models.URLField()
