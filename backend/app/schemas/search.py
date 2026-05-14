"""
JIAPI - Search Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    document_types: Optional[List[str]] = None
    era: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    sector_tags: Optional[List[str]] = None
    page: int = 1
    page_size: int = 20
    highlight: bool = True
    sort_by: str = "relevance"  # relevance, date, title


class SearchResultItem(BaseModel):
    id: UUID
    source_type: str
    title: str
    snippet: str
    highlights: List[str] = []
    url: Optional[str] = None
    metadata: Dict[str, Any] = {}
    score: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    page: int
    page_size: int
    total_pages: int
    results: List[SearchResultItem]
    facets: Dict[str, List[Dict[str, Any]]] = {}
    search_time_ms: int

    class Config:
        from_attributes = True


class AdvancedSearchRequest(BaseModel):
    query: str
    exact_phrase: Optional[str] = None
    exclude_words: Optional[List[str]] = None
    document_types: Optional[List[str]] = None
    court_levels: Optional[List[str]] = None
    years: Optional[List[int]] = None
    authorities: Optional[List[str]] = None
    sector_tags: Optional[List[str]] = None
    era: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    page: int = 1
    page_size: int = 20
    sort_by: str = "relevance"
