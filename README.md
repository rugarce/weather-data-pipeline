# Weather Data Pipeline

End-to-end data engineering pipeline that collects hourly weather data from the Open-Meteo API, validates and transforms it, and stores it in PostgreSQL.

The project is designed as a portfolio project to demonstrate practical data engineering skills including API ingestion, data validation, relational data modeling, Docker, testing, idempotent pipelines, and CI.

## Architecture

```text
Open-Meteo API
      │
      ▼
Python API Client
      │
      ▼
Raw JSON
      │
      ▼
Transformation & Validation
      │
      ▼
PostgreSQL
      │
      ├── locations
      ├── raw_weather
      └── weather_observations
```

## Features

- Hourly weather data ingestion from Open-Meteo
- Five European cities:
  - Madrid
  - Paris
  - London
  - Berlin
  - Rome
- Raw API responses stored as JSONB
- Normalized weather observations stored in PostgreSQL
- Data validation before database insertion
- Foreign key and unique constraints
- Idempotent data ingestion
- Dockerized PostgreSQL database
- Automated tests with pytest
- Continuous Integration with GitHub Actions

## Tech Stack

- Python 3.12+
- PostgreSQL 16
- Docker / Docker Compose
- Requests
- Psycopg 3
- pytest
- GitHub Actions

## Project Structure

```text
weather-data-pipeline/
│
├── src/
│   ├── api_client.py
│   ├── config.py
│   ├── database.py
│   └── pipeline.py
│
├── tests/
│   ├── test_api_client.py
│   └── test_pipeline.py
│
├── sql/
│   └── 001_create_tables.sql
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Data Model

The PostgreSQL database contains three main tables.

### locations

Stores the configured cities and their coordinates.

```text
locations
├── id
├── city
├── country
├── latitude
├── longitude
└── created_at
```

### raw_weather

Stores the original API response as JSONB.

```text
raw_weather
├── id
├── location_id
├── retrieved_at
└── payload
```

### weather_observations

Stores normalized hourly weather observations.

```text
weather_observations
├── id
├── location_id
├── observed_at
├── temperature_c
├── humidity_pct
├── precipitation_mm
├── wind_speed_kmh
└── ingested_at
```

Each observation is uniquely identified by:

```text
(location_id, observed_at)
```

This constraint provides database-level protection against duplicate observations.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd weather-data-pipeline
```

### 2. Create the environment file

Copy `.env.example` to `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

On Linux/macOS:

```bash
cp .env.example .env
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

Check the container:

```bash
docker ps
```

### 4. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Pipeline

Run:

```bash
python -m src.pipeline
```

The pipeline:

1. Requests weather data from Open-Meteo.
2. Stores the raw API response.
3. Transforms hourly data into normalized observations.
4. Validates the observations.
5. Inserts the observations into PostgreSQL.
6. Prevents duplicate observations using the database unique constraint.

## Testing

Run the complete test suite:

```bash
python -m pytest
```

The project currently includes tests for:

- Weather data transformation
- Data validation
- Invalid weather values
- Successful API responses
- API timeout handling

Tests are also executed automatically through GitHub Actions on pushes and pull requests.

## Idempotency

The pipeline is designed to be safely executed multiple times.

Weather observations use:

```sql
UNIQUE (location_id, observed_at)
```

and inserts use:

```sql
ON CONFLICT (location_id, observed_at)
DO NOTHING
```

This means running the pipeline repeatedly does not create duplicate observations.

## Data Engineering Concepts Demonstrated

This project demonstrates:

- REST API ingestion
- Raw data preservation
- ETL / ELT concepts
- Data validation
- Relational database modeling
- JSONB storage
- Primary and foreign keys
- Unique constraints
- Idempotent pipelines
- Docker
- Automated testing
- CI/CD fundamentals
- Git and GitHub workflow

## Future Improvements

Possible next steps:

- Add structured logging
- Add retry logic with exponential backoff
- Parameterize the API timezone
- Add historical weather ingestion
- Add data quality metrics
- Add scheduled execution
- Add analytical SQL queries
- Add a dashboard using Power BI or another BI tool
- Deploy the pipeline to a cloud environment

## Project Status

Completed:

- [x] Repository and Docker setup
- [x] PostgreSQL data model
- [x] Open-Meteo API ingestion
- [x] Data transformation
- [x] Data validation
- [x] Idempotent pipeline
- [x] Automated tests
- [x] GitHub Actions CI
- [x] Documentation