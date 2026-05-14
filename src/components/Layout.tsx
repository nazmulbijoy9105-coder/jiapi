import { Link, useLocation } from "react-router-dom";
import { Scale, Search, BookOpen, Gavel, Menu, X } from "lucide-react";
import { useState } from "react";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Home", icon: Scale },
    { path: "/legislations/post2023", label: "Post-2023 Laws", icon: BookOpen },
    { path: "/legislations/pre2023", label: "Pre-2023 Laws", icon: BookOpen },
    { path: "/case-laws", label: "Case Law", icon: Gavel },
    { path: "/search", label: "Search", icon: Search },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-bangladesh-green text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-3">
              <Scale className="w-8 h-8" />
              <div>
                <h1 className="text-xl font-bold">JIAPI</h1>
                <p className="text-xs text-green-200">Justice & Income API</p>
              </div>
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    location.pathname.startsWith(item.path)
                      ? "bg-green-700 text-white"
                      : "text-green-100 hover:bg-green-700 hover:text-white"
                  }`}
                >
                  <span className="flex items-center space-x-1">
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </span>
                </Link>
              ))}
            </nav>

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2 rounded-md hover:bg-green-700"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Nav */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-green-800">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="block px-4 py-3 text-sm hover:bg-green-700"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="flex items-center space-x-2">
                  <item.icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </span>
              </Link>
            ))}
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm">
            JIAPI - Justice & Income API | Bangladesh Tax Law Database
          </p>
          <p className="text-xs mt-2">
            Data sourced from bdlaws.minlaw.gov.bd, nbr.gov.bd, Bangladesh Gazette
          </p>
          <p className="text-xs mt-1">
            For research purposes. Verify against official Gazette before filing.
          </p>
        </div>
      </footer>
    </div>
  );
}
