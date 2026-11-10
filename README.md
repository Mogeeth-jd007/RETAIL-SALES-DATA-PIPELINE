\# Retail Sales ETL Pipeline



A Python-based, configuration-driven ETL pipeline that extracts CSV datasets, transforms and validates records, classifies data quality, and loads eligible records into SQLite databases.



\## Project Overview



This project demonstrates an end-to-end ETL workflow using three datasets:



\- Retail sales

\- Employees

\- Students



Each dataset has its own configuration profile, validation rules, output files, and SQLite database.



\## Technology Stack



\- Python

\- Pandas

\- SQLite

\- SQL

\- Pytest

\- Git and GitHub



\## Project Structure



```text

retail-sales-data-pipeline/

├── dashboard/

├── data/

│   ├── raw/

│   ├── processed/

│   ├── rejected/

│   └── \*.db

├── logs/

├── sql/

│   ├── retail\_sales\_analysis.sql

│   ├── employee\_analysis.sql

│   └── student\_analysis.sql

├── src/

│   ├── extract.py

│   ├── transform.py

│   ├── validate.py

│   ├── load.py

│   ├── config.py

│   ├── logger.py

│   ├── main.py

│   └── verify.py

├── tests/

├── config.json

├── requirements.txt

└── README.md

```



\## ETL Workflow



1\. Extract data from CSV files.

2\. Standardize column names and clean text.

3\. Detect numeric data types and convert configured dates.

4\. Calculate total sales where applicable.

5\. Validate records using dataset-specific rules.

6\. Classify records as VALID, WARNING, or REJECTED.

7\. Save validation results into separate CSV files.

8\. Load VALID and WARNING records into SQLite.

9\. Perform SQL analytics on the loaded datasets.



\## Data Quality Classification



| Status | Description |

|---|---|

| VALID | Records pass all configured checks |

| WARNING | Records contain non-critical missing values |

| REJECTED | Records contain critical data-quality issues |



\## Supported Datasets



| Dataset | Database | Table |

|---|---|---|

| Retail | retail\_sales.db | retail\_sales |

| Employee | employee\_data.db | employees |

| Student | student\_data.db | students |



\## Running the Pipeline



Activate the virtual environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Run the retail pipeline:



```powershell

python src/main.py --dataset retail

```



Run the employee pipeline:



```powershell

python src/main.py --dataset employee

```



Run the student pipeline:



```powershell

python src/main.py --dataset student

```



\## SQL Analytics



Three SQL scripts provide analytical queries.



\### Retail Sales

\- Total sales revenue

\- Total orders

\- Product-wise revenue

\- Category-wise revenue

\- Monthly sales

\- Top customers

\- Average order value



\### Employee

\- Total employees

\- Average salary

\- Department-wise employee count

\- Top five highest-paid employees



\### Student

\- Total students

\- Average marks

\- Course-wise student count

\- Top five students by marks



\## Automated Testing



The project uses Pytest for unit and integration testing.



Run all tests:



```powershell

$env:PYTHONPATH = "src"

pytest -v

```



The latest verified test suite contains 16 passing tests.



\## Logging



Centralized logging records pipeline execution, extraction, transformation, validation, classification, and database loading activities in the `logs/` directory.



\## Skills Demonstrated



\- Python programming

\- Data extraction and transformation

\- Data quality validation

\- Configuration-driven development

\- SQLite database operations

\- SQL analytical queries

\- Unit and integration testing

\- Git version control



\## Future Improvements



\- Dashboard integration

\- Advanced SQL analytics

\- Cloud data warehouse integration

\- Apache Airflow orchestration

\- Automated pipeline scheduling



