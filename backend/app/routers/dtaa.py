"""
JIAPI - DTAA Router
Double Taxation Avoidance Agreements
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.schemas import DTAAResponse, DTAABase
from app.core.security import get_current_user

router = APIRouter()


@router.get("/dtaas", response_model=List[DTAAResponse])
async def list_dtaas(
    country: Optional[str] = Query(None),
    status: Optional[str] = Query("active"),
    current_user: dict = Depends(get_current_user)
):
    """
    List all Double Taxation Avoidance Agreements.

    Bangladesh has approximately 35 active treaties.
    """
    dtaas = [
        {"id": "dtaa-uk", "country_name": "United Kingdom", "country_code": "GBR", "treaty_name": "Agreement for Avoidance of Double Taxation with UK", "signed_date": date(1980, 8, 8), "effective_date": date(1980, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 7.5, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-usa", "country_name": "United States", "country_code": "USA", "treaty_name": "Convention with USA", "signed_date": date(2004, 9, 26), "effective_date": date(2006, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-india", "country_name": "India", "country_code": "IND", "treaty_name": "Agreement with India", "signed_date": date(1991, 7, 10), "effective_date": date(1992, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-canada", "country_name": "Canada", "country_code": "CAN", "treaty_name": "Agreement with Canada", "signed_date": date(1982, 10, 15), "effective_date": date(1983, 1, 1), "status": "active", "withholding_rates": {"dividend": 15, "interest": 15, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-singapore", "country_name": "Singapore", "country_code": "SGP", "treaty_name": "Agreement with Singapore", "signed_date": date(2004, 12, 9), "effective_date": date(2005, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-malaysia", "country_name": "Malaysia", "country_code": "MYS", "treaty_name": "Agreement with Malaysia", "signed_date": date(1998, 12, 22), "effective_date": date(1999, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-thailand", "country_name": "Thailand", "country_code": "THA", "treaty_name": "Agreement with Thailand", "signed_date": date(2005, 11, 10), "effective_date": date(2006, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-sri-lanka", "country_name": "Sri Lanka", "country_code": "LKA", "treaty_name": "Agreement with Sri Lanka", "signed_date": date(1983, 3, 22), "effective_date": date(1984, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-pakistan", "country_name": "Pakistan", "country_code": "PAK", "treaty_name": "Agreement with Pakistan", "signed_date": date(1989, 12, 20), "effective_date": date(1990, 1, 1), "status": "active", "withholding_rates": {"dividend": 15, "interest": 15, "royalty": 15}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-saudi", "country_name": "Saudi Arabia", "country_code": "SAU", "treaty_name": "Agreement with Saudi Arabia", "signed_date": date(2017, 3, 28), "effective_date": date(2018, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 7.5, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-uae", "country_name": "United Arab Emirates", "country_code": "ARE", "treaty_name": "Agreement with UAE", "signed_date": date(2011, 1, 17), "effective_date": date(2012, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-korea", "country_name": "South Korea", "country_code": "KOR", "treaty_name": "Agreement with Korea", "signed_date": date(1983, 5, 10), "effective_date": date(1984, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-japan", "country_name": "Japan", "country_code": "JPN", "treaty_name": "Agreement with Japan", "signed_date": date(1991, 11, 10), "effective_date": date(1992, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-china", "country_name": "China", "country_code": "CHN", "treaty_name": "Agreement with China", "signed_date": date(1996, 9, 4), "effective_date": date(1997, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
        {"id": "dtaa-turkey", "country_name": "Turkey", "country_code": "TUR", "treaty_name": "Agreement with Turkey", "signed_date": date(2011, 6, 22), "effective_date": date(2012, 1, 1), "status": "active", "withholding_rates": {"dividend": 10, "interest": 10, "royalty": 10}, "relief_method": "credit", "is_comprehensive": True},
    ]

    if country:
        dtaas = [d for d in dtaas if country.lower() in d["country_name"].lower()]

    return dtaas


@router.get("/dtaas/{country_code}", response_model=DTAAResponse)
async def get_dtaa(
    country_code: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific DTAA with full articles"""
    return {
        "id": f"dtaa-{country_code.lower()}",
        "country_name": "United Kingdom",
        "country_code": country_code.upper(),
        "treaty_name": "Agreement for Avoidance of Double Taxation",
        "effective_date": date(1980, 1, 1),
        "status": "active",
        "withholding_rates": {"dividend": 10, "interest": 7.5, "royalty": 10},
        "relief_method": "credit",
        "articles": [
            {"article": 1, "title": "Persons Covered", "text": "This Agreement shall apply to persons who are residents of one or both of the Contracting States."},
            {"article": 2, "title": "Taxes Covered", "text": "This Agreement shall apply to taxes on income and on capital gains."},
            {"article": 4, "title": "Resident", "text": "For the purposes of this Agreement, the term 'resident of a Contracting State' means any person who, under the laws of that State, is liable to tax therein."},
            {"article": 5, "title": "Permanent Establishment", "text": "For the purposes of this Agreement, the term 'permanent establishment' means a fixed place of business through which the business of an enterprise is wholly or partly carried on."},
            {"article": 6, "title": "Income from Immovable Property", "text": "Income derived by a resident of a Contracting State from immovable property situated in the other Contracting State may be taxed in that other State."},
            {"article": 7, "title": "Business Profits", "text": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment."},
            {"article": 9, "title": "Associated Enterprises", "text": "Where conditions are made or imposed between associated enterprises which differ from those which would be made between independent enterprises, profits may be included in the profits of the enterprise and taxed accordingly."},
            {"article": 10, "title": "Dividends", "text": "Dividends paid by a company which is a resident of a Contracting State to a resident of the other Contracting State may be taxed in that other State."},
            {"article": 11, "title": "Interest", "text": "Interest arising in a Contracting State and paid to a resident of the other Contracting State may be taxed in that other State."},
            {"article": 12, "title": "Royalties", "text": "Royalties arising in a Contracting State and paid to a resident of the other Contracting State may be taxed in that other State."},
            {"article": 13, "title": "Capital Gains", "text": "Gains derived by a resident of a Contracting State from the alienation of immovable property situated in the other Contracting State may be taxed in that other State."},
            {"article": 23, "title": "Elimination of Double Taxation", "text": "Double taxation shall be eliminated by allowing a credit against the tax of the residence State."},
        ],
        "is_comprehensive": True,
        "created_at": "1980-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }


@router.get("/dtaas/{country_code}/withholding-rates")
async def get_withholding_rates(
    country_code: str,
    current_user: dict = Depends(get_current_user)
):
    """Get withholding tax rates for specific DTAA"""
    return {
        "country": country_code,
        "dividend": 10,
        "interest": 7.5,
        "royalty": 10,
        "technical_services": 7.5,
        "capital_gains": "Taxable in source country"
    }
