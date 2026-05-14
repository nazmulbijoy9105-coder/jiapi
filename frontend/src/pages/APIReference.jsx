import React, { useState } from 'react'
import { Code, Copy, CheckCircle, Terminal, Globe, Lock, Zap } from 'lucide-react'

function APIReference() {
  const [copied, setCopied] = useState(false)
  const [activeEndpoint, setActiveEndpoint] = useState('post2023-ita')

  const endpoints = [
    { id: 'post2023-ita', method: 'GET', path: '/api/v1/post2023/acts/ita2023', desc: 'Get ITA 2023 full act', category: 'Post-2023' },
    { id: 'post2023-section', method: 'GET', path: '/api/v1/post2023/acts/ita2023/sections/{num}', desc: 'Get specific section', category: 'Post-2023' },
    { id: 'post2023-finance', method: 'GET', path: '/api/v1/post2023/finance-acts', desc: 'List Finance Acts', category: 'Post-2023' },
    { id: 'pre2023-ito', method: 'GET', path: '/api/v1/pre2023/acts/ito1984', desc: 'Get ITO 1984 (repealed)', category: 'Pre-2023' },
    { id: 'caselaw-ad', method: 'GET', path: '/api/v1/caselaw/judgments/appellate-division', desc: 'AD judgments', category: 'Case Law' },
    { id: 'caselaw-hcd', method: 'GET', path: '/api/v1/caselaw/judgments/high-court', desc: 'HCD judgments', category: 'Case Law' },
    { id: 'caselaw-tat', method: 'GET', path: '/api/v1/caselaw/judgments/tat', desc: 'TAT decisions', category: 'Case Law' },
    { id: 'dtaa-list', method: 'GET', path: '/api/v1/dtaas', desc: 'List all DTAAs', category: 'DTAA' },
    { id: 'dtaa-detail', method: 'GET', path: '/api/v1/dtaas/{country_code}', desc: 'Get specific DTAA', category: 'DTAA' },
    { id: 'search', method: 'GET', path: '/api/v1/search?q={query}', desc: 'Full-text search', category: 'Search' },
    { id: 'amendments', method: 'GET', path: '/api/v1/amendments', desc: 'List amendments', category: 'Amendments' },
    { id: 'sros', method: 'GET', path: '/api/v1/sros', desc: 'List SROs', category: 'SROs' },
    { id: 'circulars', method: 'GET', path: '/api/v1/circulars', desc: 'List circulars', category: 'Circulars' },
  ]

  const codeExample = `curl -X GET \
  'https://api.jiapi.com/api/v1/post2023/acts/ita2023/sections/30' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json'

# Response
{
  "id": "sec-30",
  "numbering": "30",
  "heading_en": "Deduction of tax from salaries",
  "text_current": "Any person responsible for paying...",
  "effective_from": "2023-07-01",
  "cross_references": [
    {"section": "31", "act": "ITA 2023"}
  ]
}`

  const copyCode = () => {
    navigator.clipboard.writeText(codeExample)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">API Reference</h1>
        <p className="mt-2 text-dark-500">Complete documentation for JIAPI endpoints</p>
      </div>

      {/* Auth Info */}
      <div className="card bg-dark-900 text-white">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-primary-600 rounded-lg">
            <Lock size={24} />
          </div>
          <div>
            <h2 className="text-lg font-bold">Authentication</h2>
            <p className="mt-2 text-sm text-dark-300">
              All endpoints require Bearer JWT token or API key in the Authorization header.
            </p>
            <div className="mt-4 p-3 bg-dark-800 rounded-lg font-mono text-sm">
              Authorization: Bearer {'<your_jwt_token>'}
            </div>
          </div>
        </div>
      </div>

      {/* Rate Limits */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        {[
          { tier: 'Free', requests: '100/day', price: 'Free', icon: <Zap size={20} /> },
          { tier: 'Basic', requests: '1,000/day', price: 'BDT 2,000/mo', icon: <Zap size={20} /> },
          { tier: 'Pro', requests: '10,000/day', price: 'BDT 8,000/mo', icon: <Zap size={20} /> },
          { tier: 'Enterprise', requests: 'Unlimited', price: 'Custom', icon: <Zap size={20} /> },
        ].map(plan => (
          <div key={plan.tier} className="card text-center">
            <div className="text-primary-600 mx-auto mb-2">{plan.icon}</div>
            <p className="font-bold text-dark-900">{plan.tier}</p>
            <p className="text-2xl font-bold text-primary-600 mt-1">{plan.requests}</p>
            <p className="text-sm text-dark-500 mt-1">{plan.price}</p>
          </div>
        ))}
      </div>

      {/* Endpoints */}
      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Endpoints</h3>
        <div className="space-y-2">
          {endpoints.map(ep => (
            <div 
              key={ep.id}
              onClick={() => setActiveEndpoint(ep.id)}
              className={`p-3 rounded-lg cursor-pointer transition-colors ${
                activeEndpoint === ep.id ? 'bg-primary-50 border border-primary-200' : 'hover:bg-dark-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  ep.method === 'GET' ? 'bg-green-100 text-green-700' :
                  ep.method === 'POST' ? 'bg-blue-100 text-blue-700' :
                  ep.method === 'PUT' ? 'bg-amber-100 text-amber-700' :
                  'bg-red-100 text-red-700'
                }`}>
                  {ep.method}
                </span>
                <code className="text-sm text-dark-900">{ep.path}</code>
                <span className="text-xs text-dark-500">{ep.desc}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Code Example */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-dark-900">Example Request</h3>
          <button 
            onClick={copyCode}
            className="flex items-center gap-2 px-3 py-1.5 bg-dark-100 rounded-lg text-sm hover:bg-dark-200 transition-colors"
          >
            {copied ? <CheckCircle size={16} className="text-green-600" /> : <Copy size={16} />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
        <pre className="p-4 bg-dark-900 text-green-400 rounded-lg overflow-x-auto text-sm font-mono">
          {codeExample}
        </pre>
      </div>
    </div>
  )
}

export default APIReference
