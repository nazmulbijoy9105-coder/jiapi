import React from 'react'
import { Landmark, BookOpen, FileText, CheckCircle, AlertTriangle } from 'lucide-react'

function Compliance() {
  const chapters = [
    { num: 1, title: 'Registration and TIN', desc: 'Procedures for obtaining Tax Identification Number', status: 'active' },
    { num: 2, title: 'Return Filing', desc: 'Self-assessment return procedures and deadlines', status: 'active' },
    { num: 3, title: 'Assessment', desc: 'Regular assessment and best judgment assessment', status: 'active' },
    { num: 4, title: 'Audit', desc: 'Tax audit procedures and selection criteria', status: 'active' },
    { num: 5, title: 'Appeals', desc: 'Appeal procedures to AJC, Tribunal, HCD, AD', status: 'active' },
    { num: 6, title: 'Transfer Pricing', desc: 'TP audit and documentation requirements', status: 'active' },
    { num: 7, title: 'Withholding Tax', desc: 'TDS/TCS compliance and deposit procedures', status: 'active' },
    { num: 8, title: 'Penalties', desc: 'Penalty imposition and waiver procedures', status: 'active' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Tax Compliance Manual</h1>
        <p className="mt-2 text-dark-500">NBR Tax Compliance Manual - Version 2024-1</p>
      </div>

      <div className="card bg-green-50 border-green-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-green-600 rounded-lg text-white">
            <Landmark size={24} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-dark-900">NBR Tax Compliance Manual</h2>
            <p className="mt-2 text-sm text-dark-600">
              Official compliance manual published by National Board of Revenue. 
              Effective from July 1, 2024. Current version: 2024-1.
            </p>
            <div className="mt-4 flex gap-3">
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-green-700">
                Version 2024-1
              </span>
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-green-700">
                Effective: 2024-07-01
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {chapters.map(chapter => (
          <div key={chapter.num} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-primary-50 rounded-lg flex items-center justify-center text-primary-700 font-bold">
                {chapter.num}
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-dark-900">{chapter.title}</h3>
                <p className="text-sm text-dark-500 mt-1">{chapter.desc}</p>
                <div className="mt-3 flex items-center gap-2">
                  <CheckCircle size={14} className="text-green-600" />
                  <span className="text-xs text-green-700">{chapter.status}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Compliance
