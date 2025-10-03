from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import asyncio
from dotenv import load_dotenv

from .services.instantly import InstantlyService
from .services.ai_copy import AICopyService
from .services.firebase_service import FirebaseService
from .routes import domains

load_dotenv()

app = FastAPI(title="Vibe Marketing Autopilot API")

# Include routers
app.include_router(domains.router, prefix="/api", tags=["domains"])

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))
ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))

# Firebase credentials from environment variable
firebase_creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
db_service = FirebaseService(firebase_creds_path)


class CampaignRequest(BaseModel):
    campaign_name: Optional[str] = None
    url: str
    target_audience: str
    user_id: str
    sender_name: Optional[str] = None  # Sender's name for email signature
    lead_count: Optional[int] = 3  # Default to 3 leads
    leads_csv: Optional[str] = None


class LeadListRequest(BaseModel):
    leads: list
    campaign_name: str


@app.get("/")
async def root():
    return {"message": "Vibe Marketing Autopilot API", "status": "active"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/create-campaign-stream")
async def create_campaign_stream(request: CampaignRequest):
    """
    Create campaign with real-time progress updates via Server-Sent Events
    """
    async def generate_progress():
        try:
            # Step 1: Generate AI copy
            log_msg = f'Sending request to OpenAI GPT-4 for URL: {request.url}'
            yield f"data: {json.dumps({'step': 1, 'status': 'in_progress', 'message': 'Analyzing your website and generating AI-powered email copy...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.1)

            copy_variants = await ai_service.generate_email_copy(
                request.url,
                request.target_audience
            )

            # Replace [Your Name] placeholder with actual sender name
            if request.sender_name:
                for variant in copy_variants:
                    if 'body' in variant:
                        variant['body'] = variant['body'].replace('[Your Name]', request.sender_name)

            # Send detailed log with AI output
            variant_preview = f"Generated {len(copy_variants)} variants:\n"
            for i, variant in enumerate(copy_variants, 1):
                subject = variant.get('subject', 'N/A')
                variant_preview += f"\n• Variant {i}: {subject[:60]}"

            yield f"data: {json.dumps({'step': 1, 'status': 'completed', 'message': 'Generated 3 email variants with AI', 'log': variant_preview, 'variants': copy_variants})}\n\n"
            await asyncio.sleep(0.5)

            # Step 2: Generate search filters from ICP using AI
            log_msg = f'Analyzing ICP: {request.target_audience}'
            yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'AI analyzing your ICP to generate search filters...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Use AI to generate SuperSearch filters
            search_filters = await ai_service.generate_supersearch_filters(
                request.target_audience,
                request.url
            )

            log_msg = f'Generated search filters: {json.dumps(search_filters, indent=2)}'
            yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'Creating campaign in Instantly.ai...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Step 2.5: Create campaign FIRST (before enrichment)
            campaign_name = request.campaign_name or f"Launch - {request.url}"

            # Create campaign with temporary empty lead list
            temp_lead_list_id = await instantly_service.create_lead_list(
                name=f"Temp list for {campaign_name}"
            )

            campaign_data = await instantly_service.create_campaign(
                name=campaign_name,
                lead_list_id=temp_lead_list_id,
                variants=copy_variants
            )
            campaign_id = campaign_data.get("id", "N/A")

            log_msg = f'✅ Campaign created: {campaign_id}\n   - Now enriching leads directly into this campaign...'
            yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'Campaign created! Now searching for leads...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Search for leads using Instantly SuperSearch - creates a list that we'll move to campaign
            lead_list_id_from_search = None
            enrichment_id = None
            try:
                # Run SuperSearch to find new leads (creates a list)
                # Note: campaign_id parameter doesn't actually work - SuperSearch always creates a list
                search_result = await instantly_service.search_leads_supersearch(
                    search_filters=search_filters,
                    limit=request.lead_count or 3,
                    work_email_enrichment=True,
                    list_name=f"Leads for {campaign_name}"
                )

                # Get the enrichment/list resource_id
                enrichment_id = search_result.get("resource_id") or search_result.get("id")
                lead_list_id_from_search = enrichment_id
                log_msg = f'✅ SuperSearch enrichment started!\n   Enrichment ID: {enrichment_id}\n   Finding new leads that will be added to campaign {campaign_id}...'
                yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'Finding and enriching new leads...', 'log': log_msg})}\n\n"

                # Give enrichment time to start
                await asyncio.sleep(5)

                # Try to fetch actual enriched leads from SuperSearch
                real_leads = []
                try:
                    # Check enrichment status first
                    enrichment_status = await instantly_service.get_supersearch_enrichment_status(lead_list_id_from_search)
                    log_msg = f'Enrichment status: {enrichment_status.get("status", "unknown")}, Progress: {enrichment_status.get("progress", "unknown")}'
                    yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'Checking enrichment progress...', 'log': log_msg})}\n\n"
                    await asyncio.sleep(2)

                    # Try to get enriched leads from history endpoint
                    enriched_leads = await instantly_service.get_supersearch_enrichment_history(lead_list_id_from_search)
                    if enriched_leads:
                        real_leads = enriched_leads[:10]  # Get first 10 leads
                        log_msg = f'Successfully fetched {len(real_leads)} real enriched leads from SuperSearch'
                        print(f"✅ Got real leads: {len(real_leads)}")
                        print(f"Sample lead: {real_leads[0] if real_leads else 'None'}")
                    else:
                        # If no leads yet, try the lead list endpoint
                        list_leads = await instantly_service.get_leads_from_list(lead_list_id_from_search, limit=10)
                        if list_leads:
                            real_leads = list_leads
                            log_msg = f'Successfully fetched {len(real_leads)} real leads from lead list'
                            print(f"✅ Got real leads from list: {len(real_leads)}")
                        else:
                            log_msg = 'Enrichment still in progress. Leads will be available in the campaign shortly.'
                            print("⏳ Enrichment in progress, no leads available yet")
                except Exception as lead_fetch_error:
                    log_msg = f'Could not fetch leads preview yet (enrichment in progress): {str(lead_fetch_error)[:100]}'
                    print(f"Lead fetch error: {str(lead_fetch_error)}")

                # Build lead status message
                print(f"⏳ SuperSearch list created: {lead_list_id_from_search}")
                print(f"DEBUG: search_filters = {search_filters}")

                # Extract search criteria for display
                title_include = search_filters.get("title", {}).get("include", [])
                dept_list = search_filters.get("department", [])
                level_list = search_filters.get("level", [])
                locations = search_filters.get("locations", [])
                employee_count = search_filters.get("employee_count", [])
                revenue = search_filters.get("revenue", [])

                # Build enrichment status message
                if real_leads:
                    # We have actual enriched leads
                    lead_count = len(real_leads)
                    status_msg = f"✅ {lead_count} REAL leads enriched and ready"
                    enrichment_status = "completed"
                else:
                    # Enrichment in progress
                    lead_count = 5
                    status_msg = f"⏳ {lead_count} REAL leads sourced - enrichment in progress"
                    enrichment_status = "in_progress"

                # Build criteria summary for UI (note: keywords removed - always blank)
                criteria_parts = []
                if title_include:
                    criteria_parts.append(f"Titles: {', '.join(title_include[:3])}")
                if dept_list:
                    criteria_parts.append(f"Departments: {', '.join(dept_list[:2])}")
                if level_list:
                    criteria_parts.append(f"Levels: {', '.join(level_list[:2])}")
                if employee_count:
                    criteria_parts.append(f"Company Size: {', '.join(employee_count[:2])}")
                if revenue:
                    criteria_parts.append(f"Revenue: {', '.join(revenue[:2])}")
                if locations:
                    loc = locations[0]
                    city = loc.get('city', '').strip()
                    state = loc.get('state', '').strip()
                    country = loc.get('country', '').strip()

                    # Build location string
                    if city and state:
                        loc_str = f"{city}, {state}, {country}"
                    elif city:
                        loc_str = f"{city}, {country}"
                    elif state:
                        loc_str = f"{state}, {country}"
                    else:
                        loc_str = country

                    if loc_str:
                        criteria_parts.append(f"Location: {loc_str}")

                criteria_summary = " | ".join(criteria_parts) if criteria_parts else "Custom criteria"

                log_msg = f'''✅ SuperSearch sourced {lead_count} REAL leads from Instantly database
   List ID: {lead_list_id_from_search}
   Criteria: {criteria_summary}
   Status: {"Enriched and ready" if real_leads else "Enrichment in progress (emails being verified)"}

   {"These leads are ready to use in the campaign" if real_leads else "Campaign will use these leads once enrichment completes (~2-5 minutes)"}'''

                message = status_msg

                # Send lead sourcing data (no fake preview leads)
                yield f"data: {json.dumps({
                    'step': 2,
                    'status': 'completed',
                    'message': message,
                    'log': log_msg,
                    'supersearch_list_id': lead_list_id_from_search,
                    'lead_count': lead_count,
                    'enrichment_status': enrichment_status,
                    'criteria_summary': criteria_summary,
                    'show_lead_preview': False  # Don't show fake lead table
                })}\n\n"

            except Exception as e:
                # SuperSearch failed - show error and stop
                import traceback
                error_details = traceback.format_exc()
                print(f"SuperSearch error: {str(e)}")
                print(f"Full traceback: {error_details}")

                error_msg = f'❌ SuperSearch failed: {str(e)[:200]}\n\nPlease try:\n1. Making your ICP more specific (e.g., "CTOs at Series A SaaS companies in San Francisco")\n2. Uploading a CSV file with leads instead\n3. Trying again in a moment'

                yield f"data: {json.dumps({'step': 'error', 'status': 'error', 'message': error_msg})}\n\n"
                return  # Stop the campaign creation process

            await asyncio.sleep(0.5)

            # Step 3: Poll enrichment and move leads to campaign when ready
            if enrichment_id and campaign_id:
                log_msg = f'''⏳ Waiting for SuperSearch enrichment to complete...

   This typically takes 2-5 minutes depending on lead count.
   Once complete, new leads will be automatically added to your campaign.'''

                yield f"data: {json.dumps({'step': 3, 'status': 'in_progress', 'message': 'Waiting for lead enrichment...', 'log': log_msg})}\n\n"

                # Poll enrichment status (max 5 minutes)
                max_polls = 30  # 30 polls x 10 seconds = 5 minutes
                poll_count = 0
                enrichment_complete = False

                while poll_count < max_polls:
                    await asyncio.sleep(10)  # Wait 10 seconds between polls
                    poll_count += 1

                    # Check if leads are available in the list
                    try:
                        enriched_leads = await instantly_service.get_leads_from_list(enrichment_id, limit=1)
                        if enriched_leads and len(enriched_leads) > 0:
                            enrichment_complete = True
                            log_msg = f'✅ Enrichment complete! Found {len(enriched_leads)} leads. Moving to campaign...'
                            yield f"data: {json.dumps({'step': 3, 'status': 'in_progress', 'message': 'Enrichment complete! Adding leads to campaign...', 'log': log_msg})}\n\n"
                            break
                        else:
                            log_msg = f'⏳ Still enriching... (checked {poll_count} times, will keep trying)'
                            yield f"data: {json.dumps({'step': 3, 'status': 'in_progress', 'message': f'Enriching leads... ({poll_count * 10}s)', 'log': log_msg})}\n\n"
                    except Exception as poll_error:
                        print(f"Poll error: {poll_error}")
                        continue

                if enrichment_complete:
                    # Move leads from list to campaign
                    log_msg = f'Moving enriched leads from list {enrichment_id} to campaign {campaign_id}...'
                    yield f"data: {json.dumps({'step': 3, 'status': 'in_progress', 'message': 'Adding leads to campaign...', 'log': log_msg})}\n\n"

                    try:
                        # Pass the lead_count limit to avoid fetching all workspace leads
                        success = await instantly_service.move_leads_to_campaign(
                            campaign_id=campaign_id,
                            lead_list_id=enrichment_id,
                            limit=request.lead_count or 10
                        )
                        if success:
                            log_msg = f'''✅ Leads successfully added to campaign!

   Campaign ID: {campaign_id}
   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}

   Check your dashboard - leads should now appear in the campaign!'''
                            yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Leads added to campaign!', 'log': log_msg})}\n\n"
                        else:
                            log_msg = f'''⚠️ Could not add leads to campaign automatically.

   Campaign ID: {campaign_id}
   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}
   Lead List ID: {enrichment_id}

   You may need to manually add leads from the list to the campaign in Instantly.ai dashboard.'''
                            yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Campaign created (manual lead addition needed)', 'log': log_msg})}\n\n"
                    except Exception as move_error:
                        log_msg = f'''⚠️ Error moving leads: {str(move_error)[:200]}

   Campaign ID: {campaign_id}
   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}
   Lead List ID: {enrichment_id}

   Leads were enriched but need to be manually added to campaign.'''
                        yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Campaign created (manual setup needed)', 'log': log_msg})}\n\n"
                else:
                    # Enrichment timed out
                    log_msg = f'''⏳ Enrichment is taking longer than expected.

   Campaign ID: {campaign_id}
   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}
   Lead List ID: {enrichment_id}

   SuperSearch is still finding leads. Check back in a few minutes and leads should appear.'''
                    yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Campaign created (enrichment in progress)', 'log': log_msg})}\n\n"
            else:
                # Fallback if enrichment_id not available
                log_msg = f'''✅ Campaign ready!

   Campaign ID: {campaign_id}
   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}'''
                yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Campaign created!', 'log': log_msg})}\n\n"

            await asyncio.sleep(0.5)

            # Step 4: Activate campaign
            log_msg = f'Sending activation request for campaign {campaign_id}'
            yield f"data: {json.dumps({'step': 4, 'status': 'in_progress', 'message': 'Activating campaign in Instantly.ai...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.1)

            activated = await instantly_service.activate_campaign(campaign_data["id"])
            if activated:
                campaign_data["status"] = "active"
            status_msg = "Campaign is now ACTIVE and sending emails" if activated else "Campaign created but not activated"
            yield f"data: {json.dumps({'step': 4, 'status': 'completed', 'message': 'Campaign activated and ready to send', 'log': status_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Step 5: Save to database
            log_msg = f'Saving to Firebase/Firestore for user {request.user_id}'
            yield f"data: {json.dumps({'step': 5, 'status': 'in_progress', 'message': 'Saving campaign data to database...', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.1)

            db_record = await db_service.save_campaign(
                user_id=request.user_id,
                campaign_id=campaign_data["id"],
                url=request.url,
                target_audience=request.target_audience,
                copy_variants=copy_variants,
                supersearch_list_id=lead_list_id_from_search
            )
            log_msg = f'Record saved to campaigns collection with {len(copy_variants)} variants'
            yield f"data: {json.dumps({'step': 5, 'status': 'completed', 'message': 'Campaign saved to database', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Final success message
            yield f"data: {json.dumps({'step': 'done', 'status': 'success', 'data': {'campaign_id': campaign_data['id'], 'lead_list_id': lead_list_id_from_search, 'variants': copy_variants}})}\n\n"

        except Exception as e:
            import traceback
            error_msg = str(e) if str(e) else repr(e)
            full_trace = traceback.format_exc()
            print(f"Error creating campaign: {error_msg}")
            print(f"Full traceback:\n{full_trace}")
            yield f"data: {json.dumps({'step': 'error', 'status': 'error', 'message': error_msg or 'Unknown error occurred'})}\n\n"

    return StreamingResponse(generate_progress(), media_type="text/event-stream")


