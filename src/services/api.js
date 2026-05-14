// JIAPI Frontend Service - Production URLs
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://jiapi.vercel.app/api/v1'

class APIService {
  constructor() {
    this.baseURL = API_BASE_URL
    this.headers = {
      'Content-Type': 'application/json',
    }
  }

  setToken(token) {
    this.headers['Authorization'] = `Bearer ${token}`
  }

  async get(endpoint) {
    const res = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: this.headers,
    })
    return res.json()
  }

  async post(endpoint, data) {
    const res = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(data),
    })
    return res.json()
  }
}

export const api = new APIService()

// Post-2023 API
export const post2023API = {
  getITA2023: () => api.get('/post2023/acts/ita2023'),
  getSection: (num) => api.get(`/post2023/acts/ita2023/sections/${num}`),
  getFinanceActs: () => api.get('/post2023/finance-acts'),
  getTaxRates: (year) => api.get(`/post2023/tax-rates/individual?assessment_year=${year}`),
  getCorporateRates: (year) => api.get(`/post2023/tax-rates/corporate?assessment_year=${year}`),
  getWithholdingRates: () => api.get('/post2023/withholding-rates'),
  getTPRegulations: () => api.get('/post2023/tp-regulations'),
  getBEPS: () => api.get('/post2023/beps'),
  getCompliance: () => api.get('/post2023/compliance-manual'),
  getAmendmentFeed: () => api.get('/post2023/amendments/feed'),
  pointInTime: (data) => api.post('/post2023/point-in-time', data),
  diff: (data) => api.post('/post2023/diff', data),
}

// Pre-2023 API
export const pre2023API = {
  getITO1984: () => api.get('/pre2023/acts/ito1984'),
  getSection: (num) => api.get(`/pre2023/acts/ito1984/sections/${num}`),
  getFinanceActs: () => api.get('/pre2023/finance-acts'),
}

// Case Law API
export const caseLawAPI = {
  getAD: () => api.get('/caselaw/judgments/appellate-division'),
  getHCD: () => api.get('/caselaw/judgments/high-court'),
  getTAT: () => api.get('/caselaw/judgments/tat'),
  search: (q) => api.get(`/caselaw/search?q=${encodeURIComponent(q)}`),
  checkCitation: (citation) => api.get(`/caselaw/citation-checker?citation=${encodeURIComponent(citation)}`),
}

// DTAA API
export const dtaaAPI = {
  list: () => api.get('/dtaas'),
  get: (code) => api.get(`/dtaas/${code}`),
  getRates: (code) => api.get(`/dtaas/${code}/withholding-rates`),
}

// Search API
export const searchAPI = {
  search: (q, filters = {}) => {
    const params = new URLSearchParams({ q, ...filters })
    return api.get(`/search?${params}`)
  },
}

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}
