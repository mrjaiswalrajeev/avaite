from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'email', 'phone_number')
    search_fields = ('name',)
    list_filter = ('gender',)
    ordering = ('id',)