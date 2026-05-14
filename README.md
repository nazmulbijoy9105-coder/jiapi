# JIAPI - Justice & Income API 🇧🇩

> **Commercial-Grade Bangladesh Tax Law Database API**
> Post-2023 Era | Pre-2023 Era | Case Law | International Treaties

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-00a393.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://react.dev)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg)](https://vercel.com)

---

## 🚀 Deploy to Vercel via Git Bash (Windows)

### Step 1: Open Git Bash
Right-click in your project folder → **"Git Bash Here"**

### Step 2: Initialize Git & Push to GitHub
```bash
# Navigate to project (if not already there)
cd jiapi

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "JIAPI v1.0 - Bangladesh Tax Law Database API"

# Rename branch to main (Git default now uses main)
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/jiapi.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy to Vercel
```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel (first time only)
vercel login

# Deploy to production
vercel --prod
```

Or use the **Vercel Dashboard**:
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your `jiapi` GitHub repo
3. Click **Deploy** ✅

---

## 🌐 Live URLs After Deployment

| Endpoint | URL |
|----------|-----|
| **Dashboard** | `https://your-project.vercel.app` |
| **API Docs** | `https://your-project.vercel.app/docs` |
| **API Base** | `https://your-project.vercel.app/api/v1` |

---

## 📋 Architecture

```
JIAPI PLATFORM
├── Post-2023 API    (ITA 2023, ITR 2024, Finance Acts)
├── Pre-2023 API     (ITO 1984, Historical)
├── Case Law API     (AD, HCD, TAT Judgments)
├── DTAA Database    (35+ Treaties)
├── Amendment Engine (Point-in-Time + Diff)
└── Search           (Full-Text, Bengali + English)
```

---

## 🔑 Core Features

| Feature | Description |
|---------|-------------|
| **Point-in-Time Queries** | Get law text as it existed on any date |
| **Diff Engine** | Compare legislation across time periods |
| **Amendment Tracking** | Every change traced to its source |
| **Citation Network** | Link case law to legislation sections |
| **Full-Text Search** | Bengali + English across all content |
| **Webhook Alerts** | Real-time notifications on law changes |

---

## 🆓 Free Tier

| Service | Free Limit |
|---------|-----------|
| **Vercel** | 100GB bandwidth/month |
| **SQLite** | Persistent per-deployment |
| **GitHub** | Unlimited public repos |

---

**Built with ❤️ for Bangladesh Tax & Legal Community**
