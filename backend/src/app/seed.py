import asyncio
from datetime import datetime
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "deal_viewer")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

NOW = datetime.utcnow()

TEMPLATES = [
    {
        "name": "Synthetic View",
        "code": "SYNTHETIC_VIEW",
        "description": "Quick overview: reference, client, status, owner, amount and closing date",
        "isActive": True,
        "visibleFields": [
            "reference", "title", "clientName", "status",
            "ownerName", "estimatedRevenue", "expectedCloseDate", "priority"
        ],
        "sections": [
            {
                "name": "Deal Summary",
                "fields": [
                    "reference", "title", "clientName", "status",
                    "ownerName", "estimatedRevenue", "expectedCloseDate", "priority"
                ]
            }
        ],
        "labels": {
            "reference": "Reference",
            "title": "Deal Name",
            "clientName": "Client",
            "status": "Status",
            "ownerName": "Sales Owner",
            "estimatedRevenue": "Estimated Revenue",
            "expectedCloseDate": "Closing Date",
            "priority": "Priority",
        },
        "createdAt": NOW,
        "updatedAt": NOW,
    },
    {
        "name": "Commercial View",
        "code": "COMMERCIAL_VIEW",
        "description": "Commercial details: contacts, competitors, pain points, next step",
        "isActive": True,
        "visibleFields": [
            "reference", "title", "clientName", "status", "probability",
            "contacts", "commercial.competitors", "commercial.painPoints",
            "commercial.proposedSolution", "commercial.nextStep", "commercial.nextStepDate"
        ],
        "sections": [
            {
                "name": "General Information",
                "fields": ["reference", "title", "clientName", "status", "probability"]
            },
            {
                "name": "Client Contacts",
                "fields": ["contacts"]
            },
            {
                "name": "Commercial Analysis",
                "fields": [
                    "commercial.competitors", "commercial.painPoints",
                    "commercial.proposedSolution", "commercial.nextStep",
                    "commercial.nextStepDate"
                ]
            }
        ],
        "labels": {
            "reference": "Reference",
            "title": "Deal Name",
            "clientName": "Client",
            "probability": "Probability (%)",
            "commercial.competitors": "Competitors",
            "commercial.painPoints": "Pain Points",
            "commercial.proposedSolution": "Proposed Solution",
            "commercial.nextStep": "Next Step",
            "commercial.nextStepDate": "Next Step Date",
        },
        "createdAt": NOW,
        "updatedAt": NOW,
    },
    {
        "name": "Financial View",
        "code": "FINANCE_VIEW",
        "description": "Amounts, margins, taxes, costs and expected profit",
        "isActive": True,
        "visibleFields": [
            "reference", "title", "clientName", "status",
            "estimatedRevenue", "estimatedMargin", "currency",
            "financials.subtotal", "financials.discountGlobalPercent",
            "financials.taxPercent", "financials.totalExclTax",
            "financials.totalInclTax", "financials.estimatedCost",
            "financials.expectedProfit", "expectedCloseDate"
        ],
        "sections": [
            {
                "name": "General Information",
                "fields": ["reference", "title", "clientName", "status", "expectedCloseDate"]
            },
            {
                "name": "Financial Indicators",
                "fields": [
                    "estimatedRevenue", "estimatedMargin", "currency",
                    "financials.subtotal", "financials.discountGlobalPercent",
                    "financials.taxPercent", "financials.totalExclTax",
                    "financials.totalInclTax", "financials.estimatedCost",
                    "financials.expectedProfit"
                ]
            }
        ],
        "labels": {
            "reference": "Reference",
            "title": "Deal Name",
            "clientName": "Client",
            "estimatedRevenue": "Estimated Revenue",
            "estimatedMargin": "Estimated Margin",
            "expectedCloseDate": "Expected Closing",
            "financials.subtotal": "Subtotal",
            "financials.discountGlobalPercent": "Global Discount (%)",
            "financials.taxPercent": "Tax (%)",
            "financials.totalExclTax": "Total Excl. Tax",
            "financials.totalInclTax": "Total Incl. Tax",
            "financials.estimatedCost": "Estimated Cost",
            "financials.expectedProfit": "Expected Profit",
        },
        "createdAt": NOW,
        "updatedAt": NOW,
    },
    {
        "name": "Management View",
        "code": "MANAGEMENT_VIEW",
        "description": "Strategic overview: status, priority, revenue, probability and validations",
        "isActive": True,
        "visibleFields": [
            "reference", "title", "clientName", "status", "priority",
            "ownerName", "estimatedRevenue", "probability",
            "commercial.nextStep", "commercial.nextStepDate",
            "governance.approvedByManager", "governance.requiresLegalValidation",
            "governance.requiresFinanceValidation"
        ],
        "sections": [
            {
                "name": "Strategic Overview",
                "fields": [
                    "reference", "title", "clientName", "status", "priority",
                    "ownerName", "estimatedRevenue", "probability"
                ]
            },
            {
                "name": "Next Step",
                "fields": ["commercial.nextStep", "commercial.nextStepDate"]
            },
            {
                "name": "Required Validations",
                "fields": [
                    "governance.approvedByManager",
                    "governance.requiresLegalValidation",
                    "governance.requiresFinanceValidation"
                ]
            }
        ],
        "labels": {
            "reference": "Reference",
            "title": "Deal Name",
            "clientName": "Client",
            "status": "Status",
            "priority": "Priority",
            "ownerName": "Owner",
            "estimatedRevenue": "Estimated Revenue",
            "probability": "Probability (%)",
            "commercial.nextStep": "Next Step",
            "commercial.nextStepDate": "Next Step Date",
            "governance.approvedByManager": "Approved by Manager",
            "governance.requiresLegalValidation": "Legal Validation Required",
            "governance.requiresFinanceValidation": "Finance Validation Required",
        },
        "createdAt": NOW,
        "updatedAt": NOW,
    },
]

