"""
JIAPI - Post-2023 Legislation Router
ITA 2023, ITR 2024, Finance Acts, SROs, Circulars, TP Regulations
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from datetime import date
from app.schemas import (
    LegislationResponse, ContentBlockResponse, AmendmentResponse,
    PointInTimeQuery, PointInTimeResponse, DiffQuery, DiffResponse,
    SROBase, SROResponse, CircularBase, CircularResponse
)
from app.core.security import get_current_user

router = APIRouter()


# ==================== ITA 2023 ====================

@router.get("/acts/ita2023", response_model=LegislationResponse)
async def get_ita2023(current_user: dict = Depends(get_current_user)):
    """
    Get the complete Income Tax Act 2023.

    Returns the full act with metadata, sections count, and current status.
    """
    return {
        "id": "ita2023-primary",
        "era": "post2023",
        "legislation_type": "act",
        "title_en": "Income Tax Act, 2023",
        "title_bn": "আয়কর আইন, ২০২৩",
        "short_title": "ITA 2023",
        "act_number": "Act No. XII of 2023",
        "year": 2023,
        "authority": "Parliament of Bangladesh",
        "effective_date": date(2023, 7, 1),
        "status": "active",
        "preamble": """An Act to make a new law upon repealing the Income-tax Ordinance, 1984 
        by updating and in a time befitting manner""",
        "total_sections": 345,
        "total_schedules": 7,
        "keywords": ["income tax", "assessment", "tax deduction", "advance tax", "minimum tax"],
        "created_at": "2023-10-08T00:00:00",
        "updated_at": "2025-09-04T00:00:00",
        "document_url": "https://nbr.gov.bd/uploads/acts/Income_tax_act_2023.pdf"
    }


@router.get("/acts/ita2023/sections/{section_number}", response_model=ContentBlockResponse)
async def get_ita2023_section(
    section_number: str = Path(..., description="Section number (e.g., 30, 30(1))"),
    as_of: Optional[date] = Query(None, description="Get text as of specific date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific section of ITA 2023.

    - **section_number**: Section number (e.g., "30", "30(1)", "30(1)(a)")
    - **as_of**: Optional date for point-in-time query

    Returns current text with amendment history.
    """
    # Sample data - in production this queries the database
    sample_sections = {
        "30": {
            "id": "sec-30",
            "legislation_id": "ita2023-primary",
            "block_type": "section",
            "numbering": "30",
            "heading_en": "Deduction of tax from salaries",
            "heading_bn": "বেতন থেকে কর কর্তন",
            "text_original": """(1) Any person responsible for paying any income chargeable under the head \"Salaries\" shall, at the time of payment, deduct tax on the amount payable at the average rate of tax applicable to the estimated income of the assessee under this head.""",
            "text_current": """(1) Any person responsible for paying any income chargeable under the head \"Salaries\" shall, at the time of payment, deduct tax on the amount payable at the average rate of tax applicable to the estimated income of the assessee under this head.

(2) The rate of deduction under sub-section (1) shall be determined based on the tax rates specified in the Finance Act for the relevant assessment year.""",
            "text_bengali": None,
            "effective_from": date(2023, 7, 1),
            "effective_to": None,
            "display_order": 30,
            "level": 0,
            "is_active": True,
            "is_repealed": False,
            "cross_references": [
                {"section": "31", "act": "ITA 2023", "description": "Deduction from interest on securities"},
                {"section": "32", "act": "ITA 2023", "description": "Deduction from interest other than interest on securities"}
            ],
            "keywords": ["TDS", "salary", "employer", "deduction", "withholding"]
        },
        "89": {
            "id": "sec-89",
            "legislation_id": "ita2023-primary",
            "block_type": "section",
            "numbering": "89",
            "heading_en": "Deduction of tax from payment to contractors",
            "heading_bn": "ঠিকাদারদের অর্থপ্রদান থেকে কর কর্তন",
            "text_original": """(1) Any person responsible for paying any sum to a contractor shall deduct tax at the time of credit or payment, whichever is earlier.""",
            "text_current": """(1) Any person responsible for paying any sum to a contractor shall deduct tax at the time of credit or payment, whichever is earlier.

Rates:
- Up to Tk. 50,00,000: 3%
- Above Tk. 50,00,000 but below Tk. 2,00,00,000: 5%
- Above Tk. 2,00,00,000: 7%

(2) The rate shall be 50% higher if the payee fails to submit proof of submission of return.""",
            "effective_from": date(2023, 7, 1),
            "effective_to": None,
            "display_order": 89,
            "level": 0,
            "is_active": True,
            "is_repealed": False,
            "cross_references": [
                {"section": "90", "act": "ITA 2023", "description": "Deduction from payment to suppliers"}
            ],
            "keywords": ["contractor", "TDS", "withholding", "construction", "supply"]
        },
        "233": {
            "id": "sec-233",
            "legislation_id": "ita2023-primary",
            "block_type": "section",
            "numbering": "233",
            "heading_en": "Transfer pricing - International transactions",
            "heading_bn": "ট্রান্সফার প্রাইসিং - আন্তর্জাতিক লেনদেন",
            "text_original": """(1) Any income or expenditure arising from an international transaction shall be determined having regard to the arm's length price.""",
            "text_current": """(1) Any income or expenditure arising from an international transaction shall be determined having regard to the arm's length price.

(2) For the purposes of this section, \"arm's length price\" means a price which is applied or proposed to be applied in a transaction between persons other than associated enterprises.""",
            "effective_from": date(2023, 7, 1),
            "effective_to": None,
            "display_order": 233,
            "level": 0,
            "is_active": True,
            "is_repealed": False,
            "cross_references": [
                {"section": "234", "act": "ITA 2023", "description": "Computation of arm's length price"},
                {"section": "235", "act": "ITA 2023", "description": "Documentation requirements"},
                {"section": "236", "act": "ITA 2023", "description": "Accountant's report"}
            ],
            "keywords": ["transfer pricing", "international transaction", "arm's length", "OECD", "BEPS"]
        }
    }

    if section_number not in sample_sections:
        raise HTTPException(status_code=404, detail=f"Section {section_number} not found in ITA 2023")

    return sample_sections[section_number]


