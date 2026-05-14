import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Search, Filter, BookOpen, Gavel, FileText, 
  Globe, ArrowUpRight, X
} from 'lucide-react'

const filters = [
  { id: 'all', label: 'All', count: 1247 },
  { id: 'legislation', label: 'Legislation', count: 892 },
  { id: 'caselaw', label: 'Case Law', count: 234 },
  { id: 'sro', label: 'SROs', count: 89 },
  { id: 'dtaa', label: 'DTAAs', count: 32 },
]

const searchResults = [
  {
    id: 'res-1',
    type: 'legislation',
    title: 'Section 30 - Deductions from business income',
    source: 'Income Tax Act 2023',
    excerpt: '...expenditure incurred wholly and exclusively for the purposes of the business shall be allowed as a <mark>deduction</mark> in computing the income...',
    highlights: ['deduction', 'business income'],
    url: '/legislation/ita-2023-sec-30',
    score: 0.95
  },
  {
    id: 'res-2',
    type: 'caselaw',
    title: 'ABC Ltd vs Commissioner of Taxes',
    source: 'Appellate Division · 67 DLR (AD) 2024',
    excerpt: '...the Court held that <mark>Section 30</mark> of the ITA 2023 must be interpreted purposively to allow...',
    highlights: ['Section 30', 'purposively'],
    url: '/case/case-1',
    score: 0.88
  },
  {
    id: 'res-3',
    type: 'sro',
    title: 'SRO 234/2024 - IT Sector Tax Exemption',
    source: 'NBR · SRO',
    excerpt: '...software development companies shall be entitled to <mark>tax exemption</mark> on export earnings for a period of...',
    highlights: ['tax exemption', 'export earnings'],
    url: '/post2023',
    score: 0.72
  },
]

const typeIcons = {
  legislation: BookOpen,
  caselaw: Gavel,
  sro: FileText,
  dtaa: Globe,
}

const typeColors = {
  legislation: 'primary',
  caselaw: 'secondary',
  sro: 'accent',
  dtaa: 'green',
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [activeFilter, setActiveFilter] = useState('all')
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim()) setHasSearched(true)
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Search Header */}
      <div className="text-center py-8">
        <h1 className="text-3xl font-bold text-white mb-2">Search JIAPI</h1>
        <p className="text-gray-400">Search across legislation, case law, SROs, and DTAAs</p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
        <div className="relative">
          <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-gray-500" />
          <input
            type="text"
            placeholder="Search for sections, cases, SROs, or legal concepts..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-14 pr-14 py-4 bg-dark-800 border border-white/10 rounded-2xl text-white text-lg
                     placeholder-gray-500 focus:outline-none focus:border-primary-500/50 focus:ring-2 focus:ring-primary-500/20
                     transition-all"
            autoFocus
          />
          {query && (
            <button 
              type="button"
              onClick={() => { setQuery(''); setHasSearched(false); }}
              className="absolute right-5 top-1/2 -translate-y-1/2 p-1 hover:bg-white/5 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          )}
        </div>
      </form>

      {hasSearched && (
        <>
          {/* Filters */}
          <div className="flex gap-2 justify-center flex-wrap">
            {filters.map((filter) => (
              <button
                key={filter.id}
                onClick={() => setActiveFilter(filter.id)}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium
                  transition-all duration-200
                  ${activeFilter === filter.id
                    ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20'
                    : 'bg-dark-800/50 text-gray-400 border border-white/5 hover:bg-dark-700 hover:text-white'
                  }
                `}
              >
                {filter.label}
                <span className={`text-xs px-1.5 py-0.5 rounded-full
                  ${activeFilter === filter.id ? 'bg-primary-500/20 text-primary-300' : 'bg-dark-700 text-gray-500'}`}>
                  {filter.count}
                </span>
              </button>
            ))}
          </div>

          {/* Results */}
          <div className="max-w-4xl mx-auto space-y-3">
            <p className="text-sm text-gray-500 mb-4">
              Found {searchResults.length} results for "{query}"
            </p>
            {searchResults
              .filter(r => activeFilter === 'all' || r.type === activeFilter)
              .map((result) => {
                const Icon = typeIcons[result.type]
                const color = typeColors[result.type]
                return (
                  <Link
                    key={result.id}
                    to={result.url}
                    className="glass-card p-5 hover:bg-dark-800/50 transition-all group block"
                  >
                    <div className="flex items-start gap-4">
                      <div className={`w-10 h-10 rounded-xl bg-${color}-500/10 flex items-center justify-center flex-shrink-0`}>
                        <Icon className={`w-5 h-5 text-${color}-400`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`text-xs px-2 py-0.5 rounded-full bg-${color}-500/10 text-${color}-400 capitalize`}>
                            {result.type}
                          </span>
                          <span className="text-xs text-gray-500">{result.source}</span>
                        </div>
                        <h3 className="text-white font-semibold group-hover:text-primary-400 transition-colors">
                          {result.title}
                        </h3>
                        <p 
                          className="text-sm text-gray-400 mt-2 leading-relaxed"
                          dangerouslySetInnerHTML={{ 
                            __html: result.excerpt.replace(/<mark>/g, '<span class="search-highlight">').replace(/<\/mark>/g, '</span>') 
                          }}
                        />
                        <div className="flex items-center gap-2 mt-3">
                          {result.highlights.map((h, i) => (
                            <span key={i} className="text-xs px-2 py-0.5 bg-dark-700 text-gray-400 rounded">
                              {h}
                            </span>
                          ))}
                        </div>
                      </div>
                      <ArrowUpRight className="w-5 h-5 text-gray-600 group-hover:text-primary-400 flex-shrink-0" />
                    </div>
                  </Link>
                )
              })}
          </div>
        </>
      )}
    </div>
  )
}