DEALS = [
    {
        "reference": "DL-2026-0001",
        "title": "CRM Europe Deployment 2026",
        "subtitle": "Framework contract for CRM transformation",
        "clientName": "ACME Corporation",
        "clientCode": "ACME-001",
        "industry": "Technology",
        "country": "France",
        "city": "Paris",
        "ownerName": "Alice Martin",
        "ownerEmail": "alice.martin@company.com",
        "status": "NEGOTIATION",
        "priority": "HIGH",
        "stage": "proposal",
        "estimatedRevenue": 120000,
        "estimatedMargin": 35000,
        "currency": "EUR",
        "probability": 70,
        "expectedCloseDate": "2026-04-15",
        "contacts": [
            {
                "firstName": "Jean",
                "lastName": "Dupont",
                "jobTitle": "IT Director",
                "email": "jean.dupont@acme.com",
                "isDecisionMaker": True
            }
        ],
        "products": [
            {
                "name": "CRM Enterprise Suite",
                "quantity": 1,
                "unitPrice": 90000,
                "discountPercent": 10,
                "finalPrice": 81000
            }
        ],
        "financials": {
            "subtotal": 105000,
            "discountGlobalPercent": 5,
            "taxPercent": 20,
            "totalExclTax": 99750,
            "totalInclTax": 119700,
            "estimatedCost": 65000,
            "expectedProfit": 34750
        },
        "commercial": {
            "needIdentified": True,
            "competitors": ["Salesforce", "HubSpot"],
            "painPoints": ["scattered tools", "lack of reporting"],
            "proposedSolution": "Unified CRM Suite",
            "nextStep": "Legal validation",
            "nextStepDate": "2026-03-20"
        },
        "delivery": {
            "deliveryMode": "hybrid",
            "region": "EMEA",
            "implementationComplexity": "MEDIUM",
            "estimatedKickoffDate": "2026-05-05",
            "estimatedDeliveryWeeks": 10,
            "requiresTraining": True,
            "requiresMigration": True
        },
        "governance": {
            "createdBy": "alice.martin@company.com",
            "approvedByManager": False,
            "requiresLegalValidation": True,
            "requiresFinanceValidation": True,
            "isArchived": False
        },
        "tags": ["crm", "enterprise", "france"],
        "notes": [
            {
                "author": "Alice Martin",
                "content": "First meeting went well.",
                "createdAt": datetime(2026, 3, 11, 10, 0, 0)
            }
        ],
        "createdAt": datetime(2026, 1, 15),
        "updatedAt": datetime(2026, 3, 11),
    },
    {
        "reference": "DL-2026-0002",
        "title": "ERP Cloud Migration - Nextech",
        "subtitle": "ERP migration project to AWS cloud",
        "clientName": "Nextech Industries",
        "clientCode": "NEXT-002",
        "industry": "Manufacturing",
        "country": "France",
        "city": "Lyon",
        "ownerName": "Baptiste Renard",
        "ownerEmail": "b.renard@company.com",
        "status": "PROPOSAL",
        "priority": "MEDIUM",
        "stage": "discovery",
        "estimatedRevenue": 85000,
        "estimatedMargin": 22000,
        "currency": "EUR",
        "probability": 45,
        "expectedCloseDate": "2026-06-30",
        "contacts": [
            {
                "firstName": "Sophie",
                "lastName": "Marchand",
                "jobTitle": "CIO",
                "email": "s.marchand@nextech.fr",
                "isDecisionMaker": True
            }
        ],
        "products": [
            {
                "name": "ERP Cloud Migration Pack",
                "quantity": 1,
                "unitPrice": 75000,
                "discountPercent": 5,
                "finalPrice": 71250
            }
        ],
        "financials": {
            "subtotal": 78750,
            "discountGlobalPercent": 0,
            "taxPercent": 20,
            "totalExclTax": 78750,
            "totalInclTax": 94500,
            "estimatedCost": 56000,
            "expectedProfit": 22750
        },
        "commercial": {
            "needIdentified": True,
            "competitors": ["SAP", "Oracle Cloud"],
            "painPoints": ["outdated ERP", "high maintenance costs"],
            "proposedSolution": "Cloud ERP migration with Change Management",
            "nextStep": "Technical demo + POC",
            "nextStepDate": "2026-03-25"
        },
        "delivery": {
            "deliveryMode": "remote",
            "region": "France",
            "implementationComplexity": "HIGH",
            "estimatedKickoffDate": "2026-07-15",
            "estimatedDeliveryWeeks": 24,
            "requiresTraining": True,
            "requiresMigration": True
        },
        "governance": {
            "createdBy": "b.renard@company.com",
            "approvedByManager": True,
            "requiresLegalValidation": False,
            "requiresFinanceValidation": True,
            "isArchived": False
        },
        "tags": ["erp", "cloud", "migration"],
        "notes": [],
        "createdAt": datetime(2026, 2, 1),
        "updatedAt": datetime(2026, 3, 5),
    },
    {
        "reference": "DL-2026-0003",
        "title": "Data Analytics Platform - GlobalBank",
        "subtitle": "Real-time BI and analytics platform setup",
        "clientName": "GlobalBank SA",
        "clientCode": "GLOB-003",
        "industry": "Finance",
        "country": "France",
        "city": "Paris",
        "ownerName": "Claire Fontaine",
        "ownerEmail": "c.fontaine@company.com",
        "status": "QUALIFICATION",
        "priority": "HIGH",
        "stage": "qualification",
        "estimatedRevenue": 250000,
        "estimatedMargin": 80000,
        "currency": "EUR",
        "probability": 30,
        "expectedCloseDate": "2026-09-01",
        "contacts": [
            {
                "firstName": "Thomas",
                "lastName": "Leroy",
                "jobTitle": "Chief Data Officer",
                "email": "t.leroy@globalbank.fr",
                "isDecisionMaker": True
            }
        ],
        "products": [
            {
                "name": "Data Platform Enterprise",
                "quantity": 1,
                "unitPrice": 180000,
                "discountPercent": 0,
                "finalPrice": 180000
            }
        ],
        "financials": {
            "subtotal": 220500,
            "discountGlobalPercent": 0,
            "taxPercent": 20,
            "totalExclTax": 220500,
            "totalInclTax": 264600,
            "estimatedCost": 140000,
            "expectedProfit": 80500
        },
        "commercial": {
            "needIdentified": False,
            "competitors": ["Palantir", "Snowflake", "Databricks"],
            "painPoints": ["data silos", "manual reporting", "slow time-to-insight"],
            "proposedSolution": "Unified lakehouse platform with real-time dashboards",
            "nextStep": "Scoping workshop with data team",
            "nextStepDate": "2026-04-10"
        },
        "delivery": {
            "deliveryMode": "onsite",
            "region": "Ile-de-France",
            "implementationComplexity": "VERY_HIGH",
            "estimatedKickoffDate": "2026-10-01",
            "estimatedDeliveryWeeks": 36,
            "requiresTraining": True,
            "requiresMigration": True
        },
        "governance": {
            "createdBy": "c.fontaine@company.com",
            "approvedByManager": False,
            "requiresLegalValidation": True,
            "requiresFinanceValidation": True,
            "isArchived": False
        },
        "tags": ["data", "analytics", "finance"],
        "notes": [
            {
                "author": "Claire Fontaine",
                "content": "Very promising qualification meeting. CDO highly interested.",
                "createdAt": datetime(2026, 3, 8, 14, 30, 0)
            }
        ],
        "createdAt": datetime(2026, 3, 1),
        "updatedAt": datetime(2026, 3, 8),
    },
]


async def seed():
    print("Seeding Deal Viewer database...")
    await db.templates.delete_many({})
    await db.deals.delete_many({})
    print("Collections cleared.")
    await db.templates.insert_many(TEMPLATES)
    print(f"{len(TEMPLATES)} templates inserted.")
    await db.deals.insert_many(DEALS)
    print(f"{len(DEALS)} deals inserted.")
    print("Seed completed successfully.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())