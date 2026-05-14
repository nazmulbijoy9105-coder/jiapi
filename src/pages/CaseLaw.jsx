import React, { useState } from 'react'
import { Gavel, Search, Filter, ChevronDown, BookOpen, Scale, AlertCircle } from 'lucide-react'

function CaseLaw() {
  const [courtFilter, setCourtFilter] = useState('all')
  const [yearFilter, setYearFilter] = useState('all')

  const courts = [
    { id: 'all', label: 'All Courts' },
    { id: 'appellate_division', label: 'Appellate Division', count: 120 },
    { id: 'high_court', label: 'High Court Division', count: 850 },
    { id: 'tat', label: 'Tax Appellate Tribunal', count: 3200 },
  ]

  const judgments = [
    {
      id: 'ad-001',
      case_number: 'Civil Appeal No. 45 of 2019',
      title: 'Commissioner of Taxes vs. Grameenphone Ltd.',
      court: 'appellate_division',
      court_name: 'Appellate Division',
      year: 2022,
      date: '2022-03-15',
      headnotes: 'Whether SIM tax is a tax on income or a regulatory fee. Held: SIM tax is not income tax but a regulatory fee under Telecommunications Act.',
      status: 'good_law',
      assessee: 'Grameenphone Ltd.',
      tax_amount: 'Tk. 25 Crore',
      sections: ['2(62)', '4'],
      era: 'pre2023',
      citation: '72 DLR (AD) 45'
    },
    {
      id: 'hcd-001',
      case_number: 'IT Reference No. 12 of 2020',
      title: 'Bangladesh Bank vs. Commissioner of Taxes',
      court: 'high_court',
      court_name: 'High Court Division',
      bench: 'Dhaka',
      year: 2021,
      date: '2021-08-20',
      headnotes: 'Whether interest on government securities is taxable. Held: Interest on T-bills is taxable under the head Interest on Securities.',
      status: 'good_law',
      assessee: 'Bangladesh Bank',
      tax_amount: 'Tk. 5 Crore',
      sections: ['19', '22'],
      era: 'pre2023',
      citation: '73 DLR 234'
    },
    {
      id: 'tat-001',
      case_number: 'TAT Appeal No. 234 of 2023',
      title: 'ABC Garments Ltd. vs. Commissioner of Taxes',
      court: 'tat',
      court_name: 'Tax Appellate Tribunal',
      bench: 'Dhaka',
      year: 2024,
      date: '2024-02-10',
      headnotes: 'Whether export cash subsidy is taxable income. Held: Export cash subsidy is taxable as business income under Section 20.',
      status: 'good_law',
      assessee: 'ABC Garments Ltd.',
      tax_amount: 'Tk. 1.5 Crore',
      sections: ['20', '30'],
      era: 'post2023',
      citation: 'TAT Dhaka 234/2023'
    },
    {
      id: 'tat-002',
      case_number: 'TAT Appeal No. 456 of 2023',
      title: 'XYZ Pharmaceuticals vs. Commissioner of Taxes',
      court: 'tat',
      court_name: 'Tax Appellate Tribunal',
      bench: 'Chittagong',
      year: 2024,
      date: '2024-05-15',
      headnotes: 'Whether R&D expenses are allowable deduction. Held: R&D expenses directly related to business are fully deductible.',
      status: 'good_law',
      assessee: 'XYZ Pharmaceuticals',
      tax_amount: 'Tk. 3 Crore',
      sections: ['28', '29'],
      era: 'post2023',
      citation: 'TAT Chittagong 456/2023'
    }
  ]

  const filteredJudgments = judgments.filter(j => {
    if (courtFilter !== 'all' && j.court !== courtFilter) return false
    if (yearFilter !== 'all' && j.year !== parseInt(yearFilter)) return false
    return true
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Case Law Database</h1>
        <p className="mt-2 text-dark-500">Appellate Division, High Court Division, and Tax Appellate Tribunal judgments</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {courts.filter(c => c.id !== 'all').map(court => (
          <div key={court.id} className="card hover:shadow-md transition-shadow cursor-pointer"
               onClick={() => setCourtFilter(court.id)}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${
                  court.id === 'appellate_division' ? 'bg-purple-100 text-purple-600' :
                  court.id === 'high_court' ? 'bg-blue-100 text-blue-600' :
                  'bg-green-100 text-green-600'
                }`}>
                  <Gavel size={20} />
                </div>
                <div>
                  <p className="font-medium text-dark-900">{court.label}</p>
                  <p className="text-sm text-dark-500">{court.count} judgments</p>
                </div>
              </div>
              <ChevronDown size={16} className="text-dark-400" />
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter size={18} className="text-dark-500" />
            <span className="text-sm font-medium text-dark-700">Filters:</span>
          </div>
          <select 
            value={courtFilter}
            onChange={(e) => setCourtFilter(e.target.value)}
            className="input-field w-auto text-sm"
          >
            {courts.map(c => (
              <option key={c.id} value={c.id}>{c.label}</option>
            ))}
          </select>
          <select 
            value={yearFilter}
            onChange={(e) => setYearFilter(e.target.value)}
            className="input-field w-auto text-sm"
          >
            <option value="all">All Years</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
          </select>
          <div className="flex-1"></div>
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" />
            <input 
              type="text" 
              placeholder="Search judgments..."
              className="input-field pl-10 text-sm w-64"
            />
          </div>
        </div>
      </div>

      {/* Judgments List */}
      <div className="space-y-4">
        {filteredJudgments.map(judgment => (
          <div key={judgment.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    judgment.court === 'appellate_division' ? 'bg-purple-100 text-purple-700' :
                    judgment.court === 'high_court' ? 'bg-blue-100 text-blue-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {judgment.court_name}
                  </span>
                  <span className="text-xs text-dark-500">{judgment.citation}</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs ${
                    judgment.status === 'good_law' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}>
                    {judgment.status === 'good_law' ? '✓ Good Law' : '✗ Overruled'}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-dark-900">{judgment.title}</h3>
                <p className="text-sm text-dark-500 mt-1">{judgment.case_number} | {judgment.date}</p>
                <p className="mt-3 text-sm text-dark-600 leading-relaxed">{judgment.headnotes}</p>
                <div className="mt-3 flex flex-wrap items-center gap-4 text-sm">
                  <span className="flex items-center gap-1 text-dark-500">
                    <Scale size={14} />
                    Assessee: {judgment.assessee}
                  </span>
                  <span className="flex items-center gap-1 text-dark-500">
                    <AlertCircle size={14} />
                    Tax: {judgment.tax_amount}
                  </span>
                  <span className="flex items-center gap-1 text-dark-500">
                    <BookOpen size={14} />
                    Sections: {judgment.sections.join(', ')}
                  </span>
                  <span className="px-2 py-0.5 bg-dark-100 rounded text-xs text-dark-600">
                    {judgment.era === 'post2023' ? 'ITA 2023' : 'ITO 1984'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CaseLaw
