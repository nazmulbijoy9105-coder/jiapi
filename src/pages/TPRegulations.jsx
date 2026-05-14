import React from 'react'
import { Scale, BookOpen, FileText, AlertTriangle, CheckCircle } from 'lucide-react'

function TPRegulations() {
  const methods = [
    { code: 'CUP', name: 'Comparable Uncontrolled Price', desc: 'Compares price in controlled transaction with comparable uncontrolled transaction' },
    { code: 'RPM', name: 'Resale Price Method', desc: 'Appropriate gross margin is determined for the reseller' },
    { code: 'CP', name: 'Cost Plus Method', desc: 'Appropriate markup on costs is determined' },
    { code: 'PSM', name: 'Profit Split Method', desc: 'Profits are split between associated enterprises' },
    { code: 'TNMM', name: 'Transactional Net Margin Method', desc: 'Net profit margin is compared with comparable uncontrolled transactions' },
    { code: 'Other', name: 'Any Other Method', desc: 'Residual category when none of the above is suitable' },
  ]

  const penalties = [
    { section: '276', violation: 'Failure to comply with notice', penalty: 'Up to 1% of transaction value' },
    { section: '277', violation: 'Failure to maintain documents', penalty: 'Up to 1% of transaction value' },
    { section: '278', violation: 'Failure to furnish report', penalty: 'Up to 2% of transaction value' },
    { section: '279', violation: 'Failure to furnish accountant report', penalty: 'Up to Tk. 3 lakh' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Transfer Pricing Regulations</h1>
        <p className="mt-2 text-dark-500">ITA 2023 Chapter on International Transactions (Sections 233-239)</p>
      </div>

      <div className="card bg-primary-50 border-primary-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-primary-600 rounded-lg text-white">
            <Scale size={24} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-dark-900">Transfer Pricing under ITA 2023</h2>
            <p className="mt-2 text-sm text-dark-600">
              Sections 233-239 govern transfer pricing for international transactions. 
              Broadly aligned with OECD Guidelines though Bangladesh is not an OECD member.
            </p>
            <div className="mt-4 flex gap-3">
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-primary-700">
                Sections 233-239
              </span>
              <span className="px-3 py-1 bg-white rounded-full text-xs font-medium text-primary-700">
                OECD Aligned
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Arm's Length Methods</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {methods.map((method, i) => (
            <div key={i} className="p-4 bg-dark-50 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-bold">
                  {method.code}
                </span>
                <span className="font-medium text-dark-900">{method.name}</span>
              </div>
              <p className="text-sm text-dark-600">{method.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Documentation Requirements</h3>
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <CheckCircle size={20} className="text-green-600 mt-0.5" />
            <div>
              <p className="font-medium text-dark-900">Threshold</p>
              <p className="text-sm text-dark-600">International transactions exceeding Tk. 3 crore require documentation</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle size={20} className="text-green-600 mt-0.5" />
            <div>
              <p className="font-medium text-dark-900">Master File</p>
              <p className="text-sm text-dark-600">Required for MNE groups - group-level information</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle size={20} className="text-green-600 mt-0.5" />
            <div>
              <p className="font-medium text-dark-900">Local File</p>
              <p className="text-sm text-dark-600">Required for Bangladesh entities - entity-level documentation</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle size={20} className="text-green-600 mt-0.5" />
            <div>
              <p className="font-medium text-dark-900">Deadline</p>
              <p className="text-sm text-dark-600">Within 30 days of requisition by DCT (Deputy Commissioner of Taxes)</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-dark-900 mb-4">Penalty Provisions</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-200">
                <th className="text-left py-3 px-4 font-medium text-dark-700">Section</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Violation</th>
                <th className="text-left py-3 px-4 font-medium text-dark-700">Penalty</th>
              </tr>
            </thead>
            <tbody>
              {penalties.map((p, i) => (
                <tr key={i} className="border-b border-dark-100 hover:bg-dark-50">
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                      Sec {p.section}
                    </span>
                  </td>
                  <td className="py-3 px-4">{p.violation}</td>
                  <td className="py-3 px-4 font-medium text-red-700">{p.penalty}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default TPRegulations
