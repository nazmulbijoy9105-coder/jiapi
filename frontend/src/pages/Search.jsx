import React, { useState } from 'react'
import { Search, Filter, BookOpen, Gavel, FileText, Globe, ChevronRight, X } from 'lucide-react'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState({ era: 'all', type: 'all' })
  const [hasSearched, setHasSearched] = useState(false)

  const sampleResults = [
    {
      type: 'legislation',
      icon: <BookOpen size={18} />,
      title: 'Section 30 - Deduction of tax from salaries',
      snippet: 'Any person responsible for paying any income chargeable under the head Salaries shall, at the time of payment, deduct tax...',
      highlight: 'Any person <mark>responsible</mark> for paying any income chargeable under the head Salaries shall...',
      metadata: { era: 'post2023', act: 'ITA 2023', section: '30' },
      score: 0.95
    },
    {
      type: 'case_law',
      icon: <Gavel size={18} />,
      title: 'ABC Garments Ltd. vs. Commissioner of Taxes',
      snippet: 'Export cash subsidy is taxable as business income under Section 20 of the Income Tax Act 2023...',
      highlight: 'Export cash subsidy is <mark>taxable</mark> as business income under Section 20...',
      metadata: { court: 'TAT Dhaka', year: 2024, status: 'good_law' },
      score: 0.85
    },
    {
      type: 'sro',
      icon: <FileText size={18} />,
      title: 'SRO 404-Law/2025 - Authentic English Text of ITA 2023',
      snippet: 'Official authentic English text of Income Tax Act 2023 published by National Board of Revenue...',
      highlight: 'Official <mark>authentic</mark> English text of Income Tax Act 2023 published...',
      metadata: { date: '2025-10-08', authority: 'NBR' },
      score: 0.75
    },
    {
      type: 'dtaa',
      icon: <Globe size={18} />,
      title: 'Bangladesh-UK DTAA - Article 10 (Dividends)',
      snippet: 'Dividends paid by a company which is a resident of a Contracting State to a resident of the other Contracting State...',
      highlight: 'Dividends paid by a company which is a <mark>resident</mark> of a Contracting State...',
      metadata: { country: 'UK', rate: '10%', article: 10 },
      score: 0.70
    }
  ]

  const handleSearch = (e) => {
    e.preventDefault()
    setHasSearched(true)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Search</h1>
        <p className="mt-2 text-dark-500">Full-text search across all legislation, case law, SROs, and DTAAs</p>
      </div>

      {/* Search Bar */}
      <div className="card">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="relative">
            <Search size={20} className="absolute left-4 top-1/2 -translate-y-1/2 text-dark-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search sections, cases, SROs, or DTAAs..."
              className="input-field pl-12 py-4 text-lg"
            />
            {query && (
              <button 
                type="button"
                onClick={() => setQuery('')}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-dark-600"
              >
                <X size={18} />
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter size={16} className="text-dark-500" />
              <span className="text-sm text-dark-700">Filters:</span>
            </div>
            <select 
              value={filters.era}
              onChange={(e) => setFilters({...filters, era: e.target.value})}
              className="input-field w-auto text-sm py-1.5"
            >
              <option value="all">All Eras</option>
              <option value="post2023">Post-2023 (ITA 2023)</option>
              <option value="pre2023">Pre-2023 (ITO 1984)</option>
            </select>
            <select 
              value={filters.type}
              onChange={(e) => setFilters({...filters, type: e.target.value})}
              className="input-field w-auto text-sm py-1.5"
            >
              <option value="all">All Types</option>
              <option value="legislation">Legislation</option>
              <option value="case_law">Case Law</option>
              <option value="sro">SROs</option>
              <option value="circular">Circulars</option>
              <option value="dtaa">DTAAs</option>
            </select>
            <div className="flex-1"></div>
            <button type="submit" className="btn-primary">
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Results */}
      {hasSearched && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-dark-500">
              Found <span className="font-medium text-dark-900">{sampleResults.length}</span> results 
              for "<span className="font-medium text-dark-900">{query || 'tax deduction'}</span>"
            </p>
            <div className="flex gap-2">
              <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">Relevance</span>
              <span className="px-2 py-1 bg-dark-100 text-dark-600 rounded text-xs">Date</span>
            </div>
          </div>

          {sampleResults.map((result, i) => (
            <div key={i} className="card hover:shadow-md transition-shadow cursor-pointer group">
              <div className="flex items-start gap-4">
                <div className="p-2 bg-primary-50 rounded-lg text-primary-600 mt-1">
                  {result.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium uppercase tracking-wide text-dark-400">
                      {result.type.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-dark-400">•</span>
                    <span className="text-xs text-dark-400">
                      Score: {(result.score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <h3 className="font-semibold text-dark-900 group-hover:text-primary-600 transition-colors">
                    {result.title}
                  </h3>
                  <p 
                    className="mt-2 text-sm text-dark-600 leading-relaxed"
                    dangerouslySetInnerHTML={{ 
                      __html: result.highlight.replace(/<mark>/g, '<mark class="bg-yellow-200 px-0.5 rounded">') 
                    }}
                  />
                  <div className="mt-3 flex flex-wrap gap-2">
                    {Object.entries(result.metadata).map(([key, value]) => (
                      <span key={key} className="px-2 py-1 bg-dark-100 rounded text-xs text-dark-600">
                        {key}: {value}
                      </span>
                    ))}
                  </div>
                </div>
                <ChevronRight size={18} className="text-dark-400 mt-2 group-hover:text-primary-600" />
              </div>
            </div>
          ))}
        </div>
      )}

      {!hasSearched && (
        <div className="card text-center py-12">
          <Search size={48} className="mx-auto text-dark-300 mb-4" />
          <h3 className="text-lg font-medium text-dark-700">Start searching</h3>
          <p className="mt-2 text-sm text-dark-500">
            Search by section number, case name, keyword, or legal concept.<br/>
            Supports Bengali and English text.
          </p>
        </div>
      )}
    </div>
  )
}

export default SearchPage
