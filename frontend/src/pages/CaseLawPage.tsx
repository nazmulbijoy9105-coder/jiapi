import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Gavel } from "lucide-react";
import { caseLawApi } from "../services/api";
import CaseLawCard from "../components/CaseLawCard";
import type { CaseLaw } from "../services/api";

export default function CaseLawPage() {
  const { court } = useParams<{ court?: string }>();

  const { data, isLoading } = useQuery({
    queryKey: ["case-laws", court],
    queryFn: async () => {
      let response;
      if (court === "appellate-division") {
        response = await caseLawApi.getByCourt("appellate-division");
      } else if (court === "high-court") {
        response = await caseLawApi.getByCourt("high-court");
      } else if (court === "tat") {
        response = await caseLawApi.getByCourt("tat");
      } else {
        response = await caseLawApi.getAll();
      }
      return response.data;
    },
  });

  const courtTabs = [
    { key: "", label: "All Courts" },
    { key: "appellate-division", label: "Appellate Division" },
    { key: "high-court", label: "High Court Division" },
    { key: "tat", label: "Tax Appellate Tribunal" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3 mb-2">
        <Gavel className="w-6 h-6 text-primary-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Case Law Database</h1>
          <p className="text-sm text-gray-600">
            Appellate Division, High Court Division, and Tax Appellate Tribunal decisions
          </p>
        </div>
      </div>

      {/* Court Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
        {courtTabs.map((tab) => (
          <a
            key={tab.key}
            href={tab.key ? `/case-laws/${tab.key}` : "/case-laws"}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md text-center transition-colors ${
              (court || "") === tab.key
                ? "bg-white text-gray-900 shadow-sm"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            {tab.label}
          </a>
        ))}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {data?.results?.map((c: CaseLaw) => (
            <CaseLawCard key={c.id} caseLaw={c} />
          ))}
          {(!data?.results || data.results.length === 0) && (
            <div className="col-span-2 text-center py-12 text-gray-500">
              No case law found for the selected court.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
