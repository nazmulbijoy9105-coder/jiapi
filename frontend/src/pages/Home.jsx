import React from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpen, Database, Gavel, Globe, Search, 
  AlertTriangle, TrendingUp, Scale, Shield,
  Landmark, Code, ArrowRight, Activity, Users,
  FileText, CheckCircle, Clock
} from 'lucide-react'

function StatCard({ icon, label, value, change, changeType }) {
  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="p-3 bg-primary-50 rounded-lg text-primary-600">
          {icon}
        </div>
        {change && (
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${
            changeType === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {change}
          </span>
        )}
      </div>
      <div className="mt-4">
        <p className="text-2xl font-bold text-dark-900">{value}</p>
        <p className="text-sm text-dark-500 mt-1">{label}</p>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description, path, color }) {
  const colors = {
    blue: 'bg-primary-50 text-primary-600 border-primary-200',
    purple: 'bg-secondary-50 text-secondary-600 border-secondary-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200',
    red: 'bg-red-50 text-red-600 border-red-200',
    teal: 'bg-teal-50 text-teal-600 border-teal-200',
  }

  return (
    <Link to={path} className="card hover:shadow-lg transition-all group">
      <div className={`p-3 rounded-lg w-fit ${colors[color] || colors.blue}`}>
        {icon}
      </div>
      <h3 className="mt-4 text-lg font-semibold text-dark-900 group-hover:text-primary-600 transition-colors">
        {title}
      </h3>
      <p className="mt-2 text-sm text-dark-500 leading-relaxed">
        {description}
      </p>
      <div className="mt-4 flex items-center gap-2 text-sm font-medium text-primary-600 
                      opacity-0 group-hover:opacity-100 transition-opacity">
        Explore <ArrowRight size={16} />
      </div>
    </Link>
  )
}

function Home() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-dark-900 text-white p-8 lg:p-12">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary-600/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

        <div className="relative z-10 max-w-3xl">
          <div className="flex items-center gap-2 mb-4">
            <span className="px-3 py-1 bg-primary-600/30 border border-primary-500/30 rounded-full text-xs font-medium">
              🇧🇩 Bangladesh Tax Law Database
            </span>
            <span className="px-3 py-1 bg-green-600/30 border border-green-500/30 rounded-full text-xs font-medium">
              Commercial Grade
            </span>
          </div>
          <h1 className="text-4xl lg:text-5xl font-bold leading-tight">
            Justice & Income API
          </h1>
          <p className="mt-4 text-lg text-dark-300 leading-relaxed max-w-2xl">
            Comprehensive tax law database for Bangladesh. ITA 2023, ITO 1984, case law, 
            DTAAs, SROs, amendments, and real-time compliance alerts — all in one API.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link to="/post2023" className="btn-primary flex items-center gap-2">
              <BookOpen size={18} />
              Browse ITA 2023
            </Link>
            <Link to="/api-reference" className="px-4 py-2 bg-white/10 text-white rounded-lg 
                                                  font-medium hover:bg-white/20 transition-colors 
                                                  flex items-center gap-2">
              <Code size={18} />
              API Documentation
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard 
          icon={<BookOpen size={24} />}
          label="Legislation Acts"
          value="45+"
          change="+3 this year"
          changeType="up"
        />
        <StatCard 
          icon={<Gavel size={24} />}
          label="Case Law Judgments"
          value="4,170+"
          change="+120 this month"
          changeType="up"
        />
        <StatCard 
          icon={<Globe size={24} />}
          label="DTAA Treaties"
          value="35"
          change="Active"
          changeType="up"
        />
        <StatCard 
          icon={<AlertTriangle size={24} />}
          label="Amendments Tracked"
          value="2,500+"
          change="+15 pending"
          changeType="up"
        />
      </div>

      {/* Features Grid */}
      <div>
        <h2 className="text-2xl font-bold text-dark-900 mb-6">Explore JIAPI</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <FeatureCard
            icon={<BookOpen size={24} />}
            title="Post-2023 Legislation"
            description="ITA 2023, ITR 2024, Finance Acts 2023-2025. Full text with amendment tracking and point-in-time queries."
            path="/post2023"
            color="blue"
          />
          <FeatureCard
            icon={<Database size={24} />}
            title="Pre-2023 Legislation"
            description="ITO 1984 with all amendments up to FY 2022-23. Historical Finance Acts, SROs, and circulars."
            path="/pre2023"
            color="purple"
          />
          <FeatureCard
            icon={<Gavel size={24} />}
            title="Case Law Database"
            description="AD, HCD, and TAT judgments. Full-text search, citation checker, and provision linking."
            path="/caselaw"
            color="green"
          />
          <FeatureCard
            icon={<Globe size={24} />}
            title="DTAA Treaties"
            description="35+ Double Taxation Avoidance Agreements. Withholding rates, articles, and country-specific guides."
            path="/dtaa"
            color="teal"
          />
          <FeatureCard
            icon={<Search size={24} />}
            title="Advanced Search"
            description="Full-text search across all content in English and Bengali. Boolean operators and field filters."
            path="/search"
            color="orange"
          />
          <FeatureCard
            icon={<AlertTriangle size={24} />}
            title="Amendment Tracker"
            description="Real-time amendment feed. Point-in-time queries, diff views, and webhook notifications."
            path="/amendments"
            color="red"
          />
          <FeatureCard
            icon={<TrendingUp size={24} />}
            title="Tax Rates"
            description="Individual and corporate tax rates. Withholding tax rates, surcharge brackets, and special categories."
            path="/tax-rates"
            color="blue"
          />
          <FeatureCard
            icon={<Scale size={24} />}
            title="Transfer Pricing"
            description="TP regulations under ITA 2023. Arm's length methods, documentation, and penalty provisions."
            path="/tp-regulations"
            color="purple"
          />
          <FeatureCard
            icon={<Shield size={24} />}
            title="BEPS Framework"
            description="OECD BEPS action items. Bangladesh relevance, implementation status, and ITA 2023 alignment."
            path="/beps"
            color="green"
          />
          <FeatureCard
            icon={<Landmark size={24} />}
            title="Compliance Manual"
            description="NBR Tax Compliance Manual. Registration, filing, assessment, audit, and appeal procedures."
            path="/compliance"
            color="teal"
          />
          <FeatureCard
            icon={<Code size={24} />}
            title="API Reference"
            description="Complete API documentation. Authentication, endpoints, rate limits, and code examples."
            path="/api-reference"
            color="orange"
          />
        </div>
      </div>

      {/* Quick Access */}
      <div className="card bg-dark-900 text-white">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div>
            <h3 className="text-xl font-bold">Ready to integrate?</h3>
            <p className="mt-2 text-dark-300">
              Get API keys, explore endpoints, and start building with JIAPI today.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <div className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg text-sm">
              <CheckCircle size={16} className="text-green-400" />
              Free tier: 100 req/day
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg text-sm">
              <CheckCircle size={16} className="text-green-400" />
              JWT + API Key auth
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg text-sm">
              <CheckCircle size={16} className="text-green-400" />
              Webhook alerts
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
