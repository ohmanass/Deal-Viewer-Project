# Deal Viewer

Gestion et affichage de deals commerciaux avec templates d'affichage.

---

## Présentation

Deal Viewer est une application web complète permettant de gérer des opportunités commerciales riches stockées dans MongoDB. Elle implémente un système de **templates d'affichage** jouant le rôle d'adapters — un pattern architectural fondamental pour séparer la donnée brute de sa représentation visuelle.

Le principe central : un deal contient toujours l'intégralité de ses données. Le template décide quels champs afficher, dans quel ordre, et avec quels libellés. Le même deal peut donc être vu sous 4 angles différents sans jamais modifier la donnée source.

---

## Stack technique

- **Backend** : Python, FastAPI, Motor (driver MongoDB async)
- **Base de données** : MongoDB (2 collections : `deals` et `templates`)
- **Frontend** : React (Vite), React Router

---

## Architecture du projet

```
deal-viewer/
├── backend/
│   └── src/
│       └── app/
│           ├── main.py               # Point d'entrée FastAPI
│           ├── seed.py               # Script d'insertion des données de démo
│           ├── core/
│           │   ├── database.py       # Connexion MongoDB
│           │   └── utils.py          # Sérialisation ObjectId
│           ├── models/
│           │   ├── deal.py           # Modèles Pydantic pour les deals
│           │   └── template.py       # Modèles Pydantic pour les templates
│           ├── routes/
│           │   ├── deals.py          # Endpoints CRUD deals + projection
│           │   └── templates.py      # Endpoints CRUD templates
│           └── services/
│               └── projection.py     # Logique d'application du template sur un deal
└── frontend/
    └── src/
        ├── App.jsx                   # Routing principal
        ├── components/
        │   └── Navbar.jsx
        ├── pages/
        │   ├── TemplateList.jsx      # Liste des templates
        │   ├── TemplateForm.jsx      # Création d'un template
        │   ├── DealList.jsx          # Liste des deals + filtres
        │   ├── DealForm.jsx          # Création d'un deal
        │   └── DealView.jsx          # Affichage d'un deal avec template
        └── services/
            └── api.js                # Appels API REST
```

---

## Collections MongoDB

### Collection `deals`

Contient les documents deals complets avec l'ensemble des champs métier. C'est la **source de vérité unique** — elle ne change jamais selon la vue choisie.

Chaque document deal contient :
- Informations générales : `reference`, `title`, `clientName`, `status`, `priority`
- Données commerciales : `commercial.competitors`, `commercial.painPoints`, `commercial.nextStep`
- Données financières : `financials.totalInclTax`, `financials.expectedProfit`, `estimatedRevenue`
- Données de livraison : `delivery.region`, `delivery.implementationComplexity`
- Gouvernance : `governance.approvedByManager`, `governance.requiresLegalValidation`
- Tableaux : `contacts`, `products`, `notes`, `tags`

### Collection `templates`

Contient les adapters d'affichage. Chaque template définit :
- `visibleFields` : liste des champs du deal à afficher (notation pointée autorisée)
- `sections` : regroupement logique des champs en sections nommées
- `labels` : libellés personnalisés pour chaque champ

Le template **ne modifie jamais** la donnée — il agit comme un masque appliqué sur le document deal complet.

---

## Pourquoi le template est un adapter d'affichage

Le pattern **adapter d'affichage** repose sur une séparation stricte entre la donnée et sa représentation.

Un deal stocké en base contient 40+ champs couvrant tous les aspects métier. Selon le profil de l'utilisateur, seule une partie de ces champs est pertinente :

| Template | Profil | Champs exposés |
|---|---|---|
| Synthetic View | Commercial terrain | Référence, client, statut, owner, montant, closing |
| Commercial View | Analyste commercial | Contacts, concurrents, pain points, next step |
| Financial View | Direction financière | Montants HT/TTC, marges, taxes, coûts, profit |
| Management View | Direction générale | Statut, priorité, probabilité, validations requises |

La logique de projection est implémentée dans `services/projection.py` via la fonction `apply_template(deal, template)` qui :
1. Parcourt la liste `visibleFields` du template
2. Extrait chaque valeur du deal en gérant la **notation pointée** (`financials.totalInclTax`)
3. Reconstruit le document projeté organisé en sections avec labels personnalisés

