import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI(title="SaaS Landing Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class ContactSubmission(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=2000)


# ---------- Routes ----------
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.post("/api/contact")
def submit_contact(payload: ContactSubmission):
    try:
        from database import create_document
        doc_id = create_document("contact", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pricing")
def get_pricing():
    plans = [
        {
            "name": "Starter",
            "price": 0,
            "period": "mo",
            "features": ["Up to 3 projects", "Basic analytics", "Community support"],
            "cta": "Get Started",
            "highlight": False,
        },
        {
            "name": "Pro",
            "price": 29,
            "period": "mo",
            "features": ["Unlimited projects", "Advanced analytics", "Priority support", "Team access"],
            "cta": "Start Pro",
            "highlight": True,
        },
        {
            "name": "Enterprise",
            "price": 99,
            "period": "mo",
            "features": ["Custom SLAs", "Dedicated success manager", "SSO/SAML", "Security reviews"],
            "cta": "Contact Sales",
            "highlight": False,
        },
    ]
    return {"plans": plans}

@app.get("/api/testimonials")
def get_testimonials():
    testimonials = [
        {
            "name": "Avery Quinn",
            "role": "CTO, NovaPay",
            "quote": "We shipped our fintech MVP 3x faster. The glassmorphic design elevates our brand.",
            "avatar": "https://i.pravatar.cc/100?img=12",
        },
        {
            "name": "Maya Chen",
            "role": "Founder, FluxAI",
            "quote": "Onboarding was a breeze and conversions jumped 27% in the first week.",
            "avatar": "https://i.pravatar.cc/100?img=5",
        },
        {
            "name": "Leo Martins",
            "role": "Product Lead, Velo",
            "quote": "Beautiful defaults, sane APIs, and a modern feel our users love.",
            "avatar": "https://i.pravatar.cc/100?img=32",
        },
    ]
    return {"testimonials": testimonials}

@app.get("/api/blog")
def get_blog():
    posts = [
        {
            "id": 1,
            "title": "Designing with Glassmorphism in 2025",
            "excerpt": "How to balance depth, contrast, and accessibility in frosted UIs.",
            "tag": "Design",
            "date": "2025-09-01",
        },
        {
            "id": 2,
            "title": "Why Fintech Loves 3D Micro-Interactions",
            "excerpt": "A breakdown of subtle 3D cues that improve trust and clarity.",
            "tag": "Product",
            "date": "2025-10-12",
        },
        {
            "id": 3,
            "title": "From MVP to Scale: A SaaS Playbook",
            "excerpt": "Pricing, packaging, and the experiments that matter.",
            "tag": "Growth",
            "date": "2025-10-28",
        },
    ]
    return {"posts": posts}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
