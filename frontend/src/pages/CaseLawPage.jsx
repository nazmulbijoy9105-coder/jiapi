import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Gavel, Landmark, Scale, Filter, Search,
  CheckCircle, XCircle, AlertCircle, ArrowUpRight
} from 'lucide-react'

const courts = [
  { id: 'ad', name: 'Appellate Division', icon: Landmark, count: 156, color: 'primary' },
  { id: 'hcd', name: 'High Court Division', icon: Scale, count: 892, color: 'secondary' },
  { id: 'tat', name: 'Tax Appellate Tribunal', icon: Gavel, count: 2340, color: 'accent' },
]

const cases = [
  {
    id: 'case-1',
    case_number: 'Civil Appeal No. 45 of 2024',
    title: 'ABC Ltd vs Commissioner of Taxes',
    court: 'Appellate Division',
    year: 2024,
    date: '2024-12-15',
    status: 'good_law',
    provisions: ['30', '45'],
    citation: '67 DLR (AD) 2024',
    summary: 'Interpretation of business expenditure deduction under Section 30 of ITA 2023'
  },
  {
    id: 'case-2',
    case_number: 'Tax Reference No. 123 of 2023',
    title: 'XYZ Corporation vs NBR',
    court: 'High Court Division',
    year: 2023,
    date: '2023-11-20',
    status: 'good_law',
    provisions: ['120', '121'],
    citation: '75 DLR 2023',
    summary: 'Transfer pricing documentation requirements under ITA 2023 Chapter XII'
  },
  {
    id: 'case-3',
    case_number: 'TAT Appeal No. 567 of 2024',
    title: 'Global Trade Ltd vs CTO',
    court: 'Tax Appellate Tribunal',
    year: 2024,
    date: '2024-10-05',
    status: 'good_law',
    provisions: ['60'],
    citation: '2024 BLT (TAT) 89',
    summary: 'Income from other sources - applicability to foreign remittances'
  },
  {
    id: 'case-4',
    case_number: 'Civil Appeal No. 12 of 2022',
    title: 'Mega Industries vs Commissioner',
    court: 'Appellate Division',
    year: 2022,
    date: '2022-08-30',
    status: 'overruled',
    provisions: ['30'],
    citation: '74 DLR (AD) 2022',
    summary: '[OVERRULED] Previous interpretation of depreciation allowance',
    overruling_case: 'Civil Appeal No. 45 of 2024'
  },
]

const statusConfig = {
  good_law: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10', label: 'Good Law' },
  overruled: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-500/10', label: 'Overruled' },
  distinguished: { icon: AlertCircle, color: 'text-amber-400', bg: 'bg-amber-500/10', label: 'Distinguished' },
  followed: { icon: CheckCircle, color: 'text-blue-400', bg: 'bg-blue-500/10', label: 'Followed' },
}

export default function CaseLawPage() {
  const [activeCourt, setActiveCourt] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Case Law Database</h1>
          <p className="text-gray-400 mt-1">Appellate Division · High Court · TAT</p>
        </div>
      </div>

      {/* Court Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {courts.map((court) => {
          const Icon = court.icon
          return (
            <button
              key={court.id}
              onClick={() => setActiveCourt(court.id)}
              className={`
                glass-card p-5 text-left hover:bg-dark-800/50 transition-all
                ${activeCourt === court.id ? 'border-primary-500/30 ring-1 ring-primary-500/20' : ''}
              `}
            >
              <div className="flex items-start justify-between mb-3">
                <div className={`w-10 h-10 rounded-xl bg-${court.color}-500/10 flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 text-${court.color}-400`} />
                </div>
                <span className="text-2xl font-bold text-white">{court.count}</span>
              </div>
              <p className="text-white font-medium">{court.name}</p>
              <p className="text-sm text-gray-500">judgments</p>
            </button>
          )
        })}
      </div>

      {/* Search & Filter */}
      <div className="glass-card p-4">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search cases by title, citation, or provision..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-field pl-12"
            />
          </div>
          <button className="btn-secondary flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      {/* Cases List */}
      <div className="space-y-3">
        {cases
          .filter(c => activeCourt === 'all' || c.court.toLowerCase().includes(activeCourt))
          .filter(c => c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                      c.citation.toLowerCase().includes(searchQuery.toLowerCase()) ||
                      c.provisions.some(p => p.includes(searchQuery)))
          .map((caseItem) => {
            const status = statusConfig[caseItem.status]
            const StatusIcon = status.icon
            return (
              <Link
                key={caseItem.id}
                to={`/case/${caseItem.id}`}
                className="glass-card p-5 hover:bg-dark-800/50 transition-all group block"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className={`badge ${status.bg} ${status.color} border border-current/20`}>
                        <StatusIcon className="w-3 h-3 inline mr-1" />
                        {status.label}
                      </span>
                      <span className="text-xs text-gray-500 font-mono">{caseItem.case_number}</span>
                    </div>
                    <h3 className="text-white font-semibold group-hover:text-primary-400 transition-colors">
                      {caseItem.title}
                    </h3>
                    <p className="text-sm text-gray-400 mt-1">{caseItem.summary}</p>
                    <div className="flex items-center gap-4 mt-3">
                      <span className="text-xs text-gray-500">{caseItem.court}</span>
                      <span className="text-xs text-gray-500">{caseItem.date}</span>
                      <span className="text-xs text-gray-500 font-mono">{caseItem.citation}</span>
                      <div className="flex gap-1">
                        {caseItem.provisions.map(p => (
                          <span key={p} className="text-xs px-2 py-0.5 bg-primary-500/10 text-primary-400 rounded">
                            Sec {p}
                          </span>
                        ))}
                      </div>
                    </div>
                    {caseItem.overruling_case && (
                      <p className="text-xs text-red-400 mt-2">
                        Overruled by: {caseItem.overruling_case}
                      </p>
                    )}
                  </div>
                  <ArrowUpRight className="w-5 h-5 text-gray-600 group-hover:text-primary-400 
                                          group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all flex-shrink-0" />
                </div>
              </Link>
            )
          })}
      </div>
    </div>
  )
}