---

## Routes API

### Templates

| Méthode | Endpoint | Description |
|---|---|---|
| `POST` | `/templates` | Créer un template |
| `GET` | `/templates` | Lister tous les templates |
| `GET` | `/templates/:id` | Récupérer un template |
| `PUT` | `/templates/:id` | Modifier un template |
| `DELETE` | `/templates/:id` | Supprimer un template |

### Deals

| Méthode | Endpoint | Description |
|---|---|---|
| `POST` | `/deals` | Créer un deal |
| `GET` | `/deals` | Lister tous les deals (avec filtres optionnels) |
| `GET` | `/deals/:id` | Récupérer un deal complet |
| `PUT` | `/deals/:id` | Modifier un deal |
| `DELETE` | `/deals/:id` | Supprimer un deal |
| `GET` | `/deals/:id/view?templateId=...` | Afficher un deal projeté par un template |

### Exemples d'appel

```bash
# Lister tous les deals
GET /deals

# Filtrer par client
GET /deals?clientName=ACME

# Filtrer par période
GET /deals?startDate=2026-01-01&endDate=2026-06-30

# Combiner les deux filtres (ET logique)
GET /deals?clientName=ACME&startDate=2026-01-01&endDate=2026-06-30

# Afficher un deal avec le template financier
GET /deals/abc123/view?templateId=xyz456
```

---

## Projection d'un deal par un template

La route `GET /deals/:id/view?templateId=...` est le cœur du projet.

**Comportement :**
1. Chargement du deal complet depuis MongoDB
2. Chargement du template depuis MongoDB
3. Application de `visibleFields` : seuls les champs listés sont extraits
4. Gestion de la notation pointée : `financials.totalInclTax` → `deal["financials"]["totalInclTax"]`
5. Organisation en sections avec labels personnalisés
6. Retour du document projeté — jamais le deal brut complet

**Règle d'or** : aucun deal ne peut être affiché sans template sélectionné au préalable. Cette règle est appliquée côté frontend (blocage de navigation) et côté backend (templateId obligatoire sur la route `/view`).

---

## Filtres deals

Les filtres sont implémentés via des query parameters sur `GET /deals`.

- **Par client** : recherche insensible à la casse via `$regex` MongoDB
- **Par période** : filtre sur `expectedCloseDate` via `$gte` / `$lte`
- **Combinaison** : les deux filtres sont combinés avec un opérateur ET logique

---

## Installation et lancement

### Prérequis

- Python 3.10+
- Poetry
- Node.js 20+
- MongoDB en local sur le port `27017`

### Backend

```bash
cd backend
poetry install
poetry shell
cd src/app
uvicorn main:app --reload
```

L'API est disponible sur `http://localhost:8000`.
La documentation Swagger est disponible sur `http://localhost:8000/docs`.

### Seed (données de démo)

```bash
cd backend
poetry run python src/app/seed.py
```

Insère 4 templates et 3 deals riches dans MongoDB.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

L'interface est disponible sur `http://localhost:5173`.

### Variables d'environnement

Créer un fichier `.env` dans `backend/` :

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=deal_viewer
```

---

## Données de démo

### 3 deals

| Référence | Client | Statut | Montant |
|---|---|---|---|
| DL-2026-0001 | ACME Corporation | NEGOTIATION | 120 000 € |
| DL-2026-0002 | Nextech Industries | PROPOSAL | 85 000 € |
| DL-2026-0003 | GlobalBank SA | QUALIFICATION | 250 000 € |

### 4 templates

| Code | Nom | Champs exposés |
|---|---|---|
| `SYNTHETIC_VIEW` | Synthetic View | 8 champs |
| `COMMERCIAL_VIEW` | Commercial View | 11 champs |
| `FINANCE_VIEW` | Financial View | 15 champs |
| `MANAGEMENT_VIEW` | Management View | 13 champs |

---

## Parcours utilisateur

1. Aller sur **Templates** → sélectionner un template
2. Cliquer sur **View Deals** → accéder à la liste des deals filtrée
3. Optionnel : filtrer par client ou par période
4. Cliquer sur **View** sur un deal → affichage projeté selon le template choisi
5. Revenir à la liste et choisir un autre template → l'affichage du même deal change complètement