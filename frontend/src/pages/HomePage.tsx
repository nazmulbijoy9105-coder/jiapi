import { Link } from "react-router-dom";
import { BookOpen, Gavel, Globe, FileText, ArrowRight, Shield, Zap, Database } from "lucide-react";
import SearchBar from "../components/SearchBar";

export default function HomePage() {
  const features = [
    {
      icon: BookOpen,
      title: "Post-2023 Tax Laws",
      description: "ITA 2023, ITR 2024, Finance Acts, SROs, Circulars — all with amendment tracking",
      link: "/legislations/post2023",
      color: "bg-blue-50 text-blue-700",
    },
    {
      icon: FileText,
      title: "Pre-2023 Archive",
      description: "Complete ITO 1984 with all amendments through FY 2022-23",
      link: "/legislations/pre2023",
      color: "bg-amber-50 text-amber-700",
    },
    {
      icon: Gavel,
      title: "Case Law Database",
      description: "AD, HCD, and TAT decisions with citation checker",
      link: "/case-laws",
      color: "bg-green-50 text-green-700",
    },
    {
      icon: Globe,
      title: "DTAAs & International",
      description: "35+ Double Taxation Avoidance Agreements + OECD BEPS references",
      link: "/legislations/post2023?type=dtaa",
      color: "bg-indigo-50 text-indigo-700",
    },
  ];

  const capabilities = [
    { icon: Zap, title: "Point-in-Time Queries", desc: "See the law as it existed on any specific date" },
    { icon: Shield, title: "Amendment Diff Engine", desc: "Compare legislation across time periods" },
    { icon: Database, title: "Citation Checker", desc: "Verify if case law is still good law" },
  ];

  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-12">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium mb-6">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span>Commercial-Grade Bangladesh Tax Law API</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Justice & Income API
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Comprehensive database of Bangladesh income tax laws, case law, and international treaties — 
          with real-time amendment tracking and point-in-time queries.
        </p>

        <SearchBar />

        <div className="flex flex-wrap justify-center gap-4 mt-8 text-sm text-gray-500">
          <span>ITA 2023</span>
          <span>•</span>
          <span>ITO 1984</span>
          <span>•</span>
          <span>Finance Acts</span>
          <span>•</span>
          <span>SROs</span>
          <span>•</span>
          <span>DTAAs</span>
          <span>•</span>
          <span>Case Law</span>
        </div>
      </section>

      {/* Feature Cards */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Browse by Category</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature) => (
            <Link
              key={feature.title}
              to={feature.link}
              className="group card hover:shadow-lg transition-all"
            >
              <div className={`w-12 h-12 rounded-lg ${feature.color} flex items-center justify-center mb-4`}>
                <feature.icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-primary-600">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-600 mb-4">{feature.description}</p>
              <span className="inline-flex items-center text-sm text-primary-600 font-medium">
                Browse <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* Capabilities */}
      <section className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Core Capabilities</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {capabilities.map((cap) => (
            <div key={cap.title} className="text-center">
              <div className="w-14 h-14 bg-primary-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                <cap.icon className="w-7 h-7 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{cap.title}</h3>
              <p className="text-sm text-gray-600">{cap.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Data Sources */}
      <section className="text-center py-8">
        <h2 className="text-lg font-semibold text-gray-700 mb-4">Trusted Data Sources</h2>
        <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-500">
          <span>bdlaws.minlaw.gov.bd</span>
          <span>nbr.gov.bd</span>
          <span>Bangladesh Gazette</span>
          <span>Supreme Court Library</span>
        </div>
      </section>
    </div>
  );
}
