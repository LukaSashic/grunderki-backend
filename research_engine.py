# research_engine.py
"""
Real-Time Research Engine
Conducts parallel web research and synthesizes findings with Claude
"""

import asyncio
import json
import os
import hashlib
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from anthropic import Anthropic

anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ResearchEngine:
    """
    Manages real-time research for business intelligence
    """
    
    # Research triggers based on keywords
    RESEARCH_TRIGGERS = {
        "business_idea": {
            "keywords": ["consulting", "beratung", "shop", "store", "restaurant", "service"],
            "priority": "high",
            "queries": ["market_size", "competitors", "trends"]
        },
        "location": {
            "keywords": ["berlin", "münchen", "hamburg", "köln"],
            "priority": "medium",
            "queries": ["local_market", "local_competitors"]
        },
        "target_customer": {
            "keywords": ["restaurants", "hotels", "einzelhandel", "kmu", "startups"],
            "priority": "medium",
            "queries": ["customer_segment", "pain_points"]
        }
    }
    
    SYNTHESIS_PROMPT = """You are a business analyst synthesizing market research for a founder.

RESEARCH QUERY: {query}
BUSINESS CONTEXT: {business_context}

SEARCH RESULTS:
{search_results}

YOUR TASK:
Synthesize the search results into a concise, actionable insight for the founder.

OUTPUT FORMAT (JSON only):
{{
  "insight_type": "market_size|competitors|trends|funding|pricing",
  "headline": "One sentence key finding",
  "details": {{
    "key_metric": "Main number/fact",
    "context": "What this means for the founder",
    "sources": ["source1", "source2"]
  }},
  "confidence": 0-100,
  "actionable_takeaway": "What the founder should do with this info"
}}

RULES:
- Be specific and data-driven
- Include actual numbers when available
- Cite sources
- Keep it concise (2-3 key points max)
- Make it actionable
- Output ONLY valid JSON, no markdown"""

    def __init__(self, web_search_func, web_fetch_func=None):
        """
        Initialize with web search function from FastAPI
        
        Args:
            web_search_func: Async function that performs web search
            web_fetch_func: Optional async function that fetches web pages
        """
        self.web_search = web_search_func
        self.web_fetch = web_fetch_func
        self.client = anthropic_client
        self.cache = {}  # Simple in-memory cache (use Redis in production)
    
    async def analyze_and_research(
        self,
        user_message: str,
        business_context: Dict,
        conversation_history: List[Dict]
    ) -> Optional[Dict]:
        """
        Analyze message for research triggers and conduct research if needed
        
        Args:
            user_message: Latest user message
            business_context: Extracted business context
            conversation_history: Full conversation
            
        Returns:
            Research insights or None if no research needed
        """
        
        # Check if message triggers research
        triggers = self._identify_triggers(user_message, business_context)
        
        if not triggers:
            return None
        
        # Execute research (max 5 seconds timeout)
        try:
            research_results = await asyncio.wait_for(
                self._execute_research(triggers, business_context),
                timeout=5.0
            )
            return research_results
            
        except asyncio.TimeoutError:
            print("Research timeout - continuing without insights")
            return None
        except Exception as e:
            print(f"Research error: {e}")
            return None
    
    def _identify_triggers(self, message: str, context: Dict) -> List[str]:
        """Identify what type of research to trigger based on message"""
        
        triggers = []
        message_lower = message.lower()
        
        # Check for business idea mention
        if any(kw in message_lower for kw in self.RESEARCH_TRIGGERS["business_idea"]["keywords"]):
            if not context.get("researched_market"):
                triggers.append("market_analysis")
        
        # Check for location mention
        if any(kw in message_lower for kw in self.RESEARCH_TRIGGERS["location"]["keywords"]):
            if not context.get("researched_location"):
                triggers.append("local_market")
        
        # Check for target customer mention
        if any(kw in message_lower for kw in self.RESEARCH_TRIGGERS["target_customer"]["keywords"]):
            if not context.get("researched_customers"):
                triggers.append("customer_analysis")
        
        return triggers
    
    async def _execute_research(
        self,
        triggers: List[str],
        business_context: Dict
    ) -> Dict:
        """
        Execute research queries in parallel
        """
        
        research_plan = self._create_research_plan(triggers, business_context)
        
        # Execute searches in parallel (max 3 to stay within rate limits)
        tasks = []
        for query_info in research_plan[:3]:
            cache_key = self._get_cache_key(query_info["query"])
            
            # Check cache first
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if cached["expires_at"] > datetime.utcnow():
                    continue  # Use cached result
            
            # Execute search
            tasks.append(self._search_and_cache(query_info, cache_key))
        
        # Wait for all searches
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_results = [r for r in search_results if not isinstance(r, Exception)]
        
        if not valid_results:
            return None
        
        # Synthesize findings with Claude
        synthesis = await self._synthesize_findings(valid_results, business_context)
        
        return synthesis
    
    def _create_research_plan(
        self,
        triggers: List[str],
        context: Dict
    ) -> List[Dict]:
        """Create specific search queries based on triggers and context"""
        
        plan = []
        
        # Extract business details
        what = context.get("what", "business")
        who = context.get("who", "customers")
        location = self._extract_location(context)
        
        if "market_analysis" in triggers:
            plan.append({
                "type": "market_size",
                "query": f"{what} market size {location} 2024",
                "intent": "Find market size and potential"
            })
            plan.append({
                "type": "competitors",
                "query": f"{what} companies {location}",
                "intent": "Identify main competitors"
            })
            plan.append({
                "type": "trends",
                "query": f"{what} trends Germany 2024",
                "intent": "Understand market trends"
            })
        
        if "local_market" in triggers:
            plan.append({
                "type": "local_opportunities",
                "query": f"{what} {location} opportunities",
                "intent": "Local market opportunities"
            })
        
        if "customer_analysis" in triggers:
            plan.append({
                "type": "customer_needs",
                "query": f"{who} {what} problems Germany",
                "intent": "Customer pain points"
            })
        
        return plan
    
    def _extract_location(self, context: Dict) -> str:
        """Extract location from context, default to Germany"""
        
        # Check various context fields for location
        for field in ["who", "what", "problem"]:
            value = context.get(field, "").lower()
            if "berlin" in value:
                return "Berlin"
            elif "münchen" in value or "munich" in value:
                return "München"
            elif "hamburg" in value:
                return "Hamburg"
        
        return "Germany"
    
    async def _search_and_cache(
        self,
        query_info: Dict,
        cache_key: str
    ) -> Dict:
        """Execute search and cache result"""
        
        try:
            # Call web search
            results = await self.web_search(query_info["query"])
            
            # Cache result (24 hour expiry)
            cached_result = {
                "query": query_info["query"],
                "type": query_info["type"],
                "results": results,
                "expires_at": datetime.utcnow() + timedelta(hours=24),
                "cached_at": datetime.utcnow()
            }
            
            self.cache[cache_key] = cached_result
            
            return cached_result
            
        except Exception as e:
            print(f"Search error for {query_info['query']}: {e}")
            return {
                "query": query_info["query"],
                "error": str(e)
            }
    
    async def _synthesize_findings(
        self,
        search_results: List[Dict],
        business_context: Dict
    ) -> Dict:
        """Use Claude to synthesize research findings into actionable insights"""
        
        try:
            # Prepare search results for Claude
            formatted_results = []
            for result in search_results:
                if "error" in result:
                    continue
                    
                formatted_results.append({
                    "query": result["query"],
                    "type": result["type"],
                    "findings": result.get("results", [])[:3]  # Top 3 results only
                })
            
            if not formatted_results:
                return None
            
            # Call Claude to synthesize
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                temperature=0.5,
                system=self.SYNTHESIS_PROMPT.format(
                    query=formatted_results[0]["query"],
                    business_context=json.dumps(business_context, ensure_ascii=False),
                    search_results=json.dumps(formatted_results, indent=2, ensure_ascii=False)
                ),
                messages=[{
                    "role": "user",
                    "content": "Synthesize these research findings into actionable insights."
                }]
            )
            
            # Parse response
            response_text = response.content[0].text.strip()
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            synthesis = json.loads(response_text)
            synthesis["raw_results"] = formatted_results  # Include raw data
            synthesis["timestamp"] = datetime.utcnow().isoformat()
            
            return synthesis
            
        except Exception as e:
            print(f"Synthesis error: {e}")
            return None
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key from query"""
        return hashlib.md5(query.lower().encode()).hexdigest()
    
    async def get_competitor_insights(
        self,
        competitor_names: List[str],
        business_context: Dict
    ) -> List[Dict]:
        """
        Deep dive into specific competitors
        Used in detailed interview phase
        """
        
        insights = []
        
        for competitor in competitor_names[:3]:  # Max 3 competitors
            try:
                # Search for competitor
                query = f"{competitor} reviews services pricing"
                results = await self.web_search(query)
                
                # If web_fetch is available, fetch their website
                if self.web_fetch and results:
                    # Try to find their website in results
                    for result in results[:2]:
                        try:
                            website_content = await self.web_fetch(result.get("url", ""))
                            # Store for later analysis
                            results.append({"website_content": website_content})
                        except:
                            pass
                
                insights.append({
                    "competitor": competitor,
                    "research": results
                })
                
            except Exception as e:
                print(f"Error researching competitor {competitor}: {e}")
                continue
        
        return insights
