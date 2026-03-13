from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from core.database import get_db
from core.utils import serialize_doc, to_object_id
from models.template import TemplateCreate, TemplateUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_template(template: TemplateCreate):
    db = get_db()
    now = datetime.utcnow()
    tmpl_dict = template.model_dump(exclude_none=True)
    tmpl_dict["createdAt"] = now
    tmpl_dict["updatedAt"] = now

    existing = await db.templates.find_one({"code": tmpl_dict["code"]})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"A template with code '{tmpl_dict['code']}' already exists.",
        )

    result = await db.templates.insert_one(tmpl_dict)
    created = await db.templates.find_one({"_id": result.inserted_id})
    return serialize_doc(created)


@router.get("/")
async def list_templates():
    db = get_db()
    cursor = db.templates.find().sort("createdAt", -1)
    templates = await cursor.to_list(length=100)
    return [serialize_doc(t) for t in templates]


@router.get("/{template_id}")
async def get_template(template_id: str):
    db = get_db()
    try:
        oid = to_object_id(template_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    template = await db.templates.find_one({"_id": oid})
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found.")
    return serialize_doc(template)


@router.put("/{template_id}")
async def update_template(template_id: str, update: TemplateUpdate):
    db = get_db()
    try:
        oid = to_object_id(template_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing = await db.templates.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found.")

    update_data = update.model_dump(exclude_none=True)
    update_data["updatedAt"] = datetime.utcnow()

    await db.templates.update_one({"_id": oid}, {"$set": update_data})
    updated = await db.templates.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: str):
    db = get_db()
    try:
        oid = to_object_id(template_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await db.templates.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found.")