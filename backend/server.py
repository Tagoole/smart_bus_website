from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from typing import List, Optional

app = FastAPI(title="SmartBus API", description="Smart Bus Mobility Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "SmartBus API is running"}

# Landing page data endpoints
@app.get("/api/stats")
async def get_platform_stats():
    """Get platform statistics for the landing page"""
    return {
        "daily_users": "50K+",
        "on_time_performance": "98%",
        "routes_covered": "200+",
        "total_trips": "1M+",
        "cities_served": "25",
        "user_satisfaction": "4.8/5"
    }

@app.get("/api/features")
async def get_features():
    """Get platform features"""
    return {
        "features": [
            {
                "id": "real-time-tracking",
                "name": "Real-Time Tracking",
                "description": "Track buses in real-time with precise GPS locations and accurate ETAs for every stop.",
                "icon": "location",
                "benefits": [
                    "Live GPS tracking for all buses",
                    "Accurate ETA predictions",
                    "Automatic delay notifications"
                ]
            },
            {
                "id": "mobile-ticketing",
                "name": "Mobile Ticketing",
                "description": "Purchase tickets digitally with secure payments and instant QR code generation.",
                "icon": "ticket",
                "benefits": [
                    "Secure digital payments",
                    "Instant QR code tickets",
                    "Monthly passes & discounts"
                ]
            },
            {
                "id": "route-optimization",
                "name": "Route Optimization",
                "description": "AI-powered route planning and optimization for maximum efficiency and reduced wait times.",
                "icon": "analytics",
                "benefits": [
                    "Real-time analytics dashboard",
                    "Predictive demand forecasting",
                    "Automated fleet management"
                ]
            }
        ]
    }

@app.get("/api/download-info")
async def get_download_info():
    """Get app download information"""
    return {
        "android": {
            "available": False,
            "version": "1.0.0",
            "size": "45MB",
            "last_updated": "January 2025",
            "download_url": None,
            "placeholder_text": "📱 APK Download Placeholder"
        },
        "ios": {
            "available": False,
            "version": "1.0.0",
            "size": "42MB", 
            "last_updated": "January 2025",
            "download_url": None,
            "placeholder_text": "🍎 App Store Placeholder"
        }
    }

# Mock endpoints for future app functionality
@app.get("/api/buses/nearby")
async def get_nearby_buses():
    """Get nearby buses (mock data for demo)"""
    return {
        "buses": [
            {
                "id": "bus-001",
                "route": "Route 15",
                "current_location": {"lat": 40.7128, "lng": -74.0060},
                "eta_minutes": 5,
                "occupancy": "medium",
                "next_stops": ["Central Station", "City Mall", "University"]
            },
            {
                "id": "bus-002", 
                "route": "Route 22",
                "current_location": {"lat": 40.7580, "lng": -73.9855},
                "eta_minutes": 12,
                "occupancy": "low",
                "next_stops": ["Downtown", "Business District", "Airport"]
            }
        ]
    }

@app.get("/api/routes")
async def get_routes():
    """Get available routes (mock data)"""
    return {
        "routes": [
            {
                "id": "route-15",
                "name": "Route 15",
                "color": "#3B82F6",
                "stops": ["Terminal A", "Central Station", "City Mall", "University", "Hospital"],
                "frequency": "Every 10 minutes",
                "operating_hours": "06:00 - 23:00"
            },
            {
                "id": "route-22",
                "name": "Route 22", 
                "color": "#10B981",
                "stops": ["Downtown", "Business District", "Shopping Center", "Airport"],
                "frequency": "Every 15 minutes",
                "operating_hours": "05:30 - 24:00"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)