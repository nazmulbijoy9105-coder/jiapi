import { useParams, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Filter, BookOpen } from "lucide-react";
import { legislationApi } from "../services/api";
import LegislationCard from "../components/LegislationCard";
import type { Legislation } from "../services/api";

export default function LegislationPage() {
  const { era } = useParams<{ era: string }>();
  const [searchParams] = useSearchParams();
  const typeFilter = searchParams.get("type");

  const { data, isLoading } = useQuery({
    queryKey: ["legislations", era, typeFilter],
    queryFn: async () => {
      const params: Record<string, unknown> = {};
      if (typeFilter) params.legislation_type = typeFilter;

      const response = era === "post2023"
        ? await legislationApi.getPost2023(params)
        : await legislationApi.getPre2023(params);
      return response.data;
    },
  });

  const eraTitle = era === "post2023" ? "Post-2023 Legislation" : "Pre-2023 Legislation";
  const eraDesc = era === "post2023"
    ? "ITA 2023, ITR 2024, Finance Acts, SROs, DTAAs, TP Regulations"
    : "ITO 1984, Finance Acts 1984-2023, Historical SROs & Circulars";

  const typeLabels: Record<string, string> = {
    act: "Acts",
    rule: "Rules",
    finance_act: "Finance Acts",
    sro: "SROs",
    circular: "Circulars",
    dtaa: "DTAAs",
    tp_regulation: "TP Regulations",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3 mb-2">
        <BookOpen className="w-6 h-6 text-primary-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{eraTitle}</h1>
          <p className="text-sm text-gray-600">{eraDesc}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-2">
        <Filter className="w-4 h-4 text-gray-400 flex-shrink-0" />
        {Object.entries(typeLabels).map(([key, label]) => (
          <button
            key={key}
            onClick={() => {
              const url = new URL(window.location.href);
              if (typeFilter === key) {
                url.searchParams.delete("type");
              } else {
                url.searchParams.set("type", key);
              }
              window.location.href = url.toString();
            }}
            className={`px-3 py-1.5 text-sm rounded-full whitespace-nowrap transition-colors ${
              typeFilter === key
                ? "bg-primary-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : (
        <div className="space-y-4">
          {data?.results?.map((leg: Legislation) => (
            <LegislationCard key={leg.id} legislation={leg} era={era || "post2023"} />
          ))}
          {(!data?.results || data.results.length === 0) && (
            <div className="text-center py-12 text-gray-500">
              No legislation found for the selected filters.
            </div>
          )}
        </div>
      )}

      {/* Pagination info */}
      {data && (
        <div className="text-sm text-gray-500 text-center">
          Showing {data.results?.length || 0} of {data.total || 0} results
        </div>
      )}
    </div>
  );
}
