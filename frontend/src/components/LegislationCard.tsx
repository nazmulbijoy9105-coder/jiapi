import { Link } from "react-router-dom";
import { FileText, Calendar, ArrowRight } from "lucide-react";
import type { Legislation } from "../services/api";

interface Props {
  legislation: Legislation;
  era: string;
}

export default function LegislationCard({ legislation, era }: Props) {
  const typeColors: Record<string, string> = {
    act: "bg-blue-100 text-blue-800",
    rule: "bg-green-100 text-green-800",
    finance_act: "bg-purple-100 text-purple-800",
    sro: "bg-orange-100 text-orange-800",
    circular: "bg-pink-100 text-pink-800",
    dtaa: "bg-indigo-100 text-indigo-800",
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${typeColors[legislation.legislation_type] || "bg-gray-100 text-gray-800"}`}>
              {legislation.legislation_type.replace("_", " ").toUpperCase()}
            </span>
            <span className={`px-2 py-1 text-xs rounded-full ${
              legislation.status === "active" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
            }`}>
              {legislation.status}
            </span>
          </div>

          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {legislation.title_en}
          </h3>

          {legislation.title_bn && (
            <p className="text-sm text-gray-600 mb-2">{legislation.title_bn}</p>
          )}

          <div className="flex items-center space-x-4 text-sm text-gray-500 mt-3">
            <span className="flex items-center space-x-1">
              <Calendar className="w-4 h-4" />
              <span>Effective: {legislation.effective_date}</span>
            </span>
            {legislation.fiscal_year && (
              <span className="flex items-center space-x-1">
                <FileText className="w-4 h-4" />
                <span>FY: {legislation.fiscal_year}</span>
              </span>
            )}
          </div>
        </div>

        <Link
          to={`/legislations/${era}/${legislation.id}`}
          className="ml-4 p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
        >
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>
    </div>
  );
}
