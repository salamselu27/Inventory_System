import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from inventory.models import ItemMaster, BOMItem, Transaction

def seed():
    # 1. Create Raw Materials (RM)
    rm_items = [
        {'name': 'Raw Material A', 'unit': 'kg', 'current_stock': 500, 'reorder_level': 100, 'usage_type': 'Blending'},
        {'name': 'Raw Material B', 'unit': 'kg', 'current_stock': 300, 'reorder_level': 50, 'usage_type': 'Blending'},
        {'name': 'Packing Box', 'unit': 'pcs', 'current_stock': 1000, 'reorder_level': 200, 'usage_type': 'Packing'},
    ]
    
    rm_objs = []
    for rm in rm_items:
        obj, created = ItemMaster.objects.get_or_create(
            name=rm['name'],
            item_type='RM',
            defaults={
                'unit': rm['unit'],
                'current_stock': rm['current_stock'],
                'reorder_level': rm['reorder_level'],
                'usage_type': rm['usage_type']
            }
        )
        rm_objs.append(obj)
        if created:
            Transaction.objects.create(
                item=obj,
                txn_type='IN',
                quantity=rm['current_stock'],
                notes='Initial Seed Stock'
            )
            print(f"Created RM: {obj.name}")

    # 2. Create Finished Goods (FG)
    fg_items = [
        {'name': 'Finished Product X', 'unit': 'boxes', 'current_stock': 50, 'reorder_level': 10, 'sack_size': {'h': 10, 'w': 20, 'l': 30}},
        {'name': 'Finished Product Y', 'unit': 'boxes', 'current_stock': 20, 'reorder_level': 5, 'sack_size': {'h': 15, 'w': 25, 'l': 35}},
    ]
    
    fg_objs = []
    for fg in fg_items:
        obj, created = ItemMaster.objects.get_or_create(
            name=fg['name'],
            item_type='FG',
            defaults={
                'unit': fg['unit'],
                'current_stock': fg['current_stock'],
                'reorder_level': fg['reorder_level'],
                'sack_size': fg['sack_size']
            }
        )
        fg_objs.append(obj)
        if created:
            Transaction.objects.create(
                item=obj,
                txn_type='IN',
                quantity=fg['current_stock'],
                notes='Initial Seed Stock'
            )
            print(f"Created FG: {obj.name}")

    # 3. Create BOM (Bill of Materials)
    # Product X needs 2kg RM A and 1kg RM B and 1 Box
    bom_data = [
        (fg_objs[0], rm_objs[0], 2.0),
        (fg_objs[0], rm_objs[1], 1.0),
        (fg_objs[0], rm_objs[2], 1.0),
        # Product Y needs 1kg RM A and 3kg RM B
        (fg_objs[1], rm_objs[0], 1.0),
        (fg_objs[1], rm_objs[1], 3.0),
    ]
    
    for fg, rm, qty in bom_data:
        BOMItem.objects.get_or_create(
            finished_good=fg,
            raw_material=rm,
            defaults={'quantity': qty}
        )
        print(f"Added BOM: {rm.name} for {fg.name}")

if __name__ == '__main__':
    seed()
    print("Seeding complete.")
