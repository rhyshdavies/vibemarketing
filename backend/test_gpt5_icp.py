#!/usr/bin/env python3
"""
Test gpt-5 web search for ICP analysis
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()

async def test_gpt5_icp():
    api_key = os.getenv("OPENAI_API_KEY")
    url = "ofi.co.uk"
    
    prompt = f"""Search the web for information about {url} and analyze their business.

Based on your research, suggest 3 HIGHLY SPECIFIC Ideal Customer Profiles (ICPs) that would be perfect buyers for this company's products/services.

IMPORTANT: Base your ICPs ONLY on what this specific company actually does. Do not give generic suggestions.

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "name": "ICP Name Here",
    "description": "Who they are and why they would buy from this company",
    "target_audience": "Specific job titles at specific company types",
    "pain_points": ["First pain point", "Second pain point", "Third pain point"],
    "company_size": "startup or mid-market or enterprise"
  }}
]"""

    async with httpx.AsyncClient(timeout=300.0) as client:
        print(f"🔍 Testing gpt-5 web search for {url}...")
        print(f"⏱️  This may take 30-60 seconds...\n")
        
        try:
            response = await client.post(
                "https://api.openai.com/v1/responses",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-5",
                    "reasoning": {"effort": "low"},
                    "tools": [{"type": "web_search"}],
                    "input": prompt
                }
            )
            
            print(f"✅ Response received (status {response.status_code})\n")
            
            if response.status_code != 200:
                print(f"❌ Error: {response.text}")
                return
            
            result = response.json()
            
            # Extract text from response
            output_text = None
            for item in result.get("output", []):
                if item.get("type") == "message":
                    content = item.get("content", [])
                    if content and content[0].get("type") == "output_text":
                        output_text = content[0].get("text")
                        break
            
            if output_text:
                print("📄 Response text:")
                print("-" * 80)
                print(output_text[:500])
                print("-" * 80)
                
                # Try to parse JSON
                try:
                    cleaned = output_text.strip()
                    if "```json" in cleaned:
                        start = cleaned.find("```json") + 7
                        end = cleaned.find("```", start)
                        cleaned = cleaned[start:end].strip()
                    elif "```" in cleaned:
                        start = cleaned.find("```") + 3
                        end = cleaned.find("```", start)
                        cleaned = cleaned[start:end].strip()
                    
                    if "[" in cleaned and "]" in cleaned:
                        json_start = cleaned.find("[")
                        json_end = cleaned.rfind("]") + 1
                        cleaned = cleaned[json_start:json_end]
                    
                    icps = json.loads(cleaned)
                    print(f"\n✅ Successfully parsed {len(icps)} ICPs:")
                    for i, icp in enumerate(icps, 1):
                        print(f"\n{i}. {icp.get('name')}")
                        print(f"   {icp.get('description')}")
                        
                except Exception as e:
                    print(f"\n⚠️ Could not parse as JSON: {e}")
            else:
                print("❌ No output text found")
                print(f"Response structure: {list(result.keys())}")
                
        except asyncio.TimeoutError:
            print("❌ Request timed out after 300 seconds")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(test_gpt5_icp())
