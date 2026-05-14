import { useParams, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Calendar, History, GitCompare } from "lucide-react";
import { legislationApi } from "../services/api";

export default function SectionDetailPage() {
  const { era, id, section } = useParams<{ era: string; id: string; section: string }>();
  const [searchParams] = useSearchParams();
  const asOf = searchParams.get("as_of");

  const { data, isLoading } = useQuery({
    queryKey: ["section", era, id, section, asOf],
    queryFn: async () => {
      const response = await legislationApi.getSection(era || "post2023", id || "", section || "", asOf || undefined);
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!data) {
    return <div className="text-center py-12 text-gray-500">Section not found</div>;
  }

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500">
        <a href={`/legislations/${era}`} className="hover:text-primary-600">{era === "post2023" ? "Post-2023" : "Pre-2023"}</a>
        <span className="mx-2">/</span>
        <span>Section {data.numbering}</span>
      </nav>

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Section {data.numbering}
          </h1>
          {data.heading && (
            <p className="text-lg text-gray-600 mt-1">{data.heading}</p>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-3 py-1 text-sm rounded-full ${
            data.is_active !== false ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
          }`}>
            {data.is_active !== false ? "Active" : "Inactive"}
          </span>
        </div>
      </div>

      {/* Point-in-time notice */}
      {asOf && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-center space-x-3">
          <Calendar className="w-5 h-5 text-amber-600" />
          <div>
            <p className="text-sm font-medium text-amber-800">Point-in-Time View</p>
            <p className="text-sm text-amber-700">Showing text as of {asOf}</p>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="card">
        <div className="prose max-w-none">
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
            {data.text_at_date || data.text_current}
          </div>
        </div>

        {data.text_bengali && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-sm font-medium text-gray-500 mb-2">Bengali Text</p>
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed font-bengali">
              {data.text_bengali}
            </div>
          </div>
        )}
      </div>

      {/* Metadata */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="card">
          <div className="flex items-center space-x-2 mb-2">
            <Calendar className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Effective From</span>
          </div>
          <p className="text-sm text-gray-600">{data.effective_from}</p>
        </div>

        <div className="card">
          <div className="flex items-center space-x-2 mb-2">
            <History className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Amendments</span>
          </div>
          <p className="text-sm text-gray-600">{data.amendment_count || 0} amendments</p>
        </div>

        <div className="card">
          <div className="flex items-center space-x-2 mb-2">
            <GitCompare className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Compare</span>
          </div>
          <a 
            href={`/legislations/${era}/${id}/sections/${section}/diff`}
            className="text-sm text-primary-600 hover:underline"
          >
            View changes over time
          </a>
        </div>
      </div>
    </div>
  );
}
