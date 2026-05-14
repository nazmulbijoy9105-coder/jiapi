// ============================================
// JIAPI - Core Type Definitions
// Bangladesh Post-2023 Tax Law API
// ============================================

export interface Legislation {
  id: string;
  era: 'PRE_2023' | 'POST_2023' | 'BOTH';
  type: LegislationType;
  category: string;
  titleEn: string;
  titleBn?: string;
  shortTitle?: string;
  authority: string;
  jurisdiction: string;
  enactmentDate?: string;
  effectiveDate: string;
  repealDate?: string;
  versionNumber: number;
  status: LegislationStatus;
  parentId?: string;
  gazetteRef?: string;
  documentUrl?: string;
  pdfUrl?: string;
  tags: string[];
  keywords: string[];
  sector?: string;
  createdAt: string;
  updatedAt: string;
}

export type LegislationType = 
  | 'ACT' | 'RULES' | 'FINANCE_ACT' | 'VAT_ACT' | 'CUSTOMS_ACT'
  | 'SRO' | 'GENERAL_ORDER' | 'CIRCULAR' | 'DTAA' 
  | 'BEPS_REFERENCE' | 'TP_REGULATION' | 'COMPLIANCE_MANUAL';

export type LegislationStatus = 
  | 'ACTIVE' | 'AMENDED' | 'REPEALED' | 'SUPERSEDED' | 'DRAFT' | 'PROPOSED';

export interface ContentBlock {
  id: string;
  legislationId: string;
  blockType: BlockType;
  numbering: string;
  heading?: string;
  textOriginal: string;
  textCurrent: string;
  effectiveFrom: string;
  effectiveTo?: string;
  parentId?: string;
  children?: ContentBlock[];
  displayOrder: number;
  amendments: Amendment[];
  caseReferences: CaseLawProvision[];
  crossReferences?: ContentBlock[];
  createdAt: string;
  updatedAt: string;
}

export type BlockType = 
  | 'CHAPTER' | 'PART' | 'SECTION' | 'SUBSECTION' | 'CLAUSE' 
  | 'SUBCLAUSE' | 'PARAGRAPH' | 'SCHEDULE' | 'TABLE' | 'FORMULA' 
  | 'DEFINITION' | 'PREAMBLE';

export interface Amendment {
  id: string;
  sourceLegislationId: string;
  sourceLegislation?: Legislation;
  targetBlockId: string;
  targetBlock?: ContentBlock;
  changeType: ChangeType;
  oldText?: string;
  newText?: string;
  oldNumbering?: string;
  newNumbering?: string;
  effectiveDate: string;
  notificationDate: string;
  gazetteDate?: string;
  status: AmendmentStatus;
  appliedAt?: string;
  appliedBy?: string;
  verifiedBy?: string;
  verifiedAt?: string;
  createdAt: string;
}

export type ChangeType = 'INSERT' | 'DELETE' | 'SUBSTITUTE' | 'RENUMBER' | 'REPEAL' | 'INSERT_AFTER' | 'INSERT_BEFORE';
export type AmendmentStatus = 'PENDING' | 'VERIFIED' | 'APPLIED' | 'ROLLED_BACK' | 'REJECTED';

export interface CaseLaw {
  id: string;
  caseNumber: string;
  year: number;
  court: CourtLevel;
  bench?: string;
  petitioner: string;
  respondent: string;
  filingDate?: string;
  judgmentDate: string;
  headnotes: string;
  fullText?: string;
  pdfUrl?: string;
  status: CaseStatus;
  precedentValue: number;
  overruledById?: string;
  eraReferenced: Era;
  provisions: CaseLawProvision[];
  citations: string[];
  parallelCitations: string[];
  judges: string[];
  lawyersFor: string[];
  lawyersAgainst: string[];
  assessmentYear?: string;
  taxAmount?: number;
  createdAt: string;
  updatedAt: string;
}

export type CourtLevel = 
  | 'APPELLATE_DIVISION' | 'HIGH_COURT_DIVISION' | 'TAX_APPELLATE_TRIBUNAL' 
  | 'DISTRICT_COURT' | 'SPECIAL_JUDGE';

