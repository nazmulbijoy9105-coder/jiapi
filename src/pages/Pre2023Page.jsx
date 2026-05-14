import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Archive, FileText, ScrollText, Building2, 
  ChevronRight, Search, AlertTriangle
} from 'lucide-react'

const categories = [
  { id: 'ito1984', title: 'Income Tax Ordinance 1984', icon: Archive, count: 164, type: 'Primary Act', color: 'gray' },
  { id: 'finance', title: 'Finance Acts 1984-2023', icon: ScrollText, count: 40, type: 'Annual', color: 'accent' },
  { id: 'sros', title: 'Historical SROs', icon: Building2, count: 1200, type: 'NBR', color: 'green' },
  { id: 'circulars', title: 'Historical Circulars', icon: FileText, count: 450, type: 'NBR', color: 'blue' },
  { id: 'dtaa', title: 'Pre-2023 DTAA Versions', icon: Building2, count: 28, type: 'International', color: 'purple' },
]

const financeActs = [
  { year: 2023, title: 'Finance Act, 2023', sections_amended: 15, status: 'superseded' },
  { year: 2022, title: 'Finance Act, 2022', sections_amended: 12, status: 'historical' },
  { year: 2021, title: 'Finance Act, 2021', sections_amended: 8, status: 'historical' },
  { year: 2020, title: 'Finance Act, 2020', sections_amended: 20, status: 'historical' },
  { year: 2019, title: 'Finance Act, 2019', sections_amended: 10, status: 'historical' },
]

export default function Pre2023Page() {
  const [activeCategory, setActiveCategory] = useState('ito1984')
  const [searchQuery, setSearchQuery] = useState('')

  const activeCat = categories.find(c => c.id === activeCategory)

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Pre-2023 Legislation</h1>
          <p className="text-gray-400 mt-1">ITO 1984 archive, historical Finance Acts, SROs</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-amber-500">
          <AlertTriangle className="w-4 h-4" />
          Archive Era
        </div>
      </div>

      {/* Archive Banner */}
      <div className="rounded-2xl bg-amber-500/10 border border-amber-500/20 p-4 flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-amber-200 font-medium">Historical Archive</p>
          <p className="text-sm text-amber-200/70 mt-1">
            These laws were superseded by ITA 2023 on July 1, 2023. They remain relevant for 
            pending assessments, appeals, and litigation filed under the old regime.
          </p>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {categories.map((cat) => {
          const CatIcon = cat.icon
          return (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`
                flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap
                transition-all duration-200
                ${activeCategory === cat.id
                  ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  : 'bg-dark-800/50 text-gray-400 border border-white/5 hover:bg-dark-700 hover:text-white'
                }
              `}
            >
              <CatIcon className="w-4 h-4" />
              {cat.title}
              <span className={`text-xs px-1.5 py-0.5 rounded-full
                ${activeCategory === cat.id ? 'bg-amber-500/20 text-amber-300' : 'bg-dark-700 text-gray-500'}`}>
                {cat.count}
              </span>
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="glass-card overflow-hidden">
        <div className="p-4 border-b border-white/5">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder={`Search ${activeCat?.title}...`}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-field pl-12"
            />
          </div>
        </div>

        {activeCategory === 'finance' && (
          <div className="divide-y divide-white/5">
            {financeActs
              .filter(f => f.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          f.year.toString().includes(searchQuery))
              .map((act) => (
              <div key={act.year} className="flex items-center justify-between p-4 hover:bg-white/5 transition-colors">
                <div className="flex items-center gap-4">
                  <span className="text-sm font-mono text-amber-400 bg-amber-500/10 
                                 px-3 py-1 rounded-lg min-w-[4rem] text-center">
                    {act.year}
                  </span>
                  <div>
                    <p className="text-white font-medium">{act.title}</p>
                    <p className="text-xs text-gray-500">{act.sections_amended} sections amended</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full
                  ${act.status === 'superseded' ? 'bg-red-500/10 text-red-400' : 'bg-gray-500/10 text-gray-400'}`}>
                  {act.status}
                </span>
              </div>
            ))}
          </div>
        )}

        {activeCategory === 'ito1984' && (
          <div className="p-8 text-center">
            <Archive className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <p className="text-white font-medium">Income Tax Ordinance 1984</p>
            <p className="text-sm text-gray-500 mt-2 max-w-md mx-auto">
              Full text of ITO 1984 with all amendments up to FY 2022-23. 
              Use point-in-time queries to view as of any historical date.
            </p>
            <Link to="/point-in-time" className="btn-secondary inline-flex items-center gap-2 mt-4">
              View Point-in-Time
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