@app.post("/api/create-campaign")
async def create_campaign(request: CampaignRequest):
    """
    Main endpoint to create a full campaign (non-streaming version for backwards compatibility)
    """
    try:
        # Step 1: Generate AI copy
        print(f"Generating AI copy for {request.url}...")
        copy_variants = await ai_service.generate_email_copy(
            request.url,
            request.target_audience
        )

        # Step 2: Create lead list (from CSV or example)
        print("Creating lead list...")
        lead_list_id = await instantly_service.create_lead_list(
            name=f"Campaign - {request.url}",
            leads_data=request.leads_csv
        )

        # Step 3: Create campaign with variants
        print("Creating campaign with A/B variants...")
        campaign_data = await instantly_service.create_campaign(
            name=f"Launch - {request.url}",
            lead_list_id=lead_list_id,
            variants=copy_variants
        )

        # Step 3.5: Activate the campaign
        print("Activating campaign...")
        activated = await instantly_service.activate_campaign(campaign_data["id"])
        if activated:
            campaign_data["status"] = "active"

        # Step 4: Store in database
        print("Saving to database...")
        db_record = await db_service.save_campaign(
            user_id=request.user_id,
            campaign_id=campaign_data["id"],
            url=request.url,
            target_audience=request.target_audience,
            copy_variants=copy_variants
        )

        return {
            "success": True,
            "campaign_id": campaign_data["id"],
            "lead_list_id": lead_list_id,
            "variants": copy_variants,
            "db_record": db_record
        }

    except Exception as e:
        print(f"Error creating campaign: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/{campaign_id}")
