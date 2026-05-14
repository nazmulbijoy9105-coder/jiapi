import React from 'react'
import { Database, AlertTriangle, Calendar, BookOpen } from 'lucide-react'

function Pre2023() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-dark-900">Pre-2023 Legislation</h1>
          <p className="mt-2 text-dark-500">ITO 1984 and all amendments up to FY 2022-23</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg text-sm font-medium">
          <AlertTriangle size={16} />
          Repealed
        </div>
      </div>

      <div className="card bg-red-50 border-red-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-red-600 rounded-lg text-white">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-dark-900">Historical Archive</h2>
            <p className="mt-2 text-sm text-dark-600">
              ITO 1984 was entirely superseded by ITA 2023 from July 1, 2023. 
              This section contains the complete historical text for pending assessments, 
              ongoing litigation, and reference purposes.
            </p>
            <div className="mt-4 flex gap-3">
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-red-700">
                Repealed: June 30, 2023
              </span>
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-dark-600">
                39 Years Active
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen size={20} className="text-primary-600" />
          <h3 className="text-lg font-semibold text-dark-900">Income Tax Ordinance, 1984</h3>
        </div>
        <p className="text-dark-500 mb-4">
          Ordinance No. XXXVI of 1984. Enacted July 1, 1984. Last amended by Finance Act 2023 (pre-repeal).
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-dark-100 rounded-lg">
            <p className="text-2xl font-bold text-dark-900">1984</p>
            <p className="text-sm text-dark-500">Year Enacted</p>
          </div>
          <div className="p-4 bg-dark-100 rounded-lg">
            <p className="text-2xl font-bold text-dark-900">39</p>
            <p className="text-sm text-dark-500">Years Active</p>
          </div>
          <div className="p-4 bg-dark-100 rounded-lg">
            <p className="text-2xl font-bold text-dark-900">40</p>
            <p className="text-sm text-dark-500">Finance Acts Amended</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Calendar size={20} className="text-primary-600" />
          <h3 className="text-lg font-semibold text-dark-900">Finance Acts (1984-2023)</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-200">
                <th className="text-left py-3 px-4 font-medium text-dark-700">Year</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Key Changes</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                { year: 2023, changes: 'Last amendment before repeal', status: 'Superseded' },
                { year: 2022, changes: 'Digital service tax introduced', status: 'Historical' },
                { year: 2020, changes: 'COVID relief measures', status: 'Historical' },
                { year: 2015, changes: 'Major restructuring', status: 'Historical' },
                { year: 2012, changes: 'Tax holiday provisions', status: 'Historical' },
              ].map(row => (
                <tr key={row.year} className="border-b border-dark-100 hover:bg-dark-50">
                  <td className="py-3 px-4 font-medium">{row.year}</td>
                  <td className="py-3 px-4 text-dark-600">{row.changes}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-dark-100 rounded text-xs">{row.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Pre2023
