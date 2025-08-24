# Vendor & Shop Management System (Django REST + React + JWT + MongoDB)

Modern vendor portal to register/login, create & manage shops, and a public **Nearby** search using the Haversine formula.  
Backend: **Django + DRF + JWT (SimpleJWT) + MongoDB Atlas (MongoEngine)**  
Frontend: **React (Vite) + TailwindCSS**

---

## ✨ Features

- Vendor registration & JWT login (access/refresh)
- Create / list / view / update / delete **your** shops
- Public **Nearby** search: `GET /api/shops/nearby/?lat=&lng=&radius=`
- “Use Your Current Location” in **Create Shop** and **Nearby Search**
- Search by **city name** (geocoding via OpenStreetMap)
- Sleek dashboard with KPIs + list, and a polished login page
- Rate-limited public endpoint (IP-based)

---

## 🧱 Tech Stack

- **Backend:** Django 5, Django REST Framework, SimpleJWT, django-environ, django-cors-headers, **MongoEngine**
- **DB:** MongoDB Atlas (URI via `.env`)
- **Frontend:** React 18 (Vite), TailwindCSS
- **Auth:** JWT (short-lived access, long-lived refresh)

---

## 📂 Project Structure
```
vendor-shop/
├── backend/
│   ├── apps/
│   │   ├── vendors/                # vendor registration & auth
│   │   └── shops/                  # shop CRUD + nearby search
│   │       ├── mongo_models.py     # MongoEngine Shop model
│   │       ├── serializers.py      # DRF serializers
│   │       ├── utils.py            # haversine + bounding box
│   │       ├── permissions.py      # custom IsOwner permission
│   │       ├── views.py            # ViewSet for shops
│   │       └── urls.py             # routes for /api/shops
│   ├── project/
│   │   ├── settings.py             # Django settings
│   │   ├── urls.py                 # root URL conf
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── manage.py                   # Django entrypoint
├── frontend/
│   ├── index.html
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx                 # root layout
│       ├── main.jsx                # React entrypoint
│       ├── index.css               # Tailwind styles
│       ├── lib/
│       │   └── api.js              # axios API helpers
│       ├── components/
│       │   └── ShopForm.jsx        # reusable form
│       └── pages/
│           ├── Login.jsx           # login/register page
│           ├── Dashboard.jsx       # vendor dashboard
│           ├── NewShop.jsx         # add new shop
│           └── Shops.jsx           # public nearby search
├── api/
│   └── index.py                    # Vercel serverless entrypoint
├── vercel.json                     # Vercel config
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md
```
---

## 🔐 Environment Variables

Create **`.env`** in repo root:

```bash
# Django
SECRET_KEY=replace-with-a-strong-random-key
DEBUG=True
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
JWT_ACCESS_LIFETIME_MIN=10
JWT_REFRESH_LIFETIME_DAYS=7

# MongoDB (Atlas)
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster1.d2ejgkh.mongodb.net/Vendor-Shop?retryWrites=true&w=majority&appName=Cluster1
```
## 🔑 Generate a key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
## 🌐 Local Frontend Environment
**Create file: frontend/.env.local**
```bash
VITE_API_BASE=http://127.0.0.1:8000
```
For **production (Vercel),** leave VITE_API_BASE empty.

## 🐍 Backend — Setup & Run (Local)
```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# run server
cd backend
python manage.py runserver 8000
```
**Notes:**
- Django auth/admin stays on **SQLite.**
- All shops data go to **MongoDB Atlas** (no migrations needed for shops).
 
## ⚛️ Frontend — Setup & Run (Local)
```bash
# in another terminal
cd frontend
npm install
npm run dev
```
Open: **http://localhost:5173**
  
## 🧭 API Endpoints
```bash
Base: http://127.0.0.1:8000
```
## Auth
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh

## Shops (JWT required)
- GET /api/shops/
- POST /api/shops/
- GET /api/shops/{id}/
- PUT/PATCH /api/shops/{id}/
- DELETE /api/shops/{id}/

## Nearby (public)
- GET /api/shops/nearby/?lat=&lng=&radius=

Example:
```bash
curl "http://127.0.0.1:8000/api/shops/nearby/?lat=28.61&lng=77.20&radius=5"
```
## Nearby Strategy
- 1. Prefilter with bounding box
- 2. Compute precise Haversine
- 3. Filter by radius, sort ascending, return distance_km

## 🧰 Troubleshooting
- 401 /api/ — expected; JWT required. Login first.
- Mongo error — check MONGODB_URI and whitelist IP in Atlas.
- Blank frontend — reinstall (npm install), check Tailwind config.
- CORS error (local) — ensure .env has CORS_ALLOWED_ORIGINS=http://localhost:5173.
