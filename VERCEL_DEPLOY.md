# JIAPI - Vercel Deployment Guide (Git Bash)

## 🚀 Deploy via Git Bash on Windows

### Prerequisites
- [Git for Windows](https://git-scm.com/download/win) installed
- [Node.js](https://nodejs.org) installed
- Vercel account (free at [vercel.com](https://vercel.com))

---

## Step 1: Open Git Bash

Right-click in your `jiapi` folder → **"Git Bash Here"**

---

## Step 2: Push to GitHub

```bash
# 1. Navigate to project (if not already there)
cd jiapi

# 2. Initialize git repository
git init

# 3. Stage all files
git add .

# 4. Commit
git commit -m "JIAPI v1.0 - Bangladesh Tax Law Database API"

# 5. Rename branch to main (modern Git default)
git branch -M main

# 6. Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/jiapi.git

# 7. Push to GitHub
git push -u origin main
```

---

## Step 3: Install Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel (opens browser)
vercel login
```

---

## Step 4: Deploy to Vercel

```bash
# Deploy to production
vercel --prod

# Or deploy and get preview URL first
vercel
```

Vercel will auto-detect:
- `vercel.json` for routing
- `backend/app/main.py` for Python API
- `frontend/package.json` for React build

---

## Step 5: Set Environment Variables

After first deploy, go to Vercel Dashboard:

1. Open your project at [vercel.com/dashboard](https://vercel.com/dashboard)
2. Go to **Settings** → **Environment Variables**
3. Add:

| Variable | Value | Environment |
|----------|-------|-------------|
| `SECRET_KEY` | `your-32-char-secret-key-here` | Production |
| `DEBUG` | `false` | Production |

4. Click **Save** and redeploy if needed

---

## 🌐 Your Live URLs

After deployment:

| URL | Purpose |
|-----|---------|
| `https://jiapi-xxx.vercel.app` | Main Dashboard |
| `https://jiapi-xxx.vercel.app/docs` | Swagger API Docs |
| `https://jiapi-xxx.vercel.app/api/v1` | API Base |

---

## 📁 Project Structure

```
jiapi/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry (Vercel Python function)
│   │   ├── core/                # Config, Security, Auth
│   │   ├── models/              # All DB models (ITA 2023, ITO 1984, etc.)
│   │   ├── routers/             # All API endpoints
│   │   └── schemas/             # Pydantic schemas
│   └── requirements.txt         # Lightweight deps (SQLite)
├── frontend/
│   ├── src/
│   │   ├── services/api.js      # Production API URLs
│   │   ├── pages/               # All React pages
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js           # Production build
├── vercel.json                  # Vercel routing & builds
└── .env.vercel                  # Environment template
```

---

## 🔑 API Endpoints (Live)

### Post-2023 (ITA 2023)
- `GET /api/v1/post2023/acts/ita2023` — Full ITA 2023
- `GET /api/v1/post2023/acts/ita2023/sections/{num}` — Specific section
- `GET /api/v1/post2023/finance-acts` — Finance Acts
- `GET /api/v1/post2023/tax-rates/individual` — Individual tax rates
- `GET /api/v1/post2023/tax-rates/corporate` — Corporate tax rates
- `GET /api/v1/post2023/withholding-rates` — TDS rates
- `GET /api/v1/post2023/tp-regulations` — Transfer Pricing
- `GET /api/v1/post2023/beps` — BEPS framework
- `GET /api/v1/post2023/compliance-manual` — NBR Manual
- `GET /api/v1/post2023/amendments/feed` — Amendment feed

### Pre-2023 (ITO 1984)
- `GET /api/v1/pre2023/acts/ito1984` — Full ITO 1984
- `GET /api/v1/pre2023/acts/ito1984/sections/{num}` — Section
- `GET /api/v1/pre2023/finance-acts` — Historical Finance Acts

### Case Law
- `GET /api/v1/caselaw/judgments/appellate-division`
- `GET /api/v1/caselaw/judgments/high-court`
- `GET /api/v1/caselaw/judgments/tat`
- `GET /api/v1/caselaw/search?q={query}`
- `GET /api/v1/caselaw/citation-checker?citation={citation}`

### DTAA
- `GET /api/v1/dtaas` — List all treaties
- `GET /api/v1/dtaas/{country_code}` — Specific treaty

### Search & More
- `GET /api/v1/search?q={query}` — Global search
- `GET /api/v1/amendments` — Amendment tracker
- `GET /api/v1/sros` — SROs
- `GET /api/v1/circulars` — Circulars

---

## 🆓 Free Tier Limits

| Service | Free Limit |
|---------|-----------|
| Vercel Hosting | 100GB bandwidth/month |
| Vercel Functions | 100GB-hours/month |
| SQLite DB | Persistent per-deployment |
| API Requests | Unlimited |

---

## 🔧 Troubleshooting

### Git push rejected?
```bash
git pull origin main --rebase
git push origin main
```

### Vercel deploy fails?
```bash
# Check vercel.json is valid
vercel --debug
```

### Need to update after changes?
```bash
git add .
git commit -m "Update description"
git push origin main
vercel --prod
```

---

**Built with ❤️ for Bangladesh Tax & Legal Community**
