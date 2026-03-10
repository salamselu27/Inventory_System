from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import ItemMaster, JobCard, BOMItem, Transaction

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        item_type = request.POST.get('item_type')
        unit = request.POST.get('unit')
        reorder_level = request.POST.get('reorder_level')
        
        # Handle Dynamic Logic
        sack_size = None
        usage_type = None
        
        if item_type == 'FG':
            # Collect JSON HxWxL
            h = request.POST.get('sack_h')
            w = request.POST.get('sack_w')
            l = request.POST.get('sack_l')
            if h and w and l:
                sack_size = {'h': h, 'w': w, 'l': l}
        elif item_type == 'RM':
            usage_type = request.POST.get('usage_type')
            
        ItemMaster.objects.create(
            name=name,
            item_type=item_type,
            unit=unit,
            reorder_level=reorder_level or 0,
            sack_size=sack_size,
            usage_type=usage_type
        )
        messages.success(request, f"Item '{name}' registered successfully.")
        return redirect('add_item')
        
    return render(request, 'inventory/item_form.html')

def entry_hub(request):
    return render(request, 'inventory/entry_hub.html')

def create_job_card(request):
    if request.method == 'POST':
        step = request.POST.get('step')
        
        if step == '1':
            # Calculate RM
            fg_id = request.POST.get('finished_good')
            qty = float(request.POST.get('quantity'))
            
            fg_item = ItemMaster.objects.get(id=fg_id)
            bom_items = BOMItem.objects.filter(finished_good=fg_item)
            
            rm_data = []
            for bom in bom_items:
                # Use Decimal for precision if possible, but float is easier for prototype
                req_qty = float(bom.quantity) * qty
                rm_data.append({
                    'id': bom.raw_material.id,
                    'name': bom.raw_material.name,
                    'unit': bom.raw_material.unit,
                    'stock': bom.raw_material.current_stock,
                    'required': req_qty
                })
            
            return render(request, 'inventory/job_card_form.html', {
                'step': 2,
                'fg': fg_item,
                'quantity': qty,
                'rm_data': rm_data,
                'fgs': ItemMaster.objects.filter(item_type='FG')
            })
            
        elif step == '2':
            # Create Job Card and Update Stock
            fg_id = request.POST.get('fg_id')
            qty = float(request.POST.get('quantity'))
            rm_ids = request.POST.getlist('rm_id')
            rm_quantities = request.POST.getlist('rm_quantity')
            
            fg_item = ItemMaster.objects.get(id=fg_id)
            
            try:
                with transaction.atomic():
                    # 1. Create Job Card
                    job = JobCard.objects.create(
                        finished_good=fg_item,
                        quantity_produced=qty,
                        status='COMPLETED'
                    )
                    
                    rm_snapshot = []
                    
                    # 2. Deduct RMs
                    for r_id, r_qty in zip(rm_ids, rm_quantities):
                        rm_item = ItemMaster.objects.get(id=r_id)
                        actual_qty = float(r_qty)
                        
                        # Update Stock
                        rm_item.current_stock = float(rm_item.current_stock) - actual_qty
                        rm_item.save()
                        
                        # Create Transaction
                        Transaction.objects.create(
                            item=rm_item,
                            txn_type='OUT',
                            quantity=actual_qty,
                            reference_number=f"JOB-{job.id}",
                            notes=f"Used for {fg_item.name}"
                        )
                        
                        rm_snapshot.append({'name': rm_item.name, 'qty': actual_qty})
                    
                    # 3. Increase FG Stock
                    fg_item.current_stock = float(fg_item.current_stock) + qty
                    fg_item.save()
                    
                    Transaction.objects.create(
                        item=fg_item,
                        txn_type='IN',
                        quantity=qty,
                        reference_number=f"JOB-{job.id}",
                        notes="Production Output"
                    )
                    
                    job.rm_usage_snapshot = rm_snapshot
                    job.save()
                    
                    messages.success(request, f"Job Card #{job.id} created. Stock updated.")
                    return redirect('entry_hub')
                    
            except Exception as e:
                messages.error(request, f"Error creating Job Card: {str(e)}")
                return redirect('create_job_card')

    fgs = ItemMaster.objects.filter(item_type='FG')
    return render(request, 'inventory/job_card_form.html', {'step': 1, 'fgs': fgs})

def inventory_logs(request):
    transactions = Transaction.objects.all().order_by('-date', '-created_at')
    return render(request, 'inventory/inventory_logs.html', {'transactions': transactions})

def stock_alerts(request):
    # Filter items where stock is below or equal to reorder level
    from django.db.models import F
    low_stock_items = ItemMaster.objects.filter(current_stock__lte=F('reorder_level'))
    return render(request, 'inventory/stock_alerts.html', {'items': low_stock_items})

def live_stock(request):
    items = ItemMaster.objects.all().order_by('name')
    return render(request, 'inventory/live_stock.html', {'items': items})
