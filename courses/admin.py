from django.contrib import admin

from courses.models import Product, Group, Lesson, GroupMembership


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    pass