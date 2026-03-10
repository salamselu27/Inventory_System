from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class ItemMaster(models.Model):
    TYPE_CHOICES = [
        ('RM', 'Raw Material'),
        ('FG', 'Finished Good'),
    ]
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    item_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='RM')
    unit = models.CharField(max_length=50, default='kg')
    
    # Stock details
    current_stock = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    avg_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    
    # Specifics
    # Sack Size for FG: H x W x L. Stores as JSON {h: val, w: val, l: val}
    sack_size = models.JSONField(blank=True, null=True) 
    
    # For RM: Blending vs Packing toggle
    USAGE_CHOICES = [
        ('Blending', 'Blending'),
        ('Packing', 'Packing'),
    ]
    usage_type = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()})"

class BOMItem(models.Model):
    """Bill of Materials: Defines how much RM is needed for 1 unit of FG"""
    finished_good = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='bom_items')
    raw_material = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='used_in_bom')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, help_text="Quantity of RM per 1 unit of FG")
    
    def __str__(self):
        return f"{self.raw_material.name} for {self.finished_good.name}"

class Transaction(models.Model):
    TXN_TYPE_CHOICES = [
        ('IN', 'Inward'),
        ('OUT', 'Outward'),
        ('ADJ', 'Adjustment'),
    ]
    
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='transactions')
    txn_type = models.CharField(max_length=3, choices=TXN_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_txn_type_display()} - {self.item.name} - {self.quantity}"

class JobCard(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('COMPLETED', 'Completed'),
    ]
    
    finished_good = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, limit_choices_to={'item_type': 'FG'})
    quantity_produced = models.DecimalField(max_digits=12, decimal_places=3)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    
    # Snapshot of RM usage
    rm_usage_snapshot = models.JSONField(help_text="Snapshot of RMs used and their quantities", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job #{self.id} - {self.finished_good.name}"
