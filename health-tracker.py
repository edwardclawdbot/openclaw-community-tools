#!/usr/bin/env python3
"""
Health Dashboard - Calendar + Fitness Integration
Inspired by Oura Ring Health Assistant from OpenClaw community
"""
import json
from datetime import datetime, timedelta

class HealthDashboard:
    def __init__(self):
        self.metrics = {}
        self.calendar = []
        self.workouts = []
        
    def sync_oura_data(self, data=None):
        """Sync Oura ring data (simulated)"""
        if data is None:
            # Simulated data
            data = {
                "sleep_score": 85,
                "readiness_score": 78,
                "resting_heart_rate": 52,
                "hrv": 65,
                "steps": 8432,
                "calories_burned": 2100,
                "active_minutes": 45
            }
        self.metrics = data
        return data
    
    def add_workout(self, workout_type, duration, intensity="medium"):
        """Log a workout"""
        self.workouts.append({
            "type": workout_type,
            "duration": duration,
            "intensity": intensity,
            "date": datetime.now().isoformat()
        })
    
    def get_weekly_summary(self):
        """Get 7-day health summary"""
        total_sleep = self.metrics.get("sleep_score", 0)
        total_steps = self.metrics.get("steps", 0)
        total_workouts = len(self.workouts)
        
        return {
            "avg_sleep_score": total_sleep,
            "total_steps": total_steps,
            "workouts_this_week": total_workouts,
            "readiness": self.metrics.get("readiness_score", 0),
            "suggestion": self._get_suggestion()
        }
    
    def _get_suggestion(self):
        """AI-generated health suggestion"""
        readiness = self.metrics.get("readiness_score", 50)
        if readiness > 80:
            return "🚀 Great readiness! Push hard in your workout today."
        elif readiness > 60:
            return "💪 Moderate readiness. Maintain your regular routine."
        else:
            return "🛌 Low readiness. Consider light activity or rest day."
    
    def calendar_integration(self):
        """Get health blocks for calendar"""
        blocks = []
        readiness = self.metrics.get("readiness_score", 50)
        
        if readiness > 70:
            blocks.append({
                "type": "workout",
                "title": "High Intensity Training",
                "duration": "60 min",
                "suggested": ["Strength", "HIIT"]
            })
        else:
            blocks.append({
                "type": "workout", 
                "title": "Light Activity",
                "duration": "30 min",
                "suggested": ["Walking", "Yoga", "Stretching"]
            })
            
        blocks.append({
            "type": "recovery",
            "title": "Wind Down",
            "duration": "15 min",
            "suggested": ["Meditation", "Reading"]
        })
        
        return blocks

# Demo
health = HealthDashboard()

print("💪 HEALTH DASHBOARD")
print("="*50)

# Sync data
data = health.sync_oura_data()
print("\n📱 TODAY'S METRICS:")
print(f"  😴 Sleep Score: {data['sleep_score']}/100")
print(f"  ⚡ Readiness: {data['readiness_score']}/100")
print(f"  ❤️ Resting HR: {data['resting_heart_rate']} bpm")
print(f"  📊 HRV: {data['hrv']} ms")
print(f"  👣 Steps: {data['steps']:,}")
print(f"  🔥 Calories: {data['calories_burned']}")

# Add workouts
health.add_workout("Golf", 120, "medium")
health.add_workout("Weights", 45, "high")

# Get suggestions
summary = health.get_weekly_summary()
print(f"\n💡 AI SUGGESTION:")
print(f"  {summary['suggestion']}")

# Calendar blocks
print(f"\n📅 TODAY'S CALENDAR SUGGESTIONS:")
blocks = health.calendar_integration()
for block in blocks:
    print(f"  🏷️ {block['title']} ({block['duration']})")
    print(f"     Options: {', '.join(block['suggested'])}")

# Weekly summary
print(f"\n📊 WEEKLY SUMMARY:")
print(f"  Workouts logged: {summary['workouts_this_week']}")
print(f"  Avg Sleep Score: {summary['avg_sleep_score']}")
