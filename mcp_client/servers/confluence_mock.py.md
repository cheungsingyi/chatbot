# mcp_client/servers/confluence_mock.py

```python
#!/usr/bin/env python3
from fastmcp import FastMCP

MOCK_CONFLUENCE_DATA = {
    "Engineering": {
        "API Rate Limits": {
            "id": "eng-001",
            "content": """# API Rate Limits
            
## Current Limits
- REST API: 100 requests/minute per IP
- GraphQL API: 500 requests/minute per IP
- Webhooks: 1000 events/minute

## Authentication
All API requests require Bearer token authentication.

## Monitoring
Use our internal monitoring dashboard at /metrics/api
"""
        },
        "Architecture Overview": {
            "id": "eng-002",
            "content": """# System Architecture

## Microservices
1. Auth Service (Port 8001)
2. User Service (Port 8002)
3. Analytics Service (Port 8003)

## Databases
- PostgreSQL: Primary datastore
- Redis: Caching and sessions
- Elasticsearch: Search functionality

## Message Queue
RabbitMQ for async processing
"""
        },
        "Deployment Runbook": {
            "id": "eng-003",
            "content": """# Deployment Runbook

## Prerequisites
- Kubernetes cluster access
- AWS credentials configured
- Docker images built

## Steps
1. Run integration tests: `npm run test:integration`
2. Build Docker image: `docker build -t app:latest .`
3. Push to ECR: `aws ecr push app:latest`
4. Update k8s manifests
5. Apply: `kubectl apply -f deployment.yaml`

## Rollback
`kubectl rollout undo deployment/app`
"""
        }
    },
    "Product": {
        "Q4 2024 Roadmap": {
            "id": "prod-001",
            "content": """# Q4 2024 Product Roadmap

## Key Features
1. Multi-factor Authentication (Priority: High)
2. Advanced Analytics Dashboard (Priority: High)
3. Mobile App v2.0 (Priority: Medium)
4. API v3 Migration (Priority: Low)

## Revenue Targets
- Q4 Target: $450,000
- Q3 Actual: $380,000
- Growth Target: 18.4%

## Team Allocation
- Engineering: 12 people
- Design: 3 people
- Product: 2 people
"""
        },
        "Feature: User Analytics": {
            "id": "prod-002",
            "content": """# User Analytics Feature

## Overview
Real-time user behavior tracking and visualization.

## User Stories
- As a PM, I want to see user engagement metrics
- As a marketer, I want to track conversion funnels
- As an engineer, I want to monitor performance

## Technical Requirements
- Sub-second query response time
- Support 100K concurrent users
- 99.9% uptime SLA

## Launch Date
Planned: December 15, 2024
"""
        }
    },
    "HR": {
        "Employee Benefits": {
            "id": "hr-001",
            "content": """# Employee Benefits 2024

## Health Insurance
- Medical: 100% employer paid
- Dental: 80% employer paid
- Vision: 50% employer paid

## Retirement
- 401(k) matching: 6%
- Vesting schedule: Immediate

## Time Off
- Vacation: 20 days/year
- Sick leave: 10 days/year
- Parental leave: 16 weeks

## Professional Development
- Conference budget: $2,000/year
- Training courses: Unlimited (with approval)
"""
        },
        "Team Structure": {
            "id": "hr-002",
            "content": """# Company Team Structure

## Engineering (15 people)
- Backend: 8 engineers
- Frontend: 5 engineers
- DevOps: 2 engineers

## Product (5 people)
- Product Managers: 3
- Designers: 2

## Operations (10 people)
- Sales: 6
- Customer Success: 4

## Average Team Size: 10 people
## Total Headcount: 30
"""
        }
    },
    "Finance": {
        "Q4 2024 Revenue": {
            "id": "fin-001",
            "content": """# Q4 2024 Financial Report

## Revenue Breakdown
- Subscription Revenue: $320,000
- Enterprise Contracts: $100,000
- Professional Services: $30,000
- **Total: $450,000**

## Expenses
- Personnel: $280,000
- Infrastructure: $50,000
- Marketing: $40,000
- **Total: $370,000**

## Net Income: $80,000
## Profit Margin: 17.8%

## Previous Quarter (Q3 2024)
- Revenue: $380,000
- Growth: +18.4% QoQ
"""
        }
    }
}

mcp = FastMCP("confluence-mock")

@mcp.tool()
def search_confluence(query: str, space: str = "") -> str:
    """Search for information in the internal Confluence knowledge base. Returns relevant page excerpts based on the query.
    
    Args:
        query: Search query to find relevant pages
        space: Confluence space to search in (Engineering, Product, HR, Finance). Leave empty to search all spaces.
    """
    query_lower = query.lower()
    results = []
    spaces_to_search = [space] if space else MOCK_CONFLUENCE_DATA.keys()
    
    for search_space in spaces_to_search:
        if search_space not in MOCK_CONFLUENCE_DATA:
            continue
            
        for page_title, page_data in MOCK_CONFLUENCE_DATA[search_space].items():
            if query_lower in page_title.lower() or query_lower in page_data["content"].lower():
                preview = page_data["content"][:200].strip()
                results.append(
                    f"**[{search_space}] {page_title}** (ID: {page_data['id']})\n{preview}..."
                )
    
    if not results:
        return f"No results found for query: '{query}'"
    
    return f"Found {len(results)} result(s):\n\n" + "\n\n---\n\n".join(results)

@mcp.tool()
def get_confluence_page(page_id: str) -> str:
    """Retrieve the full content of a specific Confluence page by its page ID.
    
    Args:
        page_id: The unique ID of the Confluence page (e.g., 'eng-001', 'prod-002')
    """
    for space, pages in MOCK_CONFLUENCE_DATA.items():
        for page_title, page_data in pages.items():
            if page_data["id"] == page_id:
                return f"**[{space}] {page_title}**\n\n{page_data['content']}"
    
    return f"Page not found: {page_id}"

@mcp.tool()
def list_confluence_spaces() -> str:
    """List all available Confluence spaces and their descriptions."""
    spaces_info = []
    for space, pages in MOCK_CONFLUENCE_DATA.items():
        page_count = len(pages)
        page_titles = ", ".join(list(pages.keys())[:3])
        spaces_info.append(
            f"**{space}** ({page_count} pages)\n  Pages: {page_titles}..."
        )
    
    return "Available Confluence Spaces:\n\n" + "\n\n".join(spaces_info)

if __name__ == "__main__":
    mcp.run()
```