@router.get("/acts/ita2023/sections", response_model=List[ContentBlockResponse])
async def list_ita2023_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """List all sections of ITA 2023 with pagination"""
    return []


# ==================== ITR 2024 ====================

@router.get("/rules/itr2024", response_model=LegislationResponse)
async def get_itr2024(current_user: dict = Depends(get_current_user)):
    """
    Get Income Tax Rules 2024.

    Supporting rules for ITA 2023 implementation.
    """
    return {
        "id": "itr2024-primary",
        "era": "post2023",
        "legislation_type": "rules",
        "title_en": "Income Tax Rules, 2024",
        "title_bn": "আয়কর বিধিমালা, ২০২৪",
        "short_title": "ITR 2024",
        "year": 2024,
        "authority": "National Board of Revenue",
        "effective_date": date(2024, 7, 1),
        "status": "active",
        "total_sections": 0,
        "total_schedules": 0,
        "keywords": ["rules", "procedures", "forms", "returns"],
        "created_at": "2024-07-01T00:00:00",
        "updated_at": "2024-07-01T00:00:00"
    }


# ==================== Finance Acts ====================

@router.get("/finance-acts", response_model=List[LegislationResponse])
async def list_finance_acts(
    year: Optional[int] = Query(None, description="Filter by year"),
    current_user: dict = Depends(get_current_user)
):
    """
    List Finance Acts (annual amendments to tax rates and exemptions).

    Each Finance Act amends ITA 2023 rates, exemptions, and thresholds for the fiscal year.
    """
    finance_acts = [
        {
            "id": "fa-2023",
            "era": "post2023",
            "legislation_type": "finance_act",
            "title_en": "Finance Act, 2023",
            "short_title": "FA 2023",
            "year": 2023,
            "authority": "Parliament of Bangladesh",
            "effective_date": date(2023, 7, 1),
            "status": "active",
            "keywords": ["budget", "tax rates", "exemptions"],
            "created_at": "2023-06-01T00:00:00",
            "updated_at": "2023-06-01T00:00:00"
        },
        {
            "id": "fa-2024",
            "era": "post2023",
            "legislation_type": "finance_act",
            "title_en": "Finance Act, 2024",
            "short_title": "FA 2024",
            "year": 2024,
            "authority": "Parliament of Bangladesh",
            "effective_date": date(2024, 7, 1),
            "status": "active",
            "keywords": ["budget", "tax rates", "exemptions", "corporate tax"],
            "created_at": "2024-06-01T00:00:00",
            "updated_at": "2024-06-01T00:00:00"
        },
        {
            "id": "fa-2025",
            "era": "post2023",
            "legislation_type": "finance_act",
            "title_en": "Finance Act, 2025",
            "short_title": "FA 2025",
            "year": 2025,
            "authority": "Parliament of Bangladesh",
            "effective_date": date(2025, 7, 1),
            "status": "active",
            "keywords": ["budget", "tax rates", "minimum tax", "gross receipts"],
            "created_at": "2025-06-01T00:00:00",
            "updated_at": "2025-09-04T00:00:00"
        }
    ]

    if year:
        finance_acts = [fa for fa in finance_acts if fa["year"] == year]

    return finance_acts


