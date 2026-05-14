import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, ChevronRight, FileText, Calendar, AlertCircle, ExternalLink, TrendingUp } from 'lucide-react'

function Post2023() {
  const [activeTab, setActiveTab] = useState('ita2023')

  const tabs = [
    { id: 'ita2023', label: 'ITA 2023', icon: <BookOpen size={18} /> },
    { id: 'itr2024', label: 'ITR 2024', icon: <FileText size={18} /> },
    { id: 'finance', label: 'Finance Acts', icon: <Calendar size={18} /> },
    { id: 'cross', label: 'Cross-Reference', icon: <ExternalLink size={18} /> },
  ]

  const ita2023Sections = [
    { num: '30', title: 'Deduction of tax from salaries', type: 'TDS', keywords: ['employer', 'salary', 'withholding'] },
    { num: '31', title: 'Deduction from interest on securities', type: 'TDS', keywords: ['securities', 'interest'] },
    { num: '32', title: 'Deduction from interest other than securities', type: 'TDS', keywords: ['interest', 'bank'] },
    { num: '89', title: 'Deduction from payment to contractors', type: 'TDS', keywords: ['contractor', 'construction'] },
    { num: '90', title: 'Deduction from payment to suppliers', type: 'TDS', keywords: ['supplier', 'goods'] },
    { num: '124', title: 'Deduction from service charges/fees', type: 'TDS', keywords: ['service', 'professional'] },
    { num: '128', title: 'Deduction from lease of property', type: 'TDS', keywords: ['rent', 'lease'] },
    { num: '134', title: 'Transfer of shares (non-listed)', type: 'Capital Gains', keywords: ['shares', 'transfer'] },
    { num: '135', title: 'Transfer of securities', type: 'Capital Gains', keywords: ['securities', 'sponsor'] },
    { num: '163', title: 'Minimum tax', type: 'Computation', keywords: ['minimum', 'turnover'] },
    { num: '178', title: 'Return of income', type: 'Compliance', keywords: ['return', 'filing'] },
    { num: '233', title: 'Transfer pricing - International', type: 'TP', keywords: ['transfer pricing', 'OECD'] },
    { num: '234', title: 'Computation of arm\'s length price', type: 'TP', keywords: ['arm\'s length', 'methods'] },
    { num: '235', title: 'Documentation requirements', type: 'TP', keywords: ['documentation', 'master file'] },
  ]

  const financeActs = [
    { year: 2025, title: 'Finance Act, 2025', changes: ['Corporate rate 27.5%', 'Min tax carry forward', 'Banking channel 2.5%'], effective: '2025-07-01' },
    { year: 2024, title: 'Finance Act, 2024', changes: ['New slab rates', 'Digital service tax', 'Green tax credit'], effective: '2024-07-01' },
    { year: 2023, title: 'Finance Act, 2023', changes: ['Initial ITA 2023 rates', 'Transitional provisions'], effective: '2023-07-01' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-dark-900">Post-2023 Legislation</h1>
          <p className="mt-2 text-dark-500">Income Tax Act 2023, Rules 2024, and Finance Acts</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg text-sm font-medium">
          <AlertCircle size={16} />
          Active Era
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-dark-200">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id 
                ? 'border-primary-600 text-primary-600' 
                : 'border-transparent text-dark-500 hover:text-dark-700'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* ITA 2023 Content */}
      {activeTab === 'ita2023' && (
        <div className="space-y-6">
          <div className="card bg-primary-50 border-primary-200">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-primary-600 rounded-lg text-white">
                <BookOpen size={24} />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-bold text-dark-900">Income Tax Act, 2023</h2>
                <p className="mt-1 text-sm text-dark-600">Act No. XII of 2023 | Effective: July 1, 2023</p>
                <p className="mt-2 text-sm text-dark-500">
                  Replaced ITO 1984 entirely. 345 sections, 7 schedules. 
                  Authentic English text published via SRO 404-Law/2025.
                </p>
                <div className="mt-4 flex gap-3">
                  <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-primary-700">
                    345 Sections
                  </span>
                  <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-primary-700">
                    7 Schedules
                  </span>
                  <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-primary-700">
                    35+ DTAAs
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <h3 className="text-lg font-semibold text-dark-900 mb-4">Key Sections</h3>
              <div className="space-y-2">
                {ita2023Sections.map(section => (
                  <div key={section.num} className="card py-4 hover:shadow-md transition-shadow cursor-pointer group">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center 
                                         text-primary-700 font-bold text-sm">
                          {section.num}
                        </span>
                        <div>
                          <h4 className="font-medium text-dark-900 group-hover:text-primary-600 transition-colors">
                            {section.title}
                          </h4>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs px-2 py-0.5 bg-dark-100 rounded text-dark-600">
                              {section.type}
                            </span>
                            {section.keywords.map(k => (
                              <span key={k} className="text-xs text-dark-400">{k}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                      <ChevronRight size={18} className="text-dark-400 group-hover:text-primary-600" />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <div className="card">
                <h3 className="font-semibold text-dark-900 mb-3">Quick Links</h3>
                <div className="space-y-2">
                  <Link to="/tax-rates" className="flex items-center gap-2 p-2 rounded-lg hover:bg-dark-50 text-sm">
                    <TrendingUp size={16} className="text-primary-600" />
                    Tax Rates & Slabs
                  </Link>
                  <Link to="/tp-regulations" className="flex items-center gap-2 p-2 rounded-lg hover:bg-dark-50 text-sm">
                    <Scale size={16} className="text-primary-600" />
                    Transfer Pricing
                  </Link>
                  <Link to="/amendments" className="flex items-center gap-2 p-2 rounded-lg hover:bg-dark-50 text-sm">
                    <AlertCircle size={16} className="text-primary-600" />
                    Latest Amendments
                  </Link>
                </div>
              </div>

              <div className="card bg-amber-50 border-amber-200">
                <div className="flex items-center gap-2 text-amber-700 mb-2">
                  <AlertCircle size={18} />
                  <span className="font-medium">Important Notice</span>
                </div>
                <p className="text-sm text-amber-800">
                  SRO 404-Law/2025 published the authentic English text of ITA 2023 on October 8, 2025. 
                  Always verify against official Gazette before filing.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Finance Acts */}
      {activeTab === 'finance' && (
        <div className="space-y-4">
          {financeActs.map(act => (
            <div key={act.year} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-dark-900">{act.title}</h3>
                  <p className="text-sm text-dark-500 mt-1">Effective: {act.effective}</p>
                </div>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                  FY {act.year}-{act.year+1}
                </span>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {act.changes.map((change, i) => (
                  <span key={i} className="px-3 py-1.5 bg-dark-100 rounded-lg text-sm text-dark-700">
                    {change}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'itr2024' && (
        <div className="card">
          <h3 className="text-lg font-semibold text-dark-900">Income Tax Rules, 2024</h3>
          <p className="mt-2 text-dark-500">Supporting rules for ITA 2023 implementation.</p>
          <div className="mt-4 p-4 bg-dark-100 rounded-lg">
            <p className="text-sm text-dark-600">Coming soon: Full rules text with forms and procedures.</p>
          </div>
        </div>
      )}

      {activeTab === 'cross' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="card">
            <h3 className="font-semibold text-dark-900">VAT Act 2012</h3>
            <p className="mt-2 text-sm text-dark-500">Cross-reference for business income adjustments</p>
          </div>
          <div className="card">
            <h3 className="font-semibold text-dark-900">Customs Act 1969</h3>
            <p className="mt-2 text-sm text-dark-500">Cross-reference for import income adjustments</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Post2023