export type CaseStatus = 'GOOD_LAW' | 'OVERRULED' | 'DISTINGUISHED' | 'FOLLOWED' | 'DOUBTED' | 'PENDING_APPEAL';
export type Era = 'PRE_2023' | 'POST_2023' | 'BOTH';

export interface CaseLawProvision {
  id: string;
  caseLawId: string;
  contentBlockId: string;
  contentBlock?: ContentBlock;
  treatment: ProvisionTreatment;
  paragraphRef?: string;
  quote?: string;
  createdAt: string;
}

export type ProvisionTreatment = 'INTERPRETED' | 'APPLIED' | 'DISTINGUISHED' | 'DISCUSSED' | 'OVERRULED' | 'FOLLOWED';

export interface Dtaa {
  id: string;
  country: string;
  countryCode: string;
  treatyName: string;
  signedDate?: string;
  effectiveDate: string;
  protocolDate?: string;
  status: TreatyStatus;
  articles: DtaaArticle[];
  limitationOfBenefits: boolean;
  tiea: boolean;
  dividendRate?: number;
  interestRate?: number;
  royaltyRate?: number;
  pdfUrl?: string;
  createdAt: string;
  updatedAt: string;
}

export interface DtaaArticle {
  id: string;
  dtaaId: string;
  articleNumber: string;
  title: string;
  content: string;
  articleType: DtaaArticleType;
  displayOrder: number;
  createdAt: string;
}

export type DtaaArticleType = 
  | 'RESIDENCE' | 'PERMANENT_ESTABLISHMENT' | 'INCOME_FROM_IMMovable_PROPERTY'
  | 'BUSINESS_PROFITS' | 'SHIPPING_AIR_TRANSPORT' | 'DIVIDENDS' | 'INTEREST'
  | 'ROYALTIES' | 'CAPITAL_GAINS' | 'EMPLOYMENT_INCOME' | 'DIRECTORS_FEES'
  | 'ARTISTES_SPORTSMEN' | 'PENSIONS' | 'GOVERNMENT_SERVICE' | 'STUDENTS'
  | 'OTHER_INCOME' | 'ELIMINATION_DOUBLE_TAXATION' | 'NON_DISCRIMINATION'
  | 'MUTUAL_AGREEMENT_PROCEDURE' | 'EXCHANGE_OF_INFORMATION' 
  | 'ASSISTANCE_COLLECTION' | 'MEMBERS_OF_DIPLOMATIC_MISSIONS'
  | 'TERRITORIAL_SCOPE' | 'ENTRY_INTO_FORCE' | 'TERMINATION'
  | 'LIMITATIONS_BENEFITS' | 'OTHER';

export type TreatyStatus = 'ACTIVE' | 'SUSPENDED' | 'TERMINATED' | 'NEGOTIATING' | 'SIGNED_NOT_EFFECTIVE';

export interface NbrInstrument {
  id: string;
  instrumentType: NbrInstrumentType;
  number: string;
  year: number;
  titleEn: string;
  titleBn?: string;
  issuingWing: string;
  issuedBy: string;
  issueDate: string;
  effectiveDate: string;
  expiryDate?: string;
  summary?: string;
  fullText: string;
  pdfUrl?: string;
  applicableTo: string[];
  taxYears: string[];
  status: InstrumentStatus;
  supersededById?: string;
  createdAt: string;
  updatedAt: string;
}

export type NbrInstrumentType = 'SRO' | 'GENERAL_ORDER' | 'CIRCULAR' | 'ORDER' | 'NOTIFICATION' | 'OFFICE_ORDER';
export type InstrumentStatus = 'ACTIVE' | 'EXPIRED' | 'SUPERSEDED' | 'WITHDRAWN' | 'PROPOSED';

// ============================================
// API RESPONSE TYPES
// ============================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: PaginationMeta;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

export interface SectionWithHistory {
  block: ContentBlock;
  history: Amendment[];
  pointInTimeVersions: PointInTimeVersion[];
  relatedCases: CaseLaw[];
  crossReferences: CrossReference[];
}

export interface PointInTimeVersion {
  asOfDate: string;
  text: string;
  appliedAmendments: Amendment[];
}

export interface CrossReference {
  blockId: string;
  legislationShortTitle: string;
  numbering: string;
  heading?: string;
  relationship: 'references' | 'referenced_by';
}

export interface DiffResult {
  fromDate: string;
  toDate: string;
  additions: DiffChunk[];
  deletions: DiffChunk[];
  modifications: DiffChunk[];
}

export interface DiffChunk {
  oldText?: string;
  newText?: string;
  lineStart: number;
  lineEnd: number;
  amendment?: Amendment;
}

export interface SearchResult {
  results: SearchResultItem[];
  facets: SearchFacets;
  meta: PaginationMeta;
}

export interface SearchResultItem {
  id: string;
  type: 'legislation' | 'content_block' | 'case_law' | 'dtaa' | 'nbr_instrument';
  title: string;
  excerpt: string;
  highlight: string;
  score: number;
  url: string;
  metadata: Record<string, unknown>;
}

export interface SearchFacets {
  byType: Record<string, number>;
  byYear: Record<string, number>;
  byCourt?: Record<string, number>;
  byAuthority: Record<string, number>;
}

export interface WebhookPayload {
  event: WebhookEvent;
  timestamp: string;
  data: unknown;
  signature: string;
}

export type WebhookEvent = 
  | 'AMENDMENT_APPLIED' | 'AMENDMENT_PENDING' | 'LEGISLATION_REPEALED'
  | 'CASE_LAW_ADDED' | 'SRO_ISSUED' | 'CIRCULAR_ISSUED'
  | 'SECTION_CHANGED' | 'RATE_CHANGE';

export interface RateLimitInfo {
  limit: number;
  remaining: number;
  resetAt: string;
  window: string;
}

export interface ApiKeyInfo {
  id: string;
  name?: string;
  prefix: string;
  tier: SubscriptionTier;
  rateLimitPerMinute: number;
  dailyQuota: number;
  allowedEndpoints: string[];
  isActive: boolean;
  expiresAt?: string;
  lastUsedAt?: string;
}

export type SubscriptionTier = 'FREE' | 'BASIC' | 'PROFESSIONAL' | 'ENTERPRISE' | 'LAW_FIRM';

export interface TierLimits {
  tier: SubscriptionTier;
  monthlyRequests: number;
  rateLimitPerMinute: number;
  allowedEndpoints: string[];
  features: string[];
  priceBdt: number;
}

export const TIER_LIMITS: TierLimits[] = [
  {
    tier: 'FREE',
    monthlyRequests: 100,
    rateLimitPerMinute: 10,
    allowedEndpoints: ['acts', 'rules'],
    features: ['Bare text access', 'Basic search'],
    priceBdt: 0,
  },
  {
    tier: 'BASIC',
    monthlyRequests: 1000,
    rateLimitPerMinute: 60,
    allowedEndpoints: ['acts', 'rules', 'finance-acts', 'sros', 'circulars'],
    features: ['Full acts + rules', 'SROs & circulars', 'Basic search'],
    priceBdt: 2000,
  },
  {
    tier: 'PROFESSIONAL',
    monthlyRequests: 10000,
    rateLimitPerMinute: 120,
    allowedEndpoints: ['*'],
    features: ['All legislation', 'Amendment history', 'Diff views', 'Point-in-time queries', 'Advanced search'],
    priceBdt: 8000,
  },
  {
    tier: 'ENTERPRISE',
    monthlyRequests: 100000,
    rateLimitPerMinute: 300,
    allowedEndpoints: ['*'],
    features: ['Everything', 'Case law', 'Webhooks', 'API SLA', 'Dedicated support', 'Citation checker'],
    priceBdt: 25000,
  },
  {
    tier: 'LAW_FIRM',
    monthlyRequests: 500000,
    rateLimitPerMinute: 600,
    allowedEndpoints: ['*'],
    features: ['Everything', 'Bulk downloads', 'Annotated versions', 'Custom integrations', 'Training'],
    priceBdt: 50000,
  },
];