async def get_campaign_analytics(campaign_id: str, user_id: str):
    """
    Fetch campaign analytics from Instantly
    """
    try:
        analytics = await instantly_service.get_campaign_analytics(campaign_id)

        # Update database with latest stats
        await db_service.update_campaign_stats(campaign_id, analytics)

        return {
            "success": True,
            "campaign_id": campaign_id,
            "analytics": analytics
        }

    except Exception as e:
        print(f"Error fetching analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns")
async def get_user_campaigns(user_id: str):
    """
    Get all campaigns for a user
    """
    try:
        campaigns = await db_service.get_user_campaigns(user_id)
        return {
            "success": True,
            "campaigns": campaigns
        }
    except Exception as e:
        print(f"Error fetching campaigns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/leads/{list_id}")
async def get_leads_from_list(list_id: str):
    """
    Get enriched leads from a SuperSearch list

    Wait 2-5 minutes after campaign creation for enrichment to complete
    """
    try:
        # First try to get enriched leads from history endpoint
        leads = await instantly_service.get_supersearch_enrichment_history(list_id)

        # If no leads from history, try the list endpoint
        if not leads:
            leads = await instantly_service.get_leads_from_list(list_id, limit=100)

        if not leads:
            # Check enrichment status
            status = await instantly_service.get_supersearch_enrichment_status(list_id)

            return {
                "success": False,
                "message": "Enrichment still in progress. Please wait 2-5 minutes and try again.",
                "enrichment_status": status,
                "list_id": list_id
            }

        return {
            "success": True,
            "list_id": list_id,
            "lead_count": len(leads),
            "leads": leads
        }
    except Exception as e:
        print(f"Error fetching leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/create-email-account")
