from django.contrib import admin
from .models import ItemMaster, Transaction, JobCard, BOMItem

class BOMItemInline(admin.TabularInline):
    model = BOMItem
    fk_name = 'finished_good'
    extra = 1
    autocomplete_fields = ['raw_material']

@admin.register(ItemMaster)
class ItemMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'current_stock', 'unit', 'avg_rate')
    search_fields = ('name', 'code')
    list_filter = ('item_type',)
    inlines = [BOMItemInline]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'txn_type', 'item', 'quantity', 'created_at')
    list_filter = ('txn_type', 'date')
    search_fields = ('item__name', 'reference_number')

@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'finished_good', 'quantity_produced', 'status', 'date')
    list_filter = ('status', 'date')
