from django.contrib import admin

from .models import Post, Category

admin.site.site_header = 'پنل مدیریت وبلاگ حامد'


def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        verb = 'منتشر شد'
    else:
        verb = 'منتشر شدند'
    modeladmin.message_user(request, '{} پست {}.'.format(rows_updated, verb))


make_published.short_description = 'انتشار پست‌های انتخاب شده'


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        verb = 'پیش‌نویس شد'
    else:
        verb = 'پیش‌نویس شدند'
    modeladmin.message_user(request, '{} پست {}.'.format(rows_updated, verb))


make_draft.short_description = 'پیش‌نویس شدن پست‌های انتخاب شده'


def activate_category(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        verb = 'فعال شد'
    else:
        verb = 'فعال شدند'
    modeladmin.message_user(request, '{} دسته‌بندی {}.'.format(rows_updated, verb))


activate_category.short_description = 'فعال کردن دسته‌بندی‌های انتخاب شده'


def deactivate_category(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        verb = 'غیرفعال شد'
    else:
        verb = 'غیرفعال شدند'
    modeladmin.message_user(request, '{} دسته‌بندی {}.'.format(rows_updated, verb))


deactivate_category.short_description = 'غیرفعال کردن دسته‌بندی‌های انتخاب شده'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'parent', 'slug', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', 'position']
    actions = [activate_category, deactivate_category]


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'is_special', 'status', 'category_to_string')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']  # ordering posts in admin panel
    actions = [make_published, make_draft]


admin.site.register(Post, PostAdmin)