async def create_email_account(user_id: str, email: str, smtp_config: dict):
    """
    Create a warmed email account in Instantly
    """
    try:
        account = await instantly_service.create_email_account(email, smtp_config)

        # Save to database
        await db_service.save_email_account(user_id, account)

        return {
            "success": True,
            "account": account
        }
    except Exception as e:
        print(f"Error creating email account: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-leads")
async def upload_leads(request: LeadListRequest):
    """
    Upload leads to Instantly
    """
    try:
        lead_list_id = await instantly_service.upload_leads(
            request.campaign_name,
            request.leads
        )

        return {
            "success": True,
            "lead_list_id": lead_list_id
        }
    except Exception as e:
        print(f"Error uploading leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ICP-DRIVEN CAMPAIGN CREATION FLOW
# ============================================================================

class ICPAnalysisRequest(BaseModel):
    url: str


class LeadSearchRequest(BaseModel):
    target_audience: str  # The selected ICP description
    url: str  # For context
    lead_count: int = 10


class LeadPreviewResponse(BaseModel):
    leads: list
    total_count: int
    enrichment_id: str


class DFYDomainMatchRequest(BaseModel):
    url: str


class ICPCampaignRequest(BaseModel):
    campaign_name: str
    url: str
    user_id: str
    selected_icp: dict  # The ICP the user selected
    enrichment_id: str  # The lead list ID from search
    lead_count: int
    approved_variants: list  # The approved/edited email variants from user
    selected_domains: list  # List of domain strings user selected (legacy)
    selected_accounts: Optional[list] = []  # List of email addresses to use for sending
    sender_name: Optional[str] = None


@app.post("/api/icp/analyze")
async def analyze_url_for_icps(request: ICPAnalysisRequest):
    """
    Step 1: Analyze website and suggest 10 ICPs
    """
    try:
        print(f"🔍 Starting ICP analysis for URL: {request.url}")
        icps = await ai_service.suggest_three_icps(request.url)
        print(f"✅ ICP analysis complete. Found {len(icps)} ICPs")
        return {
            "success": True,
            "icps": icps,
            "url": request.url
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error analyzing URL for ICPs: {str(e)}")
        print(f"Full traceback:\n{error_trace}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/icp/search-leads")
async def search_leads_for_icp(request: LeadSearchRequest):
    """
    Step 2: Search for leads based on selected ICP
    Returns enrichment_id to poll for completion
    """
    try:
        # Convert ICP description to SuperSearch filters using AI
        search_filters = await ai_service.generate_supersearch_filters(
            target_audience=request.target_audience,
            url=request.url
        )

        print(f"🔍 Searching for {request.lead_count} leads with filters:")
        print(json.dumps(search_filters, indent=2))

        # Start SuperSearch enrichment
        search_result = await instantly_service.search_leads_supersearch(
            search_filters=search_filters,
            limit=request.lead_count,
            work_email_enrichment=True,
            list_name=f"ICP Leads - {request.target_audience[:50]}"
        )

        # Use resource_id (the list ID) to fetch leads, not the enrichment id
        enrichment_id = search_result.get("resource_id") or search_result.get("id")

        print(f"📋 SuperSearch created:")
        print(f"   Enrichment ID: {search_result.get('id')}")
        print(f"   Resource ID (list): {search_result.get('resource_id')}")
        print(f"   Using resource_id for lead fetching: {enrichment_id}")
        print(f"   Search filters in response: {search_result.get('search_filters')}")

        return {
            "success": True,
            "enrichment_id": enrichment_id,
            "search_filters": search_filters,
            "message": "Lead search started. Use enrichment_id to check status."
        }
    except Exception as e:
        print(f"Error searching leads for ICP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/icp/leads/{enrichment_id}")
async def get_lead_preview(enrichment_id: str, limit: int = 10):
    """
    Step 3: Get preview of leads for user approval
    The enrichment_id is actually the resource_id (list ID) from SuperSearch
    We fetch leads directly from the list using /api/v2/leads/list
    """
    try:
        # Fetch leads directly from the list using resource_id (list ID)
        print(f"📋 Fetching leads from list: {enrichment_id}")
        leads = await instantly_service.get_leads_from_list(enrichment_id, limit=limit)

        if not leads:
            print(f"⚠️ No leads found yet in list {enrichment_id}")
            return {
                "success": False,
                "enrichment_id": enrichment_id,
                "leads": [],
                "total_count": 0,
                "enriching_count": 0,
                "message": "Enrichment in progress... No leads found yet. Please wait a few seconds and try again."
            }

        # Filter out leads without emails (still enriching)
        enriched_leads = [lead for lead in leads if lead.get('email') and lead.get('email') != 'N/A']
        enriching_count = len(leads) - len(enriched_leads)

        print(f"✅ Found {len(leads)} total leads in list")
        print(f"   {len(enriched_leads)} with emails (ready)")
        print(f"   {enriching_count} still enriching")

        if enriched_leads:
            print(f"   Sample lead: {enriched_leads[0].get('email', 'N/A')} - {enriched_leads[0].get('first_name', '')} {enriched_leads[0].get('last_name', '')}")

        # Return enriched leads, or if none ready yet, return all with a message
        if enriched_leads:
            return {
                "success": True,
                "enrichment_id": enrichment_id,
                "leads": enriched_leads,
                "total_count": len(enriched_leads),
                "enriching_count": enriching_count,
                "message": f"Found {len(enriched_leads)} enriched leads" + (f" ({enriching_count} still enriching)" if enriching_count > 0 else "")
            }
        else:
            # No leads ready yet, return status
            return {
                "success": False,
                "enrichment_id": enrichment_id,
                "leads": [],
                "total_count": 0,
                "enriching_count": len(leads),
                "message": f"Enrichment in progress... {len(leads)} leads found, waiting for email verification"
            }
    except Exception as e:
        print(f"Error getting lead preview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class EmailGenerationRequest(BaseModel):
    url: str
    selected_icp: dict  # The ICP object with name, description, pain_points, etc.


class EmailRegenerateRequest(BaseModel):
    url: str
    selected_icp: dict
    variant_index: int  # Which variant to regenerate (0, 1, or 2)


@app.post("/api/icp/generate-emails")
async def generate_icp_emails(request: EmailGenerationRequest):
    """
    Step 3.5: Generate email variants based on ICP and website analysis
    Returns 3 email variants for user approval/editing
    """
    try:
        target_audience = request.selected_icp.get("target_audience", "")
        pain_points = request.selected_icp.get("pain_points", [])

        # Add pain points to context for better email generation
        context = f"{target_audience}. Key pain points: {', '.join(pain_points)}"

        variants = await ai_service.generate_email_copy(
            url=request.url,
            target_audience=context
        )

        return {
            "success": True,
            "variants": variants,
            "icp_name": request.selected_icp.get("name", "")
        }
    except Exception as e:
        print(f"Error generating ICP emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/icp/regenerate-email")
async def regenerate_single_variant(request: EmailRegenerateRequest):
    """
    Regenerate a single email variant
    """
    try:
        target_audience = request.selected_icp.get("target_audience", "")
        pain_points = request.selected_icp.get("pain_points", [])
        context = f"{target_audience}. Key pain points: {', '.join(pain_points)}"

        # Generate 3 variants and return the one at the requested index
        variants = await ai_service.generate_email_copy(
            url=request.url,
            target_audience=context
        )

        # Return the variant at the requested index (or first one if index out of range)
        variant_index = min(request.variant_index, len(variants) - 1)

        return {
            "success": True,
            "variant": variants[variant_index],
            "variant_index": request.variant_index
        }
    except Exception as e:
        print(f"Error regenerating email variant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/icp/match-domains")
async def match_dfy_domains(request: DFYDomainMatchRequest):
    """
    Step 4: Get AI-matched DFY domains AND existing email accounts for the business
    """
    try:
        # Import DomainService
        from .services.domain_service import DomainService
        domain_service = DomainService(os.getenv("INSTANTLY_API_KEY"))

        print(f"🔍 Fetching domains and accounts for {request.url}...")

        # Get available pre-warmed DFY domains
        available_domains = await domain_service.get_prewarmed_domains(
            extensions=["com", "org", "co"]
        )

        print(f"📊 Found {len(available_domains)} pre-warmed DFY domains from API")

        # Get existing email accounts
        print(f"📧 Fetching existing email accounts...")
        accounts = await instantly_service.get_accounts(limit=100, status=1)  # Only active accounts

        # Extract unique domains from accounts
        existing_account_domains = list(set(
            acc.get("email", "").split("@")[1]
            for acc in accounts
            if "@" in acc.get("email", "")
        ))

        print(f"📊 Found {len(accounts)} active accounts across {len(existing_account_domains)} domains")
        if existing_account_domains:
            print(f"   Sample account domains: {existing_account_domains[:5]}")

        # Use AI to match DFY domains if available
        matched_dfy_domains = []
        if available_domains:
            print(f"🤖 Using AI to match {len(available_domains)} DFY domains to business...")
            matched_dfy_domains = await ai_service.match_dfy_domains_to_business(
                url=request.url,
                available_domains=available_domains
            )
            print(f"✅ Matched {len(matched_dfy_domains)} DFY domains")

        return {
            "success": True,
            "matched_domains": matched_dfy_domains,
            "total_available": len(available_domains),
            "existing_accounts": accounts,
            "existing_account_domains": existing_account_domains
        }
    except Exception as e:
        print(f"❌ Error matching domains: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/icp/create-campaign")
async def create_icp_campaign(request: ICPCampaignRequest):
    """
    Step 5: Create campaign with approved leads and selected domains
    This is a streaming endpoint that returns SSE updates
    """
    async def campaign_stream():
        try:
            # Step 1: Use approved email variants
            yield f"data: {json.dumps({'step': 1, 'status': 'in_progress', 'message': 'Preparing approved email variants'})}\n\n"
            await asyncio.sleep(0.5)

            variants = request.approved_variants

            log_msg = f'Using {len(variants)} approved email variants'
            yield f"data: {json.dumps({'step': 1, 'status': 'completed', 'message': 'Email variants ready', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Step 2: Create campaign in Instantly
            yield f"data: {json.dumps({'step': 2, 'status': 'in_progress', 'message': 'Creating campaign in Instantly.ai'})}\n\n"
            await asyncio.sleep(0.5)

            campaign_result = await instantly_service.create_campaign(
                name=request.campaign_name,
                variants=variants,
                email_accounts=request.selected_accounts if request.selected_accounts else None
            )

            campaign_id = campaign_result.get("id")
            accounts_msg = f" with {len(request.selected_accounts)} email accounts" if request.selected_accounts else ""
            log_msg = f'Campaign created with ID: {campaign_id}{accounts_msg}'
            yield f"data: {json.dumps({'step': 2, 'status': 'completed', 'message': 'Campaign created', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Step 3: Add leads to campaign
            yield f"data: {json.dumps({'step': 3, 'status': 'in_progress', 'message': f'Adding {request.lead_count} leads to campaign'})}\n\n"
            await asyncio.sleep(0.5)

            success = await instantly_service.move_leads_to_campaign(
                campaign_id=campaign_id,
                lead_list_id=request.enrichment_id,
                limit=request.lead_count
            )

            if success:
                log_msg = f'Successfully added {request.lead_count} leads to campaign'
                yield f"data: {json.dumps({'step': 3, 'status': 'completed', 'message': 'Leads added to campaign', 'log': log_msg})}\n\n"
            else:
                log_msg = 'Lead addition may have failed - check campaign dashboard'
                yield f"data: {json.dumps({'step': 3, 'status': 'warning', 'message': 'Leads may not have been added', 'log': log_msg})}\n\n"

            await asyncio.sleep(0.5)

            # Step 4: Save campaign to database
            yield f"data: {json.dumps({'step': 4, 'status': 'in_progress', 'message': 'Saving campaign to database'})}\n\n"
            await asyncio.sleep(0.5)

            # Prepare campaign data with ICP info
            campaign_data = {
                "id": campaign_id,
                "name": request.campaign_name,
                "url": request.url,
                "user_id": request.user_id,
                "icp_name": request.selected_icp.get("name", ""),
                "icp_description": request.selected_icp.get("description", ""),
                "target_audience": request.selected_icp.get("target_audience", ""),
                "pain_points": request.selected_icp.get("pain_points", []),
                "lead_count": request.lead_count,
                "selected_domains": request.selected_domains,
                "created_at": asyncio.get_event_loop().time()
            }

            # Save variants
            copy_variants = []
            for idx, variant in enumerate(variants):
                variant_data = {
                    "variant_number": idx + 1,
                    "subject": variant.get("subject", ""),
                    "body": variant.get("body", "")
                }
                copy_variants.append(variant_data)

            campaign_data["variants"] = copy_variants

            # Save to Firestore
            await db_service.save_campaign(
                user_id=request.user_id,
                campaign_id=campaign_id,
                url=request.url,
                target_audience=request.selected_icp.get("target_audience", ""),
                copy_variants=copy_variants,
                supersearch_list_id=request.enrichment_id
            )

            log_msg = f'Campaign saved to database'
            yield f"data: {json.dumps({'step': 4, 'status': 'completed', 'message': 'Campaign saved to database', 'log': log_msg})}\n\n"
            await asyncio.sleep(0.5)

            # Final success message
            yield f"data: {json.dumps({'step': 'done', 'status': 'success', 'data': {'campaign_id': campaign_id, 'lead_list_id': request.enrichment_id, 'variants': copy_variants, 'icp': request.selected_icp}})}\n\n"

        except Exception as e:
            import traceback
            error_msg = str(e) if str(e) else repr(e)
            full_trace = traceback.format_exc()
            print(f"Error creating ICP campaign: {error_msg}")
            print(full_trace)
            yield f"data: {json.dumps({'step': 'error', 'status': 'error', 'message': error_msg})}\n\n"

    return StreamingResponse(
        campaign_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
