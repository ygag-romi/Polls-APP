from django.contrib import admin
from .models import Question, Choice, Comment, Tag
from polls.forms import VerifyChoiceForm, VerifyTagForm


class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'question', 'email', 'created')
    list_filter = ('active', 'created')
    search_fields = ('email', 'body')


class TagsInLine(admin.TabularInline):
    model = Question.question_tags.through
    extra = 3


class TagsAdmin(admin.ModelAdmin):
    form = VerifyTagForm
    list_display = ('tag',)


class ChoiceInLine(admin.TabularInline):
    model = Choice
    form = VerifyChoiceForm
    extra = 3


class ChoiceAdmin(admin.ModelAdmin):
    form = VerifyChoiceForm
    list_display = ('choice_text', 'question')


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Your Questions', {'fields': ['question_text']}),
        ('', {'fields': ['created_by']}),
        ('Date Info', {'fields': ['pub_date']}),
        ('Expiry Details', {'fields': ['expiry', 'closed']}),
        ('Sort Priority', {'fields': ['priority']}),
    ]
    inlines = [ChoiceInLine, CommentInLine, TagsInLine]
    list_display = (
        'question_text', 'pub_date', 'was_published_recently', 'created_by',
        'choices', 'related_tags', 'priority')
    search_fields = ['question_text']

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def related_tags(self, obj):
        new_list = []
        for tag in obj.question_tags.all():
            if tag not in new_list:
                new_list.append(tag)

        return new_list


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Tag, TagsAdmin)
