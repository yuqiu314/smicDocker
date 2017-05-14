from django.contrib import admin

# Register your models here.
from .models import VisitCount, Employee, UploadData, UploadPPT
from .models import Choice, Poll, Vote, Article, VotedEmp

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chinesename', 'preferredname')
    search_fields=['id', 'chinesename'] 

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(VisitCount)

admin.site.register(UploadData)

admin.site.register(UploadPPT)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question',)
    search_fields = ['question',]

admin.site.register(Poll, PollAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('choice', 'comment',)
    
admin.site.register(Vote, VoteAdmin)

admin.site.register(Article)

admin.site.register(VotedEmp)