from django.contrib import admin
from .models import Status, Type, Category, SubCategory, CashFlow



@admin.register(CashFlow)
class CashflowRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "type", "category", "subcategory", "amount")
    list_filter = ("status", "type", "category")
    search_fields = ("comment",)