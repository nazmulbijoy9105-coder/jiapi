"""
JIAPI - Shared Enumerations
"""
from enum import Enum


class Era(str, Enum):
    POST_2023 = "post2023"
    PRE_2023 = "pre2023"


class LegislationType(str, Enum):
    ACT = "act"
    RULE = "rule"
    FINANCE_ACT = "finance_act"
    VAT_ACT = "vat_act"
    CUSTOMS_ACT = "customs_act"
    SRO = "sro"
    GENERAL_ORDER = "general_order"
    CIRCULAR = "circular"
    DTAA = "dtaa"
    BEPS = "beps"
    TP_REGULATION = "tp_regulation"
    COMPLIANCE_MANUAL = "compliance_manual"


class LegislationStatus(str, Enum):
    ACTIVE = "active"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"
    DRAFT = "draft"


class CourtLevel(str, Enum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"
    SUPREME_COURT_OTHER = "supreme_court_other"


class CaseStatus(str, Enum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    PENDING = "pending"


class ChangeType(str, Enum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    ADD_SCHEDULE = "add_schedule"


class BlockType(str, Enum):
    SECTION = "section"
    SUBSECTION = "subsection"
    CLAUSE = "clause"
    SUBCLAUSE = "subclause"
    PARAGRAPH = "paragraph"
    SCHEDULE = "schedule"
    TABLE = "table"
    DEFINITION = "definition"
    FORMULA = "formula"


class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    RESEARCHER = "researcher"
    SUBSCRIBER_BASIC = "subscriber_basic"
    SUBSCRIBER_PRO = "subscriber_pro"
    SUBSCRIBER_ENTERPRISE = "subscriber_enterprise"
