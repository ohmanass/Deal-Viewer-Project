from pydantic import BaseModel
from typing import Optional, List, Dict


class Section(BaseModel):
    name: str
    fields: List[str]

class TemplateCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    isActive: Optional[bool] = True
    visibleFields: List[str]
    sections: Optional[List[Section]] = []
    labels: Optional[Dict[str, str]] = {}

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    isActive: Optional[bool] = None
    visibleFields: Optional[List[str]] = None
    sections: Optional[List[Section]] = None
    labels: Optional[Dict[str, str]] = None