import { Gavel, Calendar, AlertTriangle, CheckCircle } from "lucide-react";
import type { CaseLaw } from "../services/api";

interface Props {
  caseLaw: CaseLaw;
}

export default function CaseLawCard({ caseLaw }: Props) {
  const courtLabels: Record<string, string> = {
    appellate_division: "Appellate Division",
    high_court: "High Court Division",
    tat: "Tax Appellate Tribunal",
  };

  const statusIcons: Record<string, React.ReactNode> = {
    good_law: <CheckCircle className="w-4 h-4 text-green-600" />,
    overruled: <AlertTriangle className="w-4 h-4 text-red-600" />,
    distinguished: <AlertTriangle className="w-4 h-4 text-yellow-600" />,
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Gavel className="w-5 h-5 text-primary-600" />
          <span className="text-sm font-medium text-primary-700">
            {courtLabels[caseLaw.court_level] || caseLaw.court_level}
          </span>
        </div>
        <div className="flex items-center space-x-1">
          {statusIcons[caseLaw.status]}
          <span className={`text-xs font-medium ${
            caseLaw.status === "good_law" ? "text-green-700" : "text-red-700"
          }`}>
            {caseLaw.status.replace("_", " ").toUpperCase()}
          </span>
        </div>
      </div>

      <h3 className="text-base font-semibold text-gray-900 mb-2">
        {caseLaw.case_title}
      </h3>

      <p className="text-sm text-gray-600 mb-1">
        <span className="font-medium">Case No:</span> {caseLaw.case_number} / {caseLaw.case_year}
      </p>

      {caseLaw.parties && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {caseLaw.parties}
        </p>
      )}

      {caseLaw.headnotes && (
        <div className="bg-gray-50 rounded-lg p-3 mb-3">
          <p className="text-sm text-gray-700 line-clamp-3">{caseLaw.headnotes}</p>
        </div>
      )}

      <div className="flex items-center space-x-4 text-xs text-gray-500">
        <span className="flex items-center space-x-1">
          <Calendar className="w-3 h-3" />
          <span>Judgment: {caseLaw.judgment_date}</span>
        </span>
        {caseLaw.assessment_year && (
          <span>AY: {caseLaw.assessment_year}</span>
        )}
      </div>
    </div>
  );
}
