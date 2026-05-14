import React, { useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { 
  Scale, BookOpen, Search, Gavel, Globe, 
  FileText, AlertTriangle, TrendingUp, 
  Shield, ChevronDown, Menu, X, Zap,
  Code, LogIn, Database, Landmark
} from 'lucide-react'

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Zap size={20} /> },
    { path: '/post2023', label: 'Post-2023 (ITA 2023)', icon: <BookOpen size={20} /> },
    { path: '/pre2023', label: 'Pre-2023 (ITO 1984)', icon: <Database size={20} /> },
    { path: '/caselaw', label: 'Case Law', icon: <Gavel size={20} /> },
    { path: '/dtaa', label: 'DTAAs', icon: <Globe size={20} /> },
    { path: '/search', label: 'Search', icon: <Search size={20} /> },
    { path: '/amendments', label: 'Amendments', icon: <AlertTriangle size={20} /> },
    { path: '/tax-rates', label: 'Tax Rates', icon: <TrendingUp size={20} /> },
    { path: '/tp-regulations', label: 'Transfer Pricing', icon: <Scale size={20} /> },
    { path: '/beps', label: 'BEPS', icon: <Shield size={20} /> },
    { path: '/compliance', label: 'Compliance', icon: <Landmark size={20} /> },
    { path: '/api-reference', label: 'API Reference', icon: <Code size={20} /> },
  ]

  return (
    <div className="min-h-screen bg-dark-50 flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50 w-72 bg-dark-900 text-white 
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        flex flex-col overflow-y-auto
      `}>
        <div className="p-6 border-b border-dark-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <Scale className="text-white" size={24} />
            </div>
            <div>
              <h1 className="font-bold text-lg leading-tight">JIAPI</h1>
              <p className="text-xs text-dark-400">Justice & Income API</p>
            </div>
          </div>
          <p className="mt-2 text-xs text-dark-500">Bangladesh Tax Law Database</p>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setSidebarOpen(false)}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all
                ${location.pathname === item.path 
                  ? 'bg-primary-600 text-white' 
                  : 'text-dark-300 hover:bg-dark-800 hover:text-white'}
              `}
            >
              {item.icon}
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-dark-700">
          <Link 
            to="/login"
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium 
                       text-dark-300 hover:bg-dark-800 hover:text-white transition-all"
          >
            <LogIn size={20} />
            Sign In
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-dark-200 sticky top-0 z-30">
          <div className="flex items-center justify-between px-4 py-3 lg:px-8">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg hover:bg-dark-100"
              >
                <Menu size={24} />
              </button>
              <div className="hidden md:flex items-center gap-2 text-sm text-dark-500">
                <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                  v1.0.0
                </span>
                <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                  API Ready
                </span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 text-sm text-dark-500">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                System Operational
              </div>
              <Link 
                to="/api-reference"
                className="hidden sm:flex items-center gap-2 px-4 py-2 bg-primary-600 text-white 
                           rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors"
              >
                <Code size={16} />
                API Docs
              </Link>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-4 lg:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default Layout
