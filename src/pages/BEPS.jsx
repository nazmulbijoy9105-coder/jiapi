import React from 'react'
import { Shield, Globe, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

function BEPS() {
  const actions = [
    { action: 'Action 1', title: 'Digital Economy', bd_relevance: 'Growing relevance with digital service taxation', status: 'pending' },
    { action: 'Action 2', title: 'Hybrid Mismatches', bd_relevance: 'Relevant for MNE structures', status: 'pending' },
    { action: 'Action 5', title: 'Harmful Tax Practices', bd_relevance: 'Relevant for tax holiday regimes', status: 'partially_adopted' },
    { action: 'Action 6', title: 'Treaty Abuse', bd_relevance: 'PPT included in recent treaties', status: 'adopted' },
    { action: 'Action 7', title: 'PE Status', bd_relevance: 'Commissionaire arrangements', status: 'pending' },
    { action: 'Action 8-10', title: 'Transfer Pricing', bd_relevance: 'Hard-to-value intangibles', status: 'partially_adopted' },
    { action: 'Action 13', title: 'TP Documentation & CbCR', bd_relevance: 'ITA 2023 Section 235', status: 'adopted' },
    { action: 'Action 14', title: 'Dispute Resolution', bd_relevance: 'MAP provisions in treaties', status: 'adopted' },
    { action: 'Action 15', title: 'Multilateral Instrument', bd_relevance: 'Not yet signed by Bangladesh', status: 'pending' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">OECD BEPS Framework</h1>
        <p className="mt-2 text-dark-500">Base Erosion and Profit Shifting - Bangladesh relevance and implementation status</p>
      </div>

      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-blue-600 rounded-lg text-white">
            <Shield size={24} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-dark-900">BEPS in Bangladesh</h2>
            <p className="mt-2 text-sm text-dark-600">
              BEPS framework is non-binding in Bangladesh but increasingly cited in tax practice. 
              ITA 2023 incorporates several BEPS-aligned provisions, particularly in transfer pricing 
              (Sections 233-239) and international transactions.
            </p>
            <div className="mt-4 flex gap-3">
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-blue-700">
                Non-Binding
              </span>
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-blue-700">
                Increasingly Cited
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">BEPS Action Items & Bangladesh Status</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-200">
                <th className="text-left py-3 px-4 font-medium text-dark-700">Action</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Title</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">BD Relevance</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Status</th>
              </tr>
            </thead>
            <tbody>
              {actions.map((a, i) => (
                <tr key={i} className="border-b border-dark-100 hover:bg-dark-50">
                  <td className="py-3 px-4 font-medium">{a.action}</td>
                  <td className="py-3 px-4">{a.title}</td>
                  <td className="py-3 px-4 text-dark-600">{a.bd_relevance}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      a.status === 'adopted' ? 'bg-green-100 text-green-700' :
                      a.status === 'partially_adopted' ? 'bg-amber-100 text-amber-700' :
                      'bg-dark-100 text-dark-600'
                    }`}>
                      {a.status === 'adopted' && <CheckCircle size={12} className="inline mr-1" />}
                      {a.status === 'partially_adopted' && <AlertCircle size={12} className="inline mr-1" />}
                      {a.status === 'pending' && <XCircle size={12} className="inline mr-1" />}
                      {a.status.replace('_', ' ')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Related ITA 2023 Sections</h3>
        <div className="flex flex-wrap gap-2">
          {['233', '234', '235', '236', '237', '238', '239'].map(sec => (
            <span key={sec} className="px-3 py-2 bg-primary-50 text-primary-700 rounded-lg text-sm font-medium">
              Section {sec}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

export default BEPS
