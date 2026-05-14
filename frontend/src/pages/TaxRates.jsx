import React, { useState } from 'react'
import { TrendingUp, Users, Building2, AlertCircle, Info } from 'lucide-react'

function TaxRates() {
  const [activeTab, setActiveTab] = useState('individual')

  const individualSlabs = [
    { slab: 'First Tk. 3,50,000', rate: 0, category: 'General threshold' },
    { slab: 'Next Tk. 1,00,000', rate: 5, category: 'General' },
    { slab: 'Next Tk. 3,00,000', rate: 10, category: 'General' },
    { slab: 'Next Tk. 4,00,000', rate: 15, category: 'General' },
    { slab: 'Next Tk. 5,00,000', rate: 20, category: 'General' },
    { slab: 'On the balance', rate: 25, category: 'General' },
  ]

  const specialCategories = [
    { category: 'Women & Senior Citizens (65+)', exemption: 'Tk. 4,00,000', note: 'Additional Tk. 50,000' },
    { category: 'Physically Challenged', exemption: 'Tk. 4,75,000', note: 'Full exemption limit' },
    { category: 'War Wounded Freedom Fighters', exemption: 'Tk. 5,00,000', note: 'Highest exemption' },
    { category: 'Parent of Physically Challenged', exemption: 'Tk. 50,000', note: 'Additional per child' },
  ]

  const corporateRates = [
    { category: 'Publicly traded companies', rate: 20, note: 'Listed on stock exchange' },
    { category: 'Non-publicly traded companies', rate: 27.5, note: 'General rate (reduced from 30% in FA 2025)' },
    { category: 'Mobile phone companies (non-listed)', rate: 45, note: 'Highest corporate rate' },
    { category: 'Mobile phone companies (listed)', rate: 45, note: 'Same as non-listed' },
    { category: 'Banks/Insurance/MFS (listed)', rate: 37.5, note: 'Financial institutions' },
    { category: 'Banks/Insurance/MFS (non-listed)', rate: 40, note: 'Non-listed financials' },
    { category: 'Merchant banks', rate: 37.5, note: 'Same as listed banks' },
    { category: 'Tobacco/Cigarette manufacturing', rate: 45, note: 'Sin tax rate' },
    { category: 'One Person Companies', rate: 22.5, note: 'Special OPC rate' },
    { category: 'Co-Operative Society', rate: 15, note: 'Lowest corporate rate' },
    { category: 'Private University/Medical/IT', rate: 15, note: 'Education/health/tech' },
  ]

  const withholdingRates = [
    { section: '30', description: 'Salaries', rate: 'Average rate', conditions: 'Based on estimated income' },
    { section: '89', description: 'Contractors', rate: '3% / 5% / 7%', conditions: 'Slab based on amount; 50% higher without return' },
    { section: '90', description: 'Suppliers', rate: '3% / 5% / 7%', conditions: 'Slab based on amount' },
    { section: '124', description: 'Service charges/fees', rate: '7.5% / 10%', conditions: 'Based on nature of service' },
    { section: '128', description: 'Lease of property', rate: '10%', conditions: 'All lease payments' },
    { section: '134', description: 'Transfer of shares (non-listed)', rate: '15%', conditions: 'On difference between fair and face value' },
    { section: '135', description: 'Transfer of securities', rate: '10%', conditions: 'Sponsor/director/placement shares' },
    { section: '137', description: 'Commercial motor vehicles', rate: '0.05%', conditions: 'Depends on vehicle type' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-dark-900">Tax Rates</h1>
        <p className="mt-2 text-dark-500">Individual, corporate, and withholding tax rates for FY 2025-26</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-dark-200">
        {[
          { id: 'individual', label: 'Individual', icon: <Users size={18} /> },
          { id: 'corporate', label: 'Corporate', icon: <Building2 size={18} /> },
          { id: 'withholding', label: 'Withholding (TDS)', icon: <TrendingUp size={18} /> },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id 
                ? 'border-primary-600 text-primary-600' 
                : 'border-transparent text-dark-500 hover:text-dark-700'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Individual Rates */}
      {activeTab === 'individual' && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-dark-900 mb-4">Tax Slabs - Resident Individual</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-dark-200">
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Income Slab</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Rate</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Category</th>
                  </tr>
                </thead>
                <tbody>
                  {individualSlabs.map((slab, i) => (
                    <tr key={i} className="border-b border-dark-100 hover:bg-dark-50">
                      <td className="py-3 px-4 font-medium">{slab.slab}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          slab.rate === 0 ? 'bg-green-100 text-green-700' : 'bg-primary-100 text-primary-700'
                        }`}>
                          {slab.rate === 0 ? 'Exempt' : `${slab.rate}%`}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-dark-600">{slab.category}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-dark-900 mb-4">Special Categories</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {specialCategories.map((cat, i) => (
                <div key={i} className="p-4 bg-dark-50 rounded-lg">
                  <p className="font-medium text-dark-900">{cat.category}</p>
                  <p className="text-sm text-dark-600 mt-1">Exemption: {cat.exemption}</p>
                  <p className="text-xs text-dark-500 mt-1">{cat.note}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="card bg-amber-50 border-amber-200">
            <div className="flex items-start gap-3">
              <AlertCircle size={20} className="text-amber-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-amber-800">Minimum Tax</h4>
                <p className="text-sm text-amber-700 mt-1">
                  Dhaka & Chattogram City: Tk. 5,000 | Other City Corp: Tk. 4,000 | Other Areas: Tk. 3,000
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Corporate Rates */}
      {activeTab === 'corporate' && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-dark-900 mb-4">Corporate Tax Rates</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-dark-200">
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Category</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Rate</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {corporateRates.map((corp, i) => (
                    <tr key={i} className="border-b border-dark-100 hover:bg-dark-50">
                      <td className="py-3 px-4 font-medium">{corp.category}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          corp.rate <= 20 ? 'bg-green-100 text-green-700' :
                          corp.rate <= 30 ? 'bg-primary-100 text-primary-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          {corp.rate}%
                        </span>
                      </td>
                      <td className="py-3 px-4 text-dark-600">{corp.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="card bg-blue-50 border-blue-200">
            <div className="flex items-start gap-3">
              <Info size={20} className="text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-800">Banking Channel Requirement</h4>
                <p className="text-sm text-blue-700 mt-1">
                  Single transaction: Tk. 5,00,000 | Annual: Tk. 36,00,000<br/>
                  Penalty: 2.5% higher rate if not through banking channel
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Withholding Rates */}
      {activeTab === 'withholding' && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-dark-900 mb-4">Withholding Tax Rates (TDS)</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-dark-200">
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Section</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Description</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Rate</th>
                    <th className="text-left py-3 px-4 font-medium text-dark-700">Conditions</th>
                  </tr>
                </thead>
                <tbody>
                  {withholdingRates.map((w, i) => (
                    <tr key={i} className="border-b border-dark-100 hover:bg-dark-50">
                      <td className="py-3 px-4">
                        <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                          Sec {w.section}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-medium">{w.description}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-1 bg-dark-100 rounded text-xs font-medium">
                          {w.rate}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-dark-600 text-xs">{w.conditions}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TaxRates
