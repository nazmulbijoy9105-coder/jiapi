import React from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpen, FileText, Gavel, Globe, GitCompare, 
  Clock, TrendingUp, Shield, Zap, ArrowRight,
  Activity, Layers, Scale
} from 'lucide-react'

const stats = [
  { label: 'Legislation Sections', value: '2,847', change: '+12', icon: BookOpen, color: 'primary' },
  { label: 'Case Judgments', value: '1,234', change: '+45', icon: Gavel, color: 'secondary' },
  { label: 'Active DTAAs', value: '35', change: '+2', icon: Globe, color: 'accent' },
  { label: 'Amendments Tracked', value: '892', change: '+23', icon: Activity, color: 'primary' },
]

const quickAccess = [
  { 
    title: 'Income Tax Act 2023', 
    subtitle: 'ITA 2023 · 187 Sections',
    path: '/post2023',
    icon: BookOpen,
    color: 'from-primary-600 to-primary-400',
    badge: 'Primary Act'
  },
  { 
    title: 'Income Tax Rules 2024', 
    subtitle: 'ITR 2024 · 95 Rules',
    path: '/post2023',
    icon: FileText,
    color: 'from-secondary-600 to-secondary-400',
    badge: 'Rules'
  },
  { 
    title: 'ITO 1984 (Archive)', 
    subtitle: 'Historical · 164 Sections',
    path: '/pre2023',
    icon: Layers,
    color: 'from-gray-600 to-gray-400',
    badge: 'Pre-2023'
  },
  { 
    title: 'Case Law Database', 
    subtitle: 'AD · HCD · TAT',
    path: '/caselaw',
    icon: Gavel,
    color: 'from-accent-600 to-accent-400',
    badge: 'Judgments'
  },
]

const recentActivity = [
  { type: 'amendment', text: 'Finance Act 2025 amended Section 30 of ITA 2023', time: '2 hours ago' },
  { type: 'sro', text: 'New SRO 234/2024 on IT sector tax exemption', time: '1 day ago' },
  { type: 'judgment', text: 'AD judgment on transfer pricing interpretation', time: '3 days ago' },
  { type: 'circular', text: 'NBR Circular on advance tax payment', time: '5 days ago' },
]

export default function Dashboard() {
  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-dark-800 to-dark-900 border border-white/5 p-8">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 
                          flex items-center justify-center shadow-lg shadow-primary-500/20">
              <Scale className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">JIAPI Dashboard</h1>
              <p className="text-gray-400">Bangladesh Tax Law Database · Post-2023 & Pre-2023</p>
            </div>
          </div>
          <p className="text-gray-400 max-w-2xl mt-4 leading-relaxed">
            Access the complete Income Tax Act 2023, historical ITO 1984, case law from Appellate Division 
            to TAT, 35+ DTAA treaties, and real-time amendment tracking with point-in-time queries.
          </p>
          <div className="flex gap-4 mt-6">
            <Link to="/post2023" className="btn-primary flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              Explore ITA 2023
            </Link>
            <Link to="/search" className="btn-secondary flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Quick Search
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon
          return (
            <div key={i} className="stat-card group hover:bg-dark-800/50 transition-all">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-10 h-10 rounded-xl bg-${stat.color}-500/10 flex items-center justify-center
                              group-hover:bg-${stat.color}-500/20 transition-colors`}>
                  <Icon className={`w-5 h-5 text-${stat.color}-400`} />
                </div>
                <span className="text-xs font-medium text-green-400 bg-green-500/10 px-2 py-1 rounded-full">
                  {stat.change}
                </span>
              </div>
              <p className="text-2xl font-bold text-white">{stat.value}</p>
              <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
            </div>
          )
        })}
      </div>

      {/* Quick Access */}
      <div>
        <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-primary-400" />
          Quick Access
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickAccess.map((item, i) => {
            const Icon = item.icon
            return (
              <Link 
                key={i} 
                to={item.path}
                className="group relative overflow-hidden rounded-2xl bg-dark-800/50 border border-white/5 
                         p-6 hover:border-white/10 transition-all duration-300"
              >
                <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${item.color} 
                              opacity-10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 
                              group-hover:opacity-20 transition-opacity`} />
                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <span className="badge-primary text-xs">{item.badge}</span>
                    <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-white 
                                         group-hover:translate-x-1 transition-all" />
                  </div>
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${item.color} 
                                flex items-center justify-center mb-4 shadow-lg`}>
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="text-white font-semibold">{item.title}</h3>
                  <p className="text-sm text-gray-500 mt-1">{item.subtitle}</p>
                </div>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Tools & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tools */}
        <div className="lg:col-span-2">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-secondary-400" />
            Advanced Tools
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link to="/diff" className="section-card group">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center
                              group-hover:bg-primary-500/20 transition-colors">
                  <GitCompare className="w-6 h-6 text-primary-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Diff Engine</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    Compare legislation between two dates. See exactly what changed and by which amendment.
                  </p>
                </div>
              </div>
            </Link>

            <Link to="/point-in-time" className="section-card group">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-secondary-500/10 flex items-center justify-center
                              group-hover:bg-secondary-500/20 transition-colors">
                  <Clock className="w-6 h-6 text-secondary-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Point-in-Time</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    View law as it existed on any historical date. Critical for pending assessments and litigation.
                  </p>
                </div>
              </div>
            </Link>

            <Link to="/amendments" className="section-card group">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-accent-500/10 flex items-center justify-center
                              group-hover:bg-accent-500/20 transition-colors">
                  <TrendingUp className="w-6 h-6 text-accent-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Amendment Feed</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    Real-time feed of all amendments. Subscribe via webhook for instant notifications.
                  </p>
                </div>
              </div>
            </Link>

            <Link to="/dtaa" className="section-card group">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center
                              group-hover:bg-green-500/20 transition-colors">
                  <Globe className="w-6 h-6 text-green-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">DTAA Explorer</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    Browse 35+ double taxation treaties. Compare withholding rates across jurisdictions.
                  </p>
                </div>
              </div>
            </Link>
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-accent-400" />
            Recent Activity
          </h2>
          <div className="glass-card p-4 space-y-4">
            {recentActivity.map((item, i) => (
              <div key={i} className="flex items-start gap-3 pb-4 border-b border-white/5 last:border-0 last:pb-0">
                <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0
                  ${item.type === 'amendment' ? 'bg-primary-400' : 
                    item.type === 'sro' ? 'bg-secondary-400' : 
                    item.type === 'judgment' ? 'bg-accent-400' : 'bg-green-400'}`} 
                />
                <div>
                  <p className="text-sm text-gray-300 leading-relaxed">{item.text}</p>
                  <p className="text-xs text-gray-600 mt-1">{item.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
