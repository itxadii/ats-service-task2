# ATS Integration Microservice (Recruitee Adapter)

![Serverless](https://img.shields.io/badge/Serverless-Framework-fd5750?style=for-the-badge&logo=serverless)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?style=for-the-badge&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)

A serverless microservice built with **Python** and the **Serverless Framework** that acts as a unified API adapter for **Recruitee ATS**.

This service allows you to fetch jobs, create candidates, and list applications using a standardized JSON format, decoupling your frontend from specific ATS implementation details.

---

## Features

* **GET /jobs**: Fetches open jobs from Recruitee and returns them in a standardized schema.
* **POST /candidates**: Creates a new candidate in Recruitee and optionally attaches them to a specific job.
* **GET /applications**: Lists all candidates applied to a specific job.
* **Local Development**: Fully testable locally using `serverless-offline`.

---

## Prerequisites

* **Node.js** (for Serverless Framework)
* **Python 3.9+** (for logic)
* **AWS CLI** (configured with credentials, though not strictly needed for local offline mode)

---

## Setup Guide

### 1. Clone & Install

```bash
# Install Node dependencies (Serverless plugins)
npm install

# Install Python dependencies (requests)
pip install -r requirements.txt
```

### 2. Configure ATS Credentials (Recruitee)

You need a Recruitee account to run this service.

1. **Create Free Trial**: Go to Recruitee.com and sign up for an 18-day free trial.
2. **Get Company ID**:
   * Log in to Recruitee.
   * Look at your browser URL: `https://app.recruitee.com/c/12345/...`
   * The number `12345` is your Company ID.
3. **Generate API Token**:
   * Go to Settings (gear icon) > Apps & plugins.
   * Click Personal API tokens.
   * Click + New token, name it "DevOps Task", and copy the string.

### 3. Environment Variables

Create a `.env` file in the root directory:

```
RECRUITEE_COMPANY_ID=your_company_id_here
RECRUITEE_API_TOKEN=your_api_token_here
```

---

## 🚀 How to Run Locally

We use `serverless-offline` to emulate AWS Lambda and API Gateway on your local machine.

```bash
npx serverless offline
```

You should see:

```
Offline [http for lambda] listening on http://localhost:3000
```

---

## 📡 API Documentation & Examples

### 1. Get All Jobs

Returns a standardized list of open positions.

**Request:**

```bash
curl http://localhost:3000/dev/jobs
```

**Response:**

```json
[
  {
    "id": "12345",
    "title": "Senior DevOps Engineer",
    "location": "Remote",
    "status": "OPEN",
    "external_url": "https://..."
  }
]
```

### 2. Create a Candidate

Adds a candidate to the ATS. You can optionally link them to a job by providing `job_id`.

**Request:**

```bash
curl -X POST http://localhost:3000/dev/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "job_id": "12345"
  }'
```

**Response:**

```json
{
  "message": "Candidate created successfully",
  "id": "998877",
  "recruitee_id": 998877
}
```

### 3. Get Applications for a Job

Lists all candidates who have applied for a specific Job ID.

**Request:**

```bash
curl "http://localhost:3000/dev/applications?job_id=12345"
```

**Response:**

```json
[
  {
    "id": "998877",
    "candidate_name": "John Doe",
    "email": "john@example.com",
    "status": "APPLIED"
  }
]
```

---

## Project Structure

```
ats-service/
├── handler.py           # Core business logic & ATS adapters
├── serverless.yml       # AWS Infrastructure definition
├── requirements.txt     # Python dependencies
├── .env                 # Local secrets (ignored by git)
└── package.json         # Node.js dependencies (plugins)
```

---

## 📜 License

This project is part of a technical assessment and is available for review purposes.
