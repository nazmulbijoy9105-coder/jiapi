import React from 'react'
import { AlertTriangle, Calendar, ArrowRight, CheckCircle, Clock } from 'lucide-react'

function Amendments() {
  const feed = [
    { id: 'feed-001', title: 'Finance Act 2025 - Corporate Tax Rate Changes', desc: 'General corporate tax rate reduced to 27.5% for non-listed entities', priority: 'high', date: '2025-07-01', sections: ['Rate Schedule'], status: 'applied' },
    { id: 'feed-002', title: 'Finance Act 2025 - Minimum Tax Carry Forward', desc: 'Minimum tax can now be carried forward for 3 years', priority: 'high', date: '2025-07-01', sections: ['163', '70'], status: 'applied' },
    { id: 'feed-003', title: 'SRO 404-Law/2025 - Authentic English Text', desc: 'Official authentic English text of ITA 2023 published by NBR', priority: 'normal', date: '2025-10-08', sections: ['All'], status: 'applied' },
    { id: 'feed-004', title: 'Finance Act 2025 - Banking Channel Penalty', desc: '2.5% higher rate for non-banking channel transactions', priority: 'high', date: '2025-07-01', sections: ['Various'], status: 'applied' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Amendment Tracker</h1>
        <p className="mt-2 text-dark-500">Real-time feed of law changes with point-in-time and diff views</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-green-50 border-green-200">
          <div className="flex items-center gap-3">
            <CheckCircle size={24} className="text-green-600" />
            <div>
              <p className="text-2xl font-bold text-dark-900">2,500+</p>
              <p className="text-sm text-dark-500">Amendments Tracked</p>
            </div>
          </div>
        </div>
        <div className="card bg-amber-50 border-amber-200">
          <div className="flex items-center gap-3">
            <Clock size={24} className="text-amber-600" />
            <div>
              <p className="text-2xl font-bold text-dark-900">15</p>
              <p className="text-sm text-dark-500">Pending Amendments</p>
            </div>
          </div>
        </div>
        <div className="card bg-primary-50 border-primary-200">
          <div className="flex items-center gap-3">
            <Calendar size={24} className="text-primary-600" />
            <div>
              <p className="text-2xl font-bold text-dark-900">4</p>
              <p className="text-sm text-dark-500">This Month</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Latest Amendments</h3>
        <div className="space-y-4">
          {feed.map(item => (
            <div key={item.id} className="p-4 bg-dark-50 rounded-lg hover:bg-dark-100 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      item.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                    }`}>
                      {item.priority === 'high' ? '🔴 High' : '🔵 Normal'}
                    </span>
                    <span className="text-xs text-dark-500">{item.date}</span>
                  </div>
                  <h4 className="font-medium text-dark-900">{item.title}</h4>
                  <p className="text-sm text-dark-600 mt-1">{item.desc}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {item.sections.map(sec => (
                      <span key={sec} className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">
                        Sec {sec}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="ml-4">
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                    Applied
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Amendments
