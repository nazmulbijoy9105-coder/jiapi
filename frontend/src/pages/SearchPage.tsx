import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Search, FileText, Gavel, BookOpen } from "lucide-react";
import { searchApi } from "../services/api";
import LegislationCard from "../components/LegislationCard";
import CaseLawCard from "../components/CaseLawCard";

export default function SearchPage() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get("q") || "";

  const { data, isLoading } = useQuery({
    queryKey: ["search", query],
    queryFn: async () => {
      if (!query) return null;
      const response = await searchApi.global(query);
      return response.data;
    },
    enabled: !!query,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Search Results</h1>

      {query && (
        <p className="text-gray-600">
          Results for: <span className="font-semibold">"{query}"</span>
        </p>
      )}

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : data ? (
        <div className="space-y-8">
          {/* Legislations */}
          {data.results?.legislations?.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-primary-600" />
                <span>Legislations ({data.results.legislations.length})</span>
              </h2>
              <div className="space-y-3">
                {data.results.legislations.map((leg: any) => (
                  <LegislationCard key={leg.id} legislation={leg} era={leg.era} />
                ))}
              </div>
            </section>
          )}

          {/* Sections */}
          {data.results?.sections?.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                <FileText className="w-5 h-5 text-primary-600" />
                <span>Sections ({data.results.sections.length})</span>
              </h2>
              <div className="space-y-3">
                {data.results.sections.map((section: any) => (
                  <div key={section.id} className="card">
                    <p className="text-sm font-medium text-primary-700">
                      Section {section.numbering}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">{section.preview}</p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Case Laws */}
          {data.results?.case_laws?.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                <Gavel className="w-5 h-5 text-primary-600" />
                <span>Case Laws ({data.results.case_laws.length})</span>
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {data.results.case_laws.map((c: any) => (
                  <CaseLawCard key={c.id} caseLaw={c} />
                ))}
              </div>
            </section>
          )}

          {data.total === 0 && (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No results found for "{query}"</p>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          Enter a search query to find laws, sections, and case law.
        </div>
      )}
    </div>
  );
}
