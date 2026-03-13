from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from datetime import datetime

from core.database import get_db
from core.utils import serialize_doc, to_object_id
from models.deal import DealCreate, DealUpdate
from services.projection import apply_template

router = APIRouter()


# --- Helper ---
def build_filter_query(
    clientName: Optional[str],
    startDate: Optional[str],
    endDate: Optional[str],
) -> dict:
    """
    Construire une requete de filtrage pour MongoDB selon les parametres fournis.
    
    - clientName : filtre par nom de client (regex insensible a la casse)
    - startDate  : filtre les deals avec expectedCloseDate >= startDate
    - endDate    : filtre les deals avec expectedCloseDate <= endDate
    """
    query = {}

    if clientName:
        query["clientName"] = {"$regex": clientName, "$options": "i"}

    if startDate or endDate:
        date_filter = {}
        if startDate:
            date_filter["$gte"] = startDate
        if endDate:
            date_filter["$lte"] = endDate
        query["expectedCloseDate"] = date_filter

    return query


# --- CRUD ---
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_deal(deal: DealCreate):
    """
    Creer un nouveau deal dans la base de donnees.
    
    Verifie si un deal avec la meme reference existe.
    Ajoute createdAt et updatedAt avant insertion.
    """
    db = get_db()
    now = datetime.utcnow()
    deal_dict = deal.model_dump(exclude_none=True)
    deal_dict["createdAt"] = now
    deal_dict["updatedAt"] = now

    # Verifier existence d'un deal avec la meme reference
    existing = await db.deals.find_one({"reference": deal_dict["reference"]})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"A deal with reference '{deal_dict['reference']}' already exists.",
        )

    result = await db.deals.insert_one(deal_dict)
    created = await db.deals.find_one({"_id": result.inserted_id})
    return serialize_doc(created)

@router.get("/")
async def list_deals(
    clientName: Optional[str] = Query(None, description="Filter by client name"),
    startDate: Optional[str] = Query(None, description="Start date (expectedCloseDate >= startDate)"),
    endDate: Optional[str] = Query(None, description="End date (expectedCloseDate <= endDate)"),
):
    """
    Lister les deals avec filtres optionnels.
    
    - clientName : filtrage par nom de client
    - startDate / endDate : filtrage par plage de dates
    Limite resultat a 1000 documents et trie par date de creation decroissante.
    """
    db = get_db()
    query = build_filter_query(clientName, startDate, endDate)
    cursor = db.deals.find(query).sort("createdAt", -1)
    deals = await cursor.to_list(length=1000)
    return [serialize_doc(d) for d in deals]

@router.get("/{deal_id}/view")
async def view_deal_with_template(
    deal_id: str,
    templateId: str = Query(..., description="Template ID — required"),
):
    """
    Afficher un deal applique a un template.
    
    - Verifie existence du deal et du template
    - Verifie que le template est actif
    - Applique la projection du template sur le deal
    """
    db = get_db()

    # Charger le deal
    try:
        deal_oid = to_object_id(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    deal = await db.deals.find_one({"_id": deal_oid})
    if not deal:
        raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

    # Charger le template
    try:
        tmpl_oid = to_object_id(templateId)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid templateId: {e}")

    template = await db.templates.find_one({"_id": tmpl_oid})
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{templateId}' not found.")

    if not template.get("isActive", True):
        raise HTTPException(status_code=400, detail=f"Template '{template.get('name')}' is inactive.")

    # Appliquer le template sur le deal
    return apply_template(serialize_doc(deal), serialize_doc(template))

@router.get("/{deal_id}")
async def get_deal(deal_id: str):
    """
    Recuperer un deal par son ID.
    
    - Verifie que l'ID est valide
    - Retourne le deal serialise
    """
    db = get_db()
    try:
        oid = to_object_id(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    deal = await db.deals.find_one({"_id": oid})
    if not deal:
        raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")
    return serialize_doc(deal)

@router.put("/{deal_id}")
async def update_deal(deal_id: str, deal_update: DealUpdate):
    """
    Mettre a jour un deal existant.
    
    - Verifie que le deal existe
    - Exclut les champs None lors de la mise a jour
    - Met a jour le champ updatedAt
    """
    db = get_db()
    try:
        oid = to_object_id(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing = await db.deals.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

    update_data = deal_update.model_dump(exclude_none=True)
    update_data["updatedAt"] = datetime.utcnow()

    await db.deals.update_one({"_id": oid}, {"$set": update_data})
    updated = await db.deals.find_one({"_id": oid})
    return serialize_doc(updated)

@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(deal_id: str):
    """
    Supprimer un deal par son ID.
    
    - Verifie que l'ID est valide
    - Verifie que le deal existe avant suppression
    - Retourne 204 si suppression reussie
    """
    db = get_db()
    try:
        oid = to_object_id(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await db.deals.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")