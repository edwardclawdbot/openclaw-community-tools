#!/usr/bin/env python3
"""
Shopping Automation - Weekly Meal Planning to Order
Inspired by Tesco Shop Autopilot from OpenClaw community
"""
import json

class ShoppingAutopilot:
    def __init__(self):
        self.cart = []
        self.meal_plan = []
        
    def add_meal(self, meal_name, ingredients):
        """Add a meal to the plan"""
        self.meal_plan.append({
            "meal": meal_name,
            "ingredients": ingredients
        })
        
    def generate_shopping_list(self):
        """Convert meal plan to consolidated shopping list"""
        consolidated = {}
        
        for meal in self.meal_plan:
            for item in meal["ingredients"]:
                if item["name"] in consolidated:
                    consolidated[item["name"]]["quantity"] += item["quantity"]
                else:
                    consolidated[item["name"]] = item.copy()
        
        return consolidated
    
    def add_to_cart(self, item_name, quantity=1, store="Amazon Fresh"):
        """Add item to cart"""
        self.cart.append({
            "item": item_name,
            "quantity": quantity,
            "store": store,
            "status": "pending"
        })
        
    def checkout(self):
        """Simulate checkout process"""
        total = len(self.cart)
        return {
            "status": "ready_to_checkout",
            "items": total,
            "stores": list(set([item["store"] for item in self.cart]))
        }

# Demo
autopilot = ShoppingAutopilot()

# Add weekly meals
autopilot.add_meal("Tacos", [
    {"name": "Ground Beef", "quantity": 1, "unit": "lb"},
    {"name": "Taco Shells", "quantity": 1, "unit": "box"},
    {"name": "Cheese", "quantity": 1, "unit": "block"},
    {"name": "Salsa", "quantity": 1, "unit": "jar"}
])

autopilot.add_meal("Pasta", [
    {"name": "Spaghetti", "quantity": 1, "unit": "box"},
    {"name": "Marinara Sauce", "quantity": 2, "unit": "jars"},
    {"name": "Parmesan", "quantity": 1, "unit": "block"}
])

# Generate shopping list
shopping_list = autopilot.generate_shopping_list()
print("📋 SHOPPING LIST")
print("="*40)
for item, details in shopping_list.items():
    print(f"  {item}: {details['quantity']} {details.get('unit', '')}")

print("\n🛒 CART STATUS")
cart_status = autopilot.checkout()
print(f"  Items: {cart_status['items']}")
print(f"  Stores: {cart_status['stores']}")
