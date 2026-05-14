import React, { useState } from 'react'
import { Globe, Search, ArrowUpRight, Percent } from 'lucide-react'

const dtaas = [
  { code: 'GBR', name: 'United Kingdom', effective: '1997-08-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'USA', name: 'United States', effective: '2004-09-01', dividends: 15, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'IND', name: 'India', effective: '1992-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'CHN', name: 'China', effective: '1997-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'JPN', name: 'Japan', effective: '1991-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'KOR', name: 'South Korea', effective: '1987-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'SGP', name: 'Singapore', effective: '2005-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'MYS', name: 'Malaysia', effective: '1984-01-01', dividends: 10, interest: 15, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'THA', name: 'Thailand', effective: '2005-01-01', dividends: 10, interest: 10, royalties: 10, technical: 10, pe_days: 183 },
  { code: 'CAN', name: 'Canada', effective: '1983-01-01', dividends: 15, interest: 15, royalties: 10, technical: 10, pe_days: 183 },
]

export default function DTAAExplorer() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedDTAA, setSelectedDTAA] = useState(null)

  const filtered = dtaas.filter(d => 
    d.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.code.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">DTAA Explorer</h1>
          <p className="text-gray-400 mt-1">Double Taxation Avoidance Agreements · 35 Active Treaties</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* List */}
        <div className="lg:col-span-1 space-y-4">
          <div className="glass-card p-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                placeholder="Search country..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input-field pl-12"
              />
            </div>
          </div>

          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {filtered.map((dtaa) => (
              <button
                key={dtaa.code}
                onClick={() => setSelectedDTAA(dtaa)}
                className={`
                  w-full glass-card p-4 text-left hover:bg-dark-800/50 transition-all
                  ${selectedDTAA?.code === dtaa.code ? 'border-primary-500/30 ring-1 ring-primary-500/20' : ''}
                `}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-lg font-bold text-primary-400">{dtaa.code}</span>
                    <div>
                      <p className="text-white font-medium text-sm">{dtaa.name}</p>
                      <p className="text-xs text-gray-500">Effective {dtaa.effective}</p>
                    </div>
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-gray-600" />
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Detail */}
        <div className="lg:col-span-2">
          {selectedDTAA ? (
            <div className="glass-card p-6 space-y-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 
                              flex items-center justify-center">
                  <Globe className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">{selectedDTAA.name}</h2>
                  <p className="text-gray-400">DTAA with Bangladesh · Effective {selectedDTAA.effective}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-dark-800/50 rounded-xl p-4 text-center">
                  <Percent className="w-5 h-5 text-primary-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-white">{selectedDTAA.dividends}%</p>
                  <p className="text-xs text-gray-500 mt-1">Dividends</p>
                </div>
                <div className="bg-dark-800/50 rounded-xl p-4 text-center">
                  <Percent className="w-5 h-5 text-secondary-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-white">{selectedDTAA.interest}%</p>
                  <p className="text-xs text-gray-500 mt-1">Interest</p>
                </div>
                <div className="bg-dark-800/50 rounded-xl p-4 text-center">
                  <Percent className="w-5 h-5 text-accent-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-white">{selectedDTAA.royalties}%</p>
                  <p className="text-xs text-gray-500 mt-1">Royalties</p>
                </div>
                <div className="bg-dark-800/50 rounded-xl p-4 text-center">
                  <Percent className="w-5 h-5 text-green-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-white">{selectedDTAA.technical}%</p>
                  <p className="text-xs text-gray-500 mt-1">Technical</p>
                </div>
              </div>

              <div className="bg-dark-800/50 rounded-xl p-4">
                <h3 className="text-white font-semibold mb-3">PE Threshold</h3>
                <p className="text-gray-400">Permanent Establishment threshold: <span className="text-white font-medium">{selectedDTAA.pe_days} days</span></p>
              </div>
            </div>
          ) : (
            <div className="glass-card p-12 text-center">
              <Globe className="w-12 h-12 text-gray-600 mx-auto mb-4" />
              <p className="text-white font-medium">Select a country to view DTAA details</p>
              <p className="text-sm text-gray-500 mt-2">Compare withholding rates across jurisdictions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
