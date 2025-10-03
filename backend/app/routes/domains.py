"""
API routes for domain and email account management
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
from ..services.domain_service import DomainService

router = APIRouter()


def get_domain_service():
    """Dependency to get domain service instance"""
    return DomainService(os.getenv("INSTANTLY_API_KEY"))


class DomainSearchRequest(BaseModel):
    extensions: Optional[List[str]] = ["com", "org", "co"]
    search: Optional[str] = None


class CheckDomainsRequest(BaseModel):
    domains: List[str]


class SimilarDomainsRequest(BaseModel):
    domain: str
    tlds: Optional[List[str]] = ["com", "org"]


class AccountInfo(BaseModel):
    first_name: str
    last_name: str
    email_address_prefix: str


class OrderPrewarmedRequest(BaseModel):
    domain: str
    number_of_accounts: int = 1
    forwarding_domain: Optional[str] = None
    simulation: bool = False


class OrderCustomDomainRequest(BaseModel):
    domain: str
    accounts: List[AccountInfo]
    forwarding_domain: Optional[str] = None
    simulation: bool = False


class CancelAccountsRequest(BaseModel):
    account_emails: List[str]


@router.post("/domains/prewarmed")
async def get_prewarmed_domains(
    request: DomainSearchRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Get list of available pre-warmed domains
    """
    try:
        domains = await domain_service.get_prewarmed_domains(
            extensions=request.extensions,
            search=request.search
        )
        return {
            "success": True,
            "domains": domains,
            "count": len(domains)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/domains/check")
async def check_domains(
    request: CheckDomainsRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Check availability of domains
    """
    try:
        availability = await domain_service.check_domain_availability(request.domains)
        return {
            "success": True,
            "results": availability
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/domains/similar")
async def get_similar_domains(
    request: SimilarDomainsRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Generate similar available domains
    """
    try:
        domains = await domain_service.generate_similar_domains(
            domain=request.domain,
            tlds=request.tlds
        )
        return {
            "success": True,
            "domains": domains,
            "count": len(domains)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/domains/order/prewarmed")
async def order_prewarmed_domain(
    request: OrderPrewarmedRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Order pre-warmed email accounts
    """
    try:
        result = await domain_service.order_prewarmed_accounts(
            domain=request.domain,
            number_of_accounts=request.number_of_accounts,
            forwarding_domain=request.forwarding_domain,
            simulation=request.simulation
        )
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/domains/order/custom")
async def order_custom_domain(
    request: OrderCustomDomainRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Order DFY email accounts with custom domain
    """
    try:
        # Convert Pydantic models to dicts
        accounts_data = [account.dict() for account in request.accounts]

        result = await domain_service.order_custom_domain_accounts(
            domain=request.domain,
            accounts=accounts_data,
            forwarding_domain=request.forwarding_domain,
            simulation=request.simulation
        )
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domains/accounts")
async def list_accounts(
    limit: int = 10,
    starting_after: Optional[str] = None,
    with_passwords: bool = False,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    List all ordered email accounts
    """
    try:
        result = await domain_service.list_ordered_accounts(
            limit=limit,
            starting_after=starting_after,
            with_passwords=with_passwords
        )
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domains/orders")
async def list_orders(
    limit: int = 10,
    starting_after: Optional[str] = None,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    List all domain orders
    """
    try:
        result = await domain_service.list_domain_orders(
            limit=limit,
            starting_after=starting_after
        )
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/domains/accounts/cancel")
async def cancel_accounts(
    request: CancelAccountsRequest,
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Cancel email accounts
    """
    try:
        result = await domain_service.cancel_accounts(request.account_emails)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
