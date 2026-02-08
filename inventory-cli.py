#!/usr/bin/env python3
"""
Inventory Manager - CSV-based local database
Inspired by Wine Cellar Skill from OpenClaw community
"""
import os
import csv
import json
from datetime import datetime
from pathlib import Path

class InventoryManager:
    def __init__(self, csv_file=None):
        if csv_file is None:
            csv_file = os.path.expanduser("~/projects/inventory-manager/inventory.csv")
        else:
            csv_file = os.path.expanduser(csv_file)
        self.csv_file = csv_file
        self.fields = ["id", "name", "category", "quantity", "location", "date_added", "notes"]
        self._ensure_file()
        
    def _ensure_file(self):
        """Create CSV if doesn't exist"""
        try:
            with open(self.csv_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
    
    def add(self, name, category, quantity=1, location="default", notes=""):
        """Add item to inventory"""
        import random
        item_id = random.randint(1000, 9999)
        date = datetime.now().isoformat()
        
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writerow({
                "id": item_id,
                "name": name,
                "category": category,
                "quantity": quantity,
                "location": location,
                "date_added": date,
                "notes": notes
            })
        return {"status": "added", "id": item_id, "name": name}
    
    def list(self, category=None, low_stock=False):
        """List inventory items"""
        items = []
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if category and row["category"] != category:
                    continue
                if low_stock and int(row["quantity"]) > 2:
                    continue
                items.append(row)
        return items
    
    def search(self, query):
        """Search inventory"""
        results = []
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if query.lower() in row["name"].lower() or query.lower() in row["notes"].lower():
                    results.append(row)
        return results
    
    def summary(self):
        """Get inventory summary"""
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
        
        by_category = {}
        total_items = 0
        for item in items:
            cat = item["category"]
            qty = int(item["quantity"])
            by_category[cat] = by_category.get(cat, 0) + qty
            total_items += qty
        
        return {
            "total_items": total_items,
            "categories": len(by_category),
            "by_category": by_category,
            "items": items[:5]  # First 5 items
        }

# Demo
inv = InventoryManager()  # Uses default path

print("🍷 INVENTORY MANAGER")
print("="*50)

# Add sample items
inv.add("Opus One 2019", "Wine", 3, "Cellar A", "Premium Napa")
inv.add("PGA Tour Merchandise", "Apparel", 12, "Shelf 1", "Various")
inv.add("Titleist Pro V1", "Golf", 2, "Bag", "Practice balls")
inv.add("Kirkland Signature Vodka", "Spirits", 1, "Bar", "For guests")

# Summary
summary = inv.summary()
print(f"\n📊 SUMMARY")
print(f"  Total Items: {summary['total_items']}")
print(f"  Categories: {summary['categories']}")
for cat, qty in summary["by_category"].items():
    print(f"    - {cat}: {qty}")

print(f"\n🔍 SEARCH 'wine':")
for item in inv.search("wine"):
    print(f"  - {item['name']} ({item['quantity']}x) - {item['notes']}")

print(f"\n🍷 ALL ITEMS:")
for item in inv.list():
    print(f"  {item['name']} - {item['quantity']}x ({item['location']})")
