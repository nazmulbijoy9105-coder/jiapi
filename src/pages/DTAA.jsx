import React, { useState } from 'react'
import { Globe, Search, ChevronRight, ArrowRightLeft, Percent, FileText } from 'lucide-react'

function DTAA() {
  const [selectedCountry, setSelectedCountry] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  const countries = [
    { code: 'GBR', name: 'United Kingdom', signed: '1980-08-08', effective: '1980-01-01', dividend: 10, interest: 7.5, royalty: 10, technical: 7.5, method: 'credit', comprehensive: true },
    { code: 'USA', name: 'United States', signed: '2004-09-26', effective: '2006-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'IND', name: 'India', signed: '1991-07-10', effective: '1992-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'CAN', name: 'Canada', signed: '1982-10-15', effective: '1983-01-01', dividend: 15, interest: 15, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'SGP', name: 'Singapore', signed: '2004-12-09', effective: '2005-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'MYS', name: 'Malaysia', signed: '1998-12-22', effective: '1999-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'THA', name: 'Thailand', signed: '2005-11-10', effective: '2006-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'LKA', name: 'Sri Lanka', signed: '1983-03-22', effective: '1984-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'PAK', name: 'Pakistan', signed: '1989-12-20', effective: '1990-01-01', dividend: 15, interest: 15, royalty: 15, technical: 15, method: 'credit', comprehensive: true },
    { code: 'SAU', name: 'Saudi Arabia', signed: '2017-03-28', effective: '2018-01-01', dividend: 10, interest: 7.5, royalty: 10, technical: 7.5, method: 'credit', comprehensive: true },
    { code: 'ARE', name: 'UAE', signed: '2011-01-17', effective: '2012-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'KOR', name: 'South Korea', signed: '1983-05-10', effective: '1984-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'JPN', name: 'Japan', signed: '1991-11-10', effective: '1992-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'CHN', name: 'China', signed: '1996-09-04', effective: '1997-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
    { code: 'TUR', name: 'Turkey', signed: '2011-06-22', effective: '2012-01-01', dividend: 10, interest: 10, royalty: 10, technical: 10, method: 'credit', comprehensive: true },
  ]

  const filteredCountries = countries.filter(c => 
    c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.code.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const selected = countries.find(c => c.code === selectedCountry)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Double Taxation Avoidance Agreements</h1>
        <p className="mt-2 text-dark-500">35+ active treaties with withholding rates and key provisions</p>
      </div>

      {!selectedCountry ? (
        <>
          {/* Search */}
          <div className="card">
            <div className="relative">
              <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by country name or code..."
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Countries Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredCountries.map(country => (
              <div 
                key={country.code}
                onClick={() => setSelectedCountry(country.code)}
                className="card hover:shadow-lg transition-all cursor-pointer group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary-50 rounded-lg flex items-center justify-center 
                                    text-primary-700 font-bold text-sm">
                      {country.code}
                    </div>
                    <div>
                      <h3 className="font-medium text-dark-900">{country.name}</h3>
                      <p className="text-xs text-dark-500">Effective: {country.effective}</p>
                    </div>
                  </div>
                  <ChevronRight size={18} className="text-dark-400 group-hover:text-primary-600" />
                </div>
                <div className="mt-4 grid grid-cols-4 gap-2">
                  <div className="text-center p-2 bg-dark-50 rounded">
                    <p className="text-lg font-bold text-dark-900">{country.dividend}%</p>
                    <p className="text-xs text-dark-500">Dividend</p>
                  </div>
                  <div className="text-center p-2 bg-dark-50 rounded">
                    <p className="text-lg font-bold text-dark-900">{country.interest}%</p>
                    <p className="text-xs text-dark-500">Interest</p>
                  </div>
                  <div className="text-center p-2 bg-dark-50 rounded">
                    <p className="text-lg font-bold text-dark-900">{country.royalty}%</p>
                    <p className="text-xs text-dark-500">Royalty</p>
                  </div>
                  <div className="text-center p-2 bg-dark-50 rounded">
                    <p className="text-lg font-bold text-dark-900">{country.technical}%</p>
                    <p className="text-xs text-dark-500">Tech Svcs</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      ) : (
        /* Country Detail */
        <div className="space-y-6">
          <button 
            onClick={() => setSelectedCountry(null)}
            className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700"
          >
            <ChevronRight size={16} className="rotate-180" />
            Back to all treaties
          </button>

          <div className="card">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center text-white text-xl font-bold">
                {selected.code}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-dark-900">{selected.name}</h2>
                <p className="text-dark-500">Double Taxation Avoidance Agreement</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="p-4 bg-dark-100 rounded-lg">
                <p className="text-sm text-dark-500">Signed Date</p>
                <p className="font-medium text-dark-900">{selected.signed}</p>
              </div>
              <div className="p-4 bg-dark-100 rounded-lg">
                <p className="text-sm text-dark-500">Effective Date</p>
                <p className="font-medium text-dark-900">{selected.effective}</p>
              </div>
              <div className="p-4 bg-dark-100 rounded-lg">
                <p className="text-sm text-dark-500">Relief Method</p>
                <p className="font-medium text-dark-900 capitalize">{selected.method}</p>
              </div>
            </div>

            <h3 className="text-lg font-semibold text-dark-900 mb-4">Withholding Tax Rates</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Dividends', rate: selected.dividend, icon: <Percent size={20} /> },
                { label: 'Interest', rate: selected.interest, icon: <Percent size={20} /> },
                { label: 'Royalties', rate: selected.royalty, icon: <Percent size={20} /> },
                { label: 'Technical Services', rate: selected.technical, icon: <Percent size={20} /> },
              ].map(item => (
                <div key={item.label} className="card bg-primary-50 border-primary-200 text-center">
                  <div className="text-primary-600 mx-auto mb-2">{item.icon}</div>
                  <p className="text-3xl font-bold text-dark-900">{item.rate}%</p>
                  <p className="text-sm text-dark-600 mt-1">{item.label}</p>
                </div>
              ))}
            </div>

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-dark-900 mb-4">Key Articles</h3>
              <div className="space-y-3">
                {[
                  { art: 1, title: 'Persons Covered', text: 'This Agreement shall apply to persons who are residents of one or both of the Contracting States.' },
                  { art: 4, title: 'Resident', text: 'For the purposes of this Agreement, the term resident of a Contracting State means any person who, under the laws of that State, is liable to tax therein.' },
                  { art: 5, title: 'Permanent Establishment', text: 'For the purposes of this Agreement, the term permanent establishment means a fixed place of business through which the business of an enterprise is wholly or partly carried on.' },
                  { art: 9, title: 'Associated Enterprises', text: 'Where conditions are made or imposed between associated enterprises which differ from those which would be made between independent enterprises, profits may be included in the profits of the enterprise and taxed accordingly.' },
                  { art: 23, title: 'Elimination of Double Taxation', text: 'Double taxation shall be eliminated by allowing a credit against the tax of the residence State.' },
                ].map(article => (
                  <div key={article.art} className="p-4 bg-dark-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                        Article {article.art}
                      </span>
                      <span className="font-medium text-dark-900">{article.title}</span>
                    </div>
                    <p className="text-sm text-dark-600">{article.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DTAA
