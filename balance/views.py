from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from inventory.models import ItemMaster, Transaction, JobCard
from django.utils import timezone
from datetime import timedelta
import json

def shipment_planner(request):
    # Get all FG items with sack sizes
    fg_items = ItemMaster.objects.filter(item_type='FG').exclude(sack_size__isnull=True)
    
    # Pre-calculate CBM for each to pass to the frontend
    items_data = []
    for item in fg_items:
        if item.sack_size and isinstance(item.sack_size, dict):
            h = float(item.sack_size.get('h', 0))
            w = float(item.sack_size.get('w', 0))
            l = float(item.sack_size.get('l', 0))
            
            # CBM = (L x W x H in cm) / 1,000,000
            if h and w and l:
                cbm = (h * w * l) / 1000000.0
                items_data.append({
                    'id': item.id,
                    'name': item.name,
                    'h': h,
                    'w': w,
                    'l': l,
                    'cbm': round(cbm, 4)
                })
                
    context = {
        'items_json': json.dumps(items_data),
        'items': items_data
    }
    return render(request, 'balance/shipment_planner.html', context)

def insights(request):
    # 1. Inventory Valuation
    rm_value = ItemMaster.objects.filter(item_type='RM').aggregate(
        total=Sum(ExpressionWrapper(F('current_stock') * F('avg_rate'), output_field=DecimalField()))
    )['total'] or 0

    fg_value = ItemMaster.objects.filter(item_type='FG').aggregate(
        total=Sum(ExpressionWrapper(F('current_stock') * F('avg_rate'), output_field=DecimalField()))
    )['total'] or 0

    # 2. Transaction Summaries (Last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_txns = Transaction.objects.filter(date__gte=thirty_days_ago)
    
    inward_qty = recent_txns.filter(txn_type='IN').aggregate(total=Sum('quantity'))['total'] or 0
    outward_qty = recent_txns.filter(txn_type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
    
    # 3. Production Summary
    recent_jobs = JobCard.objects.filter(date__gte=thirty_days_ago, status='COMPLETED')
    fg_produced = recent_jobs.aggregate(total=Sum('quantity_produced'))['total'] or 0
    
    context = {
        'rm_value': rm_value,
        'fg_value': fg_value,
        'total_inventory_value': rm_value + fg_value,
        'inward_qty': inward_qty,
        'outward_qty': outward_qty,
        'fg_produced': fg_produced,
        'recent_jobs_count': recent_jobs.count(),
    }
    return render(request, 'balance/insights.html', context)
