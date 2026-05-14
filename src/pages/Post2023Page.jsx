import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpen, FileText, ScrollText, Building2, 
  ChevronRight, Search, Filter, ArrowUpRight
} from 'lucide-react'

const categories = [
  { id: 'ita2023', title: 'Income Tax Act 2023', icon: BookOpen, count: 187, type: 'Primary Act', color: 'primary' },
  { id: 'itr2024', title: 'Income Tax Rules 2024', icon: FileText, count: 95, type: 'Rules', color: 'secondary' },
  { id: 'finance', title: 'Finance Acts', icon: ScrollText, count: 2, type: 'Annual', color: 'accent' },
  { id: 'sros', title: 'SROs & GOs', icon: Building2, count: 234, type: 'NBR', color: 'green' },
  { id: 'circulars', title: 'Circular Letters', icon: FileText, count: 89, type: 'NBR', color: 'blue' },
  { id: 'dtaa', title: 'DTAAs', icon: Building2, count: 35, type: 'International', color: 'purple' },
  { id: 'tp', title: 'TP Regulations', icon: FileText, count: 12, type: 'NBR', color: 'orange' },
  { id: 'beps', title: 'BEPS Framework', icon: BookOpen, count: 15, type: 'OECD', color: 'pink' },
]

const sections = [
  { number: '1', title: 'Short title, extent and commencement', chapter: 'I' },
  { number: '2', title: 'Definitions', chapter: 'I' },
  { number: '3', title: 'Charge of income tax', chapter: 'II' },
  { number: '4', title: 'Scope of total income', chapter: 'II' },
  { number: '5', title: 'Residence', chapter: 'II' },
  { number: '6', title: 'Heads of income', chapter: 'III' },
  { number: '20', title: 'Salaries', chapter: 'IV' },
  { number: '30', title: 'Deductions from business income', chapter: 'V' },
  { number: '45', title: 'Capital gains', chapter: 'VI' },
  { number: '60', title: 'Income from other sources', chapter: 'VII' },
  { number: '80', title: 'Set off and carry forward of losses', chapter: 'VIII' },
  { number: '100', title: 'Assessment procedures', chapter: 'IX' },
  { number: '120', title: 'Transfer pricing', chapter: 'XII' },
  { number: '150', title: 'Appeals', chapter: 'XV' },
  { number: '180', title: 'Penalties', chapter: 'XVIII' },
]

export default function Post2023Page() {
  const [activeCategory, setActiveCategory] = useState('ita2023')
  const [searchQuery, setSearchQuery] = useState('')

  const activeCat = categories.find(c => c.id === activeCategory)
  const Icon = activeCat?.icon || BookOpen

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Post-2023 Legislation</h1>
          <p className="text-gray-400 mt-1">ITA 2023, ITR 2024, Finance Acts, SROs, DTAAs</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span className="w-2 h-2 rounded-full bg-green-500" />
          Active Era
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
                  ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20'
                  : 'bg-dark-800/50 text-gray-400 border border-white/5 hover:bg-dark-700 hover:text-white'
                }
              `}
            >
              <CatIcon className="w-4 h-4" />
              {cat.title}
              <span className={`text-xs px-1.5 py-0.5 rounded-full
                ${activeCategory === cat.id ? 'bg-primary-500/20 text-primary-300' : 'bg-dark-700 text-gray-500'}`}>
                {cat.count}
              </span>
            </button>
          )
        })}
      </div>

      {/* Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-4">
          {/* Search Bar */}
          <div className="glass-card p-4">
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

          {/* Sections List */}
          <div className="glass-card overflow-hidden">
            <div className="p-4 border-b border-white/5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl bg-${activeCat?.color}-500/10 flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 text-${activeCat?.color}-400`} />
                </div>
                <div>
                  <h2 className="text-white font-semibold">{activeCat?.title}</h2>
                  <p className="text-sm text-gray-500">{activeCat?.count} sections · {activeCat?.type}</p>
                </div>
              </div>
              <button className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                <Filter className="w-4 h-4 text-gray-400" />
              </button>
            </div>

            <div className="divide-y divide-white/5">
              {sections
                .filter(s => s.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            s.number.includes(searchQuery))
                .map((section) => (
                <Link
                  key={section.number}
                  to={`/legislation/ita-2023-sec-${section.number}`}
                  className="flex items-center justify-between p-4 hover:bg-white/5 transition-colors group"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-mono text-primary-400 bg-primary-500/10 
                                   px-3 py-1 rounded-lg min-w-[3rem] text-center">
                      {section.number}
                    </span>
                    <div>
                      <p className="text-white font-medium">{section.title}</p>
                      <p className="text-xs text-gray-500">Chapter {section.chapter}</p>
                    </div>
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-gray-600 group-hover:text-primary-400 
                                          group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                </Link>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Quick Stats */}
          <div className="glass-card p-4 space-y-4">
            <h3 className="text-white font-semibold">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Total Sections</span>
                <span className="text-white font-medium">187</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Amendments</span>
                <span className="text-white font-medium">2</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Effective From</span>
                <span className="text-white font-medium">Jul 1, 2023</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Last Updated</span>
                <span className="text-white font-medium">Jun 30, 2025</span>
              </div>
            </div>
          </div>

          {/* Related Links */}
          <div className="glass-card p-4 space-y-3">
            <h3 className="text-white font-semibold">Related</h3>
            <Link to="/diff" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
              <div className="w-8 h-8 rounded-lg bg-primary-500/10 flex items-center justify-center">
                <FileText className="w-4 h-4 text-primary-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-white">Compare with ITO 1984</p>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-white transition-colors" />
            </Link>
            <Link to="/point-in-time" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
              <div className="w-8 h-8 rounded-lg bg-secondary-500/10 flex items-center justify-center">
                <FileText className="w-4 h-4 text-secondary-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-white">View as of specific date</p>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-white transition-colors" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
