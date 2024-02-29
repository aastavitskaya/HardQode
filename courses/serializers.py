from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Lesson, GroupMembership


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'price', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_link']


class ProductStatsSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    avg_group_fill_percentage = serializers.SerializerMethodField()
    acquisition_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'price', 'students_count', 'avg_group_fill_percentage']

    def get_students_count(self, obj):
        return GroupMembership.objects.filter(group__product=obj).count()

    def get_avg_group_fill_percentage(self, obj):
        groups = obj.group_set.all()
        total_groups = groups.count()
        if total_groups == 0:
            return 0

        total_fill_percentage = sum(
            (group.groupmembership_set.count() / obj.max_group_users) * 100 for group in groups
        )

        return round(total_fill_percentage / total_groups, 2)

    def get_acquisition_percentage(self, obj):
        return round(GroupMembership.objects.filter(group__product=obj).count() * 100 / User.objects.count(), 2)
