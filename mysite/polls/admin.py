from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Questions',                   {'fields': ['question']}),
        ("Choice text",              {'fields': ['choice_text']}),
        ('Votes', {'fields': ['votes'], 'classes': ['collapse']}),
    ]
    list_display = ('choice_text', 'votes', 'question')


admin.site.register(Choice, ChoiceAdmin)
