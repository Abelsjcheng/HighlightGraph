from django.contrib import admin
from backend import models

# Register your models here.


class UsernameAdmin(admin.ModelAdmin):
    list_display = ('username', 'sex', 'age', 'education', 'research', 'background')
    search_fields = ('username', 'sex', 'age', 'education', 'research', 'background')


class DurationAdmin(admin.ModelAdmin):
    list_display = ('did', 'time', 'name', 'consumingtime', 'username')
    search_fields = ('did', 'time', 'name', 'consumingtime')


class RectangleAdmin(admin.ModelAdmin):
    list_display = ('rid', 'time', 'name', 'x1', 'y1', 'x2', 'y2', 'username', 'duration')
    search_fields = ('rid', 'time', 'name', 'x1', 'y1', 'x2', 'y2')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('qid', 'type', 'name', 'content', 'choices', 'questionImg', 'background', 'TestType')
    search_fields = ('qid', 'type', 'name', 'content', 'choices', 'questionImg', 'background', 'TestType')


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('rid', 'time', 'name', 'x1', 'y1', 'x2', 'y2', 'answer', 'TestType', 'qid', 'username', 'consumingtime')
    search_fields = ('rid', 'time', 'name', 'x1', 'y1', 'x2', 'y2', 'answer', 'TestType', 'qid')


class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('bid', 'name', 'background', 'label', 'graphname')
    search_fields = ('bid', 'name', 'background', 'label', 'graphname')


admin.site.register(models.Username, UsernameAdmin)
admin.site.register(models.Duration, DurationAdmin)
admin.site.register(models.Rectangle, RectangleAdmin)
admin.site.register(models.Questions, QuestionsAdmin)
admin.site.register(models.Answers, AnswersAdmin)
admin.site.register(models.Background, BackgroundAdmin)
