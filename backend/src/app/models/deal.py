from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- sous docs ---
class Contact(BaseModel):
    firstName: str
    lastName: str
    jobTitle: Optional[str] = None
    email: Optional[str] = None
    isDecisionMaker: Optional[bool] = False

class Product(BaseModel):
    name: str
    quantity: Optional[int] = 1
    unitPrice: Optional[float] = None
    discountPercent: Optional[float] = 0
    finalPrice: Optional[float] = None

class Financials(BaseModel):
    subtotal: Optional[float] = None
    discountGlobalPercent: Optional[float] = 0
    taxPercent: Optional[float] = 20
    totalExclTax: Optional[float] = None
    totalInclTax: Optional[float] = None
    estimatedCost: Optional[float] = None
    expectedProfit: Optional[float] = None

class Commercial(BaseModel):
    needIdentified: Optional[bool] = False
    competitors: Optional[List[str]] = []
    painPoints: Optional[List[str]] = []
    proposedSolution: Optional[str] = None
    nextStep: Optional[str] = None
    nextStepDate: Optional[str] = None

class Delivery(BaseModel):
    deliveryMode: Optional[str] = None
    region: Optional[str] = None
    implementationComplexity: Optional[str] = None
    estimatedKickoffDate: Optional[str] = None
    estimatedDeliveryWeeks: Optional[int] = None
    requiresTraining: Optional[bool] = False
    requiresMigration: Optional[bool] = False

class Governance(BaseModel):
    createdBy: Optional[str] = None
    approvedByManager: Optional[bool] = False
    requiresLegalValidation: Optional[bool] = False
    requiresFinanceValidation: Optional[bool] = False
    isArchived: Optional[bool] = False

class Note(BaseModel):
    author: Optional[str] = None
    content: Optional[str] = None
    createdAt: Optional[datetime] = None


# --- doc principal ---
class DealCreate(BaseModel):
    reference: str
    title: str
    clientName: str
    subtitle: Optional[str] = None
    clientCode: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    ownerName: Optional[str] = None
    ownerEmail: Optional[str] = None
    status: Optional[str] = "NEW"
    priority: Optional[str] = "MEDIUM"
    stage: Optional[str] = None
    estimatedRevenue: Optional[float] = None
    estimatedMargin: Optional[float] = None
    currency: Optional[str] = "EUR"
    probability: Optional[int] = 0
    expectedCloseDate: Optional[str] = None
    contacts: Optional[List[Contact]] = []
    products: Optional[List[Product]] = []
    financials: Optional[Financials] = None
    commercial: Optional[Commercial] = None
    delivery: Optional[Delivery] = None
    governance: Optional[Governance] = None
    tags: Optional[List[str]] = []
    notes: Optional[List[Note]] = []

class DealUpdate(DealCreate):
    reference: Optional[str] = None
    title: Optional[str] = None
    clientName: Optional[str] = None