import json
import os
import requests

# 1. Load Config
COMPANY_ID = os.environ.get('RECRUITEE_COMPANY_ID')
API_TOKEN = os.environ.get('RECRUITEE_API_TOKEN')
BASE_URL = f"https://api.recruitee.com/c/{COMPANY_ID}"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def _response(status, body):
    """Helper to return standard API Gateway response"""
    return {
        "statusCode": status,
        "body": json.dumps(body)
    }

# --- 1. GET /jobs ---
def get_jobs(event, context):
    try:
        # Recruitee calls jobs "offers"
        url = f"{BASE_URL}/offers"
        r = requests.get(url, headers=HEADERS)
        
        if r.status_code != 200:
            return _response(r.status_code, {"error": "Failed to fetch jobs from Recruitee"})

        data = r.json().get('offers', [])
        
        # Standardize the output as per Task Requirement
        standardized_jobs = []
        for offer in data:
            standardized_jobs.append({
                "id": str(offer.get('id')),
                "title": offer.get('title'),
                "location": offer.get('location', 'Remote'),
                "status": offer.get('status', 'OPEN').upper(), # Recruitee returns 'published', 'internal', etc.
                "external_url": offer.get('careers_url')
            })

        return _response(200, standardized_jobs)

    except Exception as e:
        return _response(500, {"error": str(e)})

# --- 2. POST /candidates ---
def create_candidate(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        if not body.get('name') or not body.get('email'):
            return _response(400, {"error": "Name and Email are required"})

        # Recruitee payload structure
        recruitee_payload = {
            "candidate": {
                "name": body.get('name'),
                "emails": [body.get('email')],
                "phones": [body.get('phone')] if body.get('phone') else [],
                "links": [body.get('resume_url')] if body.get('resume_url') else []
            }
        }

        # If job_id is present, we attach the candidate to that offer
        job_id = body.get('job_id')
        if job_id:
            recruitee_payload["offers"] = [int(job_id)]

        url = f"{BASE_URL}/candidates"
        r = requests.post(url, headers=HEADERS, json=recruitee_payload)

        if r.status_code in [200, 201]:
            new_candidate = r.json().get('candidate', {})
            return _response(201, {
                "message": "Candidate created successfully",
                "id": new_candidate.get('id'),
                "recruitee_id": new_candidate.get('id')
            })
        else:
            return _response(r.status_code, {"error": r.text})

    except Exception as e:
        return _response(500, {"error": str(e)})

# --- 3. GET /applications?job_id=... ---
def get_applications(event, context):
    try:
        # Get query parameters
        params = event.get('queryStringParameters') or {}
        job_id = params.get('job_id')

        if not job_id:
            return _response(400, {"error": "Missing job_id parameter"})

        # Recruitee Endpoint: Get candidates for a specific offer
        url = f"{BASE_URL}/offers/{job_id}/candidates"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            return _response(r.status_code, {"error": "Could not fetch applications"})

        candidates = r.json().get('candidates', [])
        
        results = []
        for cand in candidates:
            # Map Recruitee status to our standard status
            # Recruitee uses 'placements' to track status per job
            results.append({
                "id": str(cand.get('id')),
                "candidate_name": cand.get('name'),
                "email": cand.get('emails')[0] if cand.get('emails') else "",
                "status": "APPLIED" # Simplifying status mapping for MVP
            })

        return _response(200, results)

    except Exception as e:
        return _response(500, {"error": str(e)})