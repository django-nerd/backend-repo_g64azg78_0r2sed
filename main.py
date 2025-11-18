import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Fragrance, Subscriber, Order

app = FastAPI(title="Elanor - Gothic Perfumery API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Elanor API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Seed initial seven fragrances if empty
SEVEN_SINS = [
    {
        "name": "Pride",
        "slug": "pride",
        "sin": "Pride",
        "top_notes": ["bergamot", "black pepper"],
        "heart_notes": ["orris", "violet"],
        "base_notes": ["amber", "cashmere wood"],
        "description": "A luminous self-regard, gilded and unbowed.",
        "story": "In mirrored halls where crowns are invisible, Pride walks perfumed with certainty.",
        "price": 145.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Greed",
        "slug": "greed",
        "sin": "Greed",
        "top_notes": ["saffron", "aldehydes"],
        "heart_notes": ["ylang", "tobacco"],
        "base_notes": ["oud", "tonka", "golden resin"],
        "description": "Gleam of coin, velvet vaults, a hunger that glitters.",
        "story": "Greed hoards the sun, corked in crystal. Every drop a ransom.",
        "price": 165.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Lust",
        "slug": "lust",
        "sin": "Lust",
        "top_notes": ["black cherry", "pomegranate"],
        "heart_notes": ["damask rose", "jasmine sambac"],
        "base_notes": ["musk", "patchouli"],
        "description": "Velvet breath and bitten fruit under blackout silk.",
        "story": "Lust speaks in midnight vowels—skin remembers before the mind consents.",
        "price": 155.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Envy",
        "slug": "envy",
        "sin": "Envy",
        "top_notes": ["green apple", "galbanum"],
        "heart_notes": ["ivy", "lily of the valley"],
        "base_notes": ["vetiver", "oakmoss"],
        "description": "A cool gaze through frosted glass.",
        "story": "Envy prays at other altars and leaves with stained fingers of emerald.",
        "price": 140.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Gluttony",
        "slug": "gluttony",
        "sin": "Gluttony",
        "top_notes": ["caramel", "toasted sesame"],
        "heart_notes": ["cocoa", "cinnamon"],
        "base_notes": ["vanilla absolute", "smoked cedar"],
        "description": "Opulent, sticky-sweet decadence, candlelit and unashamed.",
        "story": "Gluttony licks the spoon clean and calls it worship.",
        "price": 135.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Wrath",
        "slug": "wrath",
        "sin": "Wrath",
        "top_notes": ["blood orange", "pink pepper"],
        "heart_notes": ["clove", "leather"],
        "base_notes": ["smoke", "birch tar"],
        "description": "A spark to tinder. Heat, metal, and a vow.",
        "story": "Wrath burns a clean line through the dark and calls it justice.",
        "price": 150.0,
        "image": None,
        "in_stock": True
    },
    {
        "name": "Sloth",
        "slug": "sloth",
        "sin": "Sloth",
        "top_notes": ["lavender", "chamomile"],
        "heart_notes": ["iris", "cashmere"],
        "base_notes": ["sandalwood", "white musk"],
        "description": "Soft corners, slow clocks. The world on mute.",
        "story": "Sloth is a lullaby folded into wool.",
        "price": 130.0,
        "image": None,
        "in_stock": True
    }
]

@app.post("/seed")
def seed_fragrances():
    try:
        existing = get_documents("fragrance", {}, limit=1)
        if existing:
            return {"status": "ok", "message": "Fragrances already seeded"}
        for f in SEVEN_SINS:
            create_document("fragrance", f)
        return {"status": "ok", "created": len(SEVEN_SINS)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fragrances", response_model=List[Fragrance])
def list_fragrances():
    try:
        docs = get_documents("fragrance")
        # Convert ObjectId etc.
        result = []
        for d in docs:
            d.pop("_id", None)
            result.append(Fragrance(**d))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SubscribeBody(BaseModel):
    email: str
    name: Optional[str] = None

@app.post("/subscribe")
def subscribe(body: SubscribeBody):
    try:
        sid = create_document("subscriber", body.dict())
        return {"status": "ok", "id": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/order")
def create_order(order: Order):
    try:
        oid = create_document("order", order)
        return {"status": "ok", "id": oid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