@router.get("/finance-acts/{finance_act_id}", response_model=LegislationResponse)
async def get_finance_act(
    finance_act_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific Finance Act with all amendments"""
    raise HTTPException(status_code=501, detail="Coming soon")


# ==================== Cross-Reference Acts ====================

@router.get("/cross-reference/vat2012", response_model=LegislationResponse)
async def get_vat_act_2012(current_user: dict = Depends(get_current_user)):
    """
    Get VAT and Supplementary Duty Act 2012.

    Cross-reference for business income adjustments.
    """
    return {
        "id": "vat-2012",
        "era": "post2023",
        "legislation_type": "vat_act",
        "title_en": "Value Added Tax and Supplementary Duty Act, 2012",
        "short_title": "VAT Act 2012",
        "year": 2012,
        "authority": "Parliament of Bangladesh",
        "effective_date": date(2012, 1, 1),
        "status": "active",
        "keywords": ["VAT", "supplementary duty", "business income", "input tax"],
        "created_at": "2012-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@router.get("/cross-reference/customs1969", response_model=LegislationResponse)
async def get_customs_act_1969(current_user: dict = Depends(get_current_user)):
    """
    Get Customs Act 1969.

    Cross-reference for import income adjustments.
    """
    return {
        "id": "customs-1969",
        "era": "pre2023",
        "legislation_type": "customs_act",
        "title_en": "Customs Act, 1969",
        "short_title": "Customs Act 1969",
        "year": 1969,
        "authority": "Parliament of Bangladesh",
        "effective_date": date(1969, 1, 1),
        "status": "active",
        "keywords": ["customs", "import", "duty", "tariff"],
        "created_at": "1969-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }


# ==================== Point-in-Time & Diff ====================

@router.post("/point-in-time", response_model=PointInTimeResponse)
async def get_point_in_time(
    query: PointInTimeQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Get legislation text as it existed on a specific date.

    This is the core amendment tracking feature. Provide:
    - legislation_id: The act ID
    - section_number: Specific section (optional - gets full act if omitted)
    - as_of_date: Date in YYYY-MM-DD format
    """
    return {
        "legislation": {
            "id": query.legislation_id,
            "era": "post2023",
            "legislation_type": "act",
            "title_en": "Income Tax Act, 2023",
            "year": 2023,
            "authority": "Parliament",
            "effective_date": date(2023, 7, 1),
            "status": "active",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        "section": None,
        "text_as_of_date": "Text as of " + str(query.as_of_date),
        "amendments_applied": [],
        "next_amendment": None
    }


@router.post("/diff", response_model=DiffResponse)
async def get_diff(
    query: DiffQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Compare legislation between two dates.

    Shows exactly what changed, which amendments were applied, and visual diff.
    """
    return {
        "legislation_id": query.legislation_id,
        "section_number": query.section_number,
        "from_date": query.from_date,
        "to_date": query.to_date,
        "old_text": "Original text before amendments",
        "new_text": "Updated text after amendments",
        "changes": [],
        "diff_html": "<div class='diff'><span class='removed'>Removed</span><span class='added'>Added</span></div>"
    }


# ==================== Tax Rates & Schedules ====================

@router.get("/tax-rates/individual")
async def get_individual_tax_rates(
    assessment_year: str = Query(..., description="e.g., 2024-2025"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get individual tax rates for specific assessment year.

    Includes all slabs, exemptions, and special categories.
    """
    return {
        "assessment_year": assessment_year,
        "resident_individual": [
            {"slab": "First Tk. 350,000", "rate": 0, "category": "general"},
            {"slab": "Next Tk. 100,000", "rate": 5, "category": "general"},
            {"slab": "Next Tk. 300,000", "rate": 10, "category": "general"},
            {"slab": "Next Tk. 400,000", "rate": 15, "category": "general"},
            {"slab": "Next Tk. 500,000", "rate": 20, "category": "general"},
            {"slab": "On the balance", "rate": 25, "category": "general"}
        ],
        "special_categories": {
            "women_senior_citizens": {"initial_exemption": 400000},
            "physically_challenged": {"initial_exemption": 475000},
            "war_wounded_freedom_fighters": {"initial_exemption": 500000},
            "parent_of_physically_challenged": {"additional_exemption": 50000}
        },
        "non_resident": {"rate": 30},
        "minimum_tax": {
            "dhaka_chattogram_city": 5000,
            "other_city_corporation": 4000,
            "other_areas": 3000
        },
        "surcharge": [
            {"net_worth": "Over 40M to 100M", "rate": 10},
            {"net_worth": "Over 100M to 200M", "rate": 20},
            {"net_worth": "Over 200M to 500M", "rate": 30},
            {"net_worth": "Over 500M", "rate": 35}
        ]
    }


@router.get("/tax-rates/corporate")
async def get_corporate_tax_rates(
    assessment_year: str = Query(..., description="e.g., 2024-2025"),
    current_user: dict = Depends(get_current_user)
):
    """Get corporate tax rates for specific assessment year"""
    return {
        "assessment_year": assessment_year,
        "rates": [
            {"category": "Publicly traded companies", "rate": 20},
            {"category": "Non-publicly traded companies", "rate": 27.5},
            {"category": "Mobile phone companies (non-listed)", "rate": 45},
            {"category": "Mobile phone companies (listed)", "rate": 45},
            {"category": "Banks/Insurance/MFS (listed)", "rate": 37.5},
            {"category": "Banks/Insurance/MFS (non-listed)", "rate": 40},
            {"category": "Merchant banks", "rate": 37.5},
            {"category": "Tobacco/Cigarette manufacturing", "rate": 45},
            {"category": "One Person Companies", "rate": 22.5},
            {"category": "Co-Operative Society", "rate": 15},
            {"category": "Private University/Medical/IT", "rate": 15}
        ],
        "banking_channel_requirement": {
            "threshold_single": 500000,
            "threshold_annual": 3600000,
            "penalty_rate_increase": 2.5
        }
    }


# ==================== Withholding Tax Rates ====================

@router.get("/withholding-rates")
async def get_withholding_rates(
    current_user: dict = Depends(get_current_user)
):
    """
    Get all withholding tax rates (TDS/TCS) under ITA 2023.

    Organized by section number with conditions.
    """
    return {
        "sections": [
            {"section": "30", "description": "Salaries", "rate": "Average rate", "conditions": "Based on estimated income"},
            {"section": "89", "description": "Contractors", "rate": "3%/5%/7%", "conditions": "Slab based; 50% higher without return"},
            {"section": "90", "description": "Suppliers", "rate": "3%/5%/7%", "conditions": "Slab based"},
            {"section": "124", "description": "Service charge, fees, commission", "rate": "7.5%/10%", "conditions": "Based on nature of service"},
            {"section": "128", "description": "Lease of property", "rate": "10%", "conditions": "All lease payments"},
            {"section": "134", "description": "Transfer of shares (non-listed)", "rate": "15%", "conditions": "On difference between fair and face value"},
            {"section": "135", "description": "Transfer of securities", "rate": "10%", "conditions": "Sponsor/director/placement shares"},
            {"section": "137", "description": "Commercially operated motor vehicles", "rate": "0.05%", "conditions": "Depends on vehicle type"}
        ],
        "note": "Rates are subject to change by annual Finance Acts and SROs"
    }


# ==================== Transfer Pricing ====================

@router.get("/tp-regulations")
async def get_tp_regulations(current_user: dict = Depends(get_current_user)):
    """
    Get Transfer Pricing Regulations under ITA 2023.

    Chapter on international transactions (Sections 233-239).
    """
    return {
        "chapter": "International Transactions",
        "sections_covered": ["233", "234", "235", "236", "237", "238", "239"],
        "arm_length_methods": [
            {"method": "CUP", "name": "Comparable Uncontrolled Price", "description": "Compares price in controlled transaction with price in comparable uncontrolled transaction"},
            {"method": "RPM", "name": "Resale Price Method", "description": "Appropriate gross margin is determined"},
            {"method": "CP", "name": "Cost Plus Method", "description": "Appropriate markup on costs is determined"},
            {"method": "PSM", "name": "Profit Split Method", "description": "Profits are split between associated enterprises"},
            {"method": "TNMM", "name": "Transactional Net Margin Method", "description": "Net profit margin is compared"},
            {"method": "Other", "name": "Any Other Method", "description": "Residual category when none of above is suitable"}
        ],
        "documentation_requirements": {
            "threshold": "International transactions exceeding Tk. 3 crore",
            "master_file": "Required for MNE groups",
            "local_file": "Required for Bangladesh entities",
            "deadline": "Within 30 days of requisition by DCT"
        },
        "penalty_provisions": {
            "section_276": "Failure to comply with notice - up to 1% of transaction value",
            "section_277": "Failure to maintain documents - up to 1% of transaction value",
            "section_278": "Failure to furnish report - up to 2% of transaction value",
            "section_279": "Failure to furnish accountant report - up to Tk. 3 lakh"
        },
        "oecd_alignment": "Broadly aligned with OECD Guidelines though Bangladesh is not OECD member"
    }


# ==================== BEPS References ====================

@router.get("/beps")
async def get_beps_references(current_user: dict = Depends(get_current_user)):
    """
    Get OECD BEPS framework references.

    Non-binding but increasingly cited in Bangladesh tax practice.
    """
    return {
        "note": "BEPS framework is non-binding in Bangladesh but increasingly cited",
        "actions": [
            {
                "action": "Action 1",
                "title": "Addressing the Tax Challenges of the Digital Economy",
                "bd_relevance": "Growing relevance with digital service taxation",
                "bd_status": "pending"
            },
            {
                "action": "Action 2",
                "title": "Neutralising the Effects of Hybrid Mismatch Arrangements",
                "bd_relevance": "Relevant for MNE structures",
                "bd_status": "pending"
            },
            {
                "action": "Action 5",
                "title": "Countering Harmful Tax Practices",
                "bd_relevance": "Relevant for tax holiday regimes",
                "bd_status": "partially_adopted"
            },
            {
                "action": "Action 6",
                "title": "Preventing Treaty Abuse",
                "bd_relevance": "Principal Purpose Test included in recent treaties",
                "bd_status": "adopted"
            },
            {
                "action": "Action 13",
                "title": "Transfer Pricing Documentation and CbCR",
                "bd_relevance": "Documentation requirements under ITA 2023 Section 235",
                "bd_status": "adopted"
            }
        ],
        "related_ita2023_sections": ["233", "234", "235", "236", "237", "238", "239"],
        "binding": False
    }


# ==================== Compliance Manual ====================

@router.get("/compliance-manual")
async def get_compliance_manual(current_user: dict = Depends(get_current_user)):
    """Get NBR Tax Compliance Manual"""
    return {
        "title": "NBR Tax Compliance Manual",
        "version": "2024-1",
        "effective_date": date(2024, 7, 1),
        "is_current": True,
        "chapters": [
            {"chapter": 1, "title": "Registration and TIN", "description": "Procedures for obtaining TIN"},
            {"chapter": 2, "title": "Return Filing", "description": "Self-assessment return procedures"},
            {"chapter": 3, "title": "Assessment", "description": "Regular and best judgment assessment"},
            {"chapter": 4, "title": "Audit", "description": "Tax audit procedures and selection"},
            {"chapter": 5, "title": "Appeals", "description": "Appeal procedures to AJC, Tribunal, HCD"},
            {"chapter": 6, "title": "Transfer Pricing", "description": "TP audit and documentation"},
            {"chapter": 7, "title": "Withholding Tax", "description": "TDS/TCS compliance"},
            {"chapter": 8, "title": "Penalties", "description": "Penalty imposition procedures"}
        ]
    }


# ==================== Amendment Feed ====================

@router.get("/amendments/feed")
async def get_amendment_feed(
    limit: int = Query(20, ge=1, le=100),
    priority: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Get feed of latest amendments.

    Subscribe to webhooks for real-time notifications.
    """
    return {
        "total": 3,
        "items": [
            {
                "id": "amd-001",
                "title": "Finance Act 2025 - Corporate Tax Rate Changes",
                "description": "General corporate tax rate reduced to 27.5% for non-listed entities",
                "affected_sections": ["Rate Schedule"],
                "priority": "high",
                "effective_date": date(2025, 7, 1),
                "created_at": datetime.now()
            },
            {
                "id": "amd-002",
                "title": "Finance Act 2025 - Minimum Tax Changes",
                "description": "Minimum tax carry forward provision introduced",
                "affected_sections": ["163", "70"],
                "priority": "high",
                "effective_date": date(2025, 7, 1),
                "created_at": datetime.now()
            },
            {
                "id": "amd-003",
                "title": "SRO 404-Law/2025 - Authentic English Text",
                "description": "Official authentic English text of ITA 2023 published",
                "affected_sections": ["All"],
                "priority": "normal",
                "effective_date": date(2025, 10, 8),
                "created_at": datetime.now()
            }
        ]
    }
