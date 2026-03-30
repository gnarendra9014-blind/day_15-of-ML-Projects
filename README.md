# Day 15: Self-Healing Data Pipeline Agent 🤖✨

A robust, AI-powered data engineering pipeline that automatically diagnoses and fixes data validation errors. Using **LLMs (Llama 3.3 70B via Groq)**, the agent identifies why a pipeline run failed and generates fixes to ensure data integrity without manual intervention.

---

## 🚀 Overview
Traditional data pipelines often break when they encounter unexpected data formats, missing values, or schema changes. This project implements a **Self-Healing Loop**:
1. **Fetch**: Ingests raw data.
2. **Validate**: Checks data against predefined quality rules.
3. **Diagnose**: If validation fails, an AI Agent analyzes the errors.
4. **Fix**: The AI generates specific cleaning/transformation logic to resolve the issues.
5. **Retry**: The pipeline automatically retries with the new fixes applied.

## ✨ Key Features
- **AI-Driven Error Resolution**: Uses Llama 3.3 to understand complex data quality issues.
- **Automatic Retry Logic**: Up to 3 attempts with cumulative fixes.
- **SQL Database Integration**: Tracks every pipeline run, error, and successful transformation.
- **Groq Acceleration**: High-speed inference for near-instant diagnosis.

## 🛠️ Architecture
- `app.py`: Main controller managing the pipeline lifecycle.
- `healer.py`: The "Brain" - interfaces with Groq to diagnose and generate fixes.
- `pipeline.py`: Core logic for fetching, cleaning, and transforming data.
- `database.py`: Persistent storage for run history and clean results.

## 📦 Getting Started

### 1. Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/gnarendra9014-blind/day_15-of-ML-Projects.git
cd day_15-of-ML-Projects

# Set up a virtual environment
python -m venv venv
source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Pipeline
```bash
python app.py
```

## 📊 Run Tracking
Successful runs and error logs are stored in `pipeline.db`. You can query the `pipeline_runs` table to see the AI's diagnosis history and successful fixes.

---
Built as part of the **25 Days of ML Projects** challenge. 🚀