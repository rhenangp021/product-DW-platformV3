# ProductDataPlatform_v3

An end-to-end data engineering project demonstrating data ingestion, transformation, dimensional modeling, ETL orchestration, and analytical reporting.

The solution uses Python, Microsoft SQL Server, SQL Server Integration Services (SSIS), and Power BI, following the Medallion Architecture.

## Project Overview

The project extracts product data from the DummyJSON API, stores the original JSON payload in SQL Server, transforms the data into structured relational tables, and builds a dimensional model for historical and analytical reporting.

The pipeline is organized into three layers:

- **Bronze:** Raw data ingestion.
- **Silver:** Data transformation and cleansing.
- **Gold:** Dimensional modeling and analytical datasets.

ETL execution monitoring and data quality constraints are also implemented.

## Architecture

```text
              DummyJSON Products API
                       |
                       v
                Python Extraction
                       |
                       v
                JSON File Output
                       |
                       v
              Python Bronze Loader
                       |
                       v
               SQL Server - Bronze
                 products_raw
                       |
                       v
                  SSIS Package
                       |
                       v
               SQL Server - Silver
                +--------------+
                |   products   |
                | product_reviews
                +--------------+
                       |
                       v
               SQL Server - Gold
                +--------------+
                | dim_product  |
                | dim_date     |
                |              |
                | fact_product |
                | _snapshot    |
                +--------------+
                       |
                       v
                Analytical Views
                       |
                       v
                    Power BI
```

## Technologies

| Technology | Purpose |
|---|---|
| Python | API extraction and Bronze ingestion |
| Microsoft SQL Server | Data storage and dimensional modeling |
| SQL Server Integration Services (SSIS) | ETL processing and orchestration |
| Power BI | Data visualization and reporting |
| Git / GitHub | Source control and version management |

## Data Pipeline

### 1. Data Extraction – Python

Python connects to the DummyJSON Products API:

`https://dummyjson.com/products`

The extraction process:
- Retrieves product information in JSON format.
- Saves the response as a timestamped JSON file.
- Preserves the original API payload for downstream processing.

**Note:** The default API response returns 30 products, while the API reports 194 products in total. Pagination is required to retrieve the complete dataset.

### 2. Bronze Layer – Raw Data

The Bronze layer stores the original JSON payload in SQL Server.

Main table:

`bronze.products_raw`

This layer preserves source data and ingestion metadata, providing the foundation for subsequent transformations.

### 3. Silver Layer – Data Transformation

An SSIS package processes the raw JSON data and transforms it into structured relational records.

Main tables:

- `silver.products`
- `silver.product_reviews`

The transformation process extracts product attributes and prepares the data for analytical use.

### 4. Gold Layer – Dimensional Model

The Gold layer provides a dimensional model designed for analytical queries and historical tracking.

**Dimension tables**

- `gold.dim_product`
- `gold.dim_date`

**Fact table**

- `gold.fact_product_snapshot`

The fact table stores product snapshots, including price, discount percentage, rating, stock, ingestion timestamp, and ingestion ID.

This structure supports historical comparisons across ingestion runs.

### 5. Analytical Views

The project includes four analytical views:

- `gold.vw_product_changes`
- `gold.vw_product_inventory_changes`
- `gold.vw_product_kpis`
- `gold.vw_product_snapshot_history`

These views provide access to product changes, inventory movements, KPIs, and historical snapshots.

## ETL Monitoring and Data Quality

The pipeline includes audit tables to monitor execution:

- `audit.ETL_Run_Log`
- `audit.ETL_Step_Log`

They track pipeline executions, individual ETL steps, execution status, processed row counts, and error information.

Data integrity is supported through:

- Primary keys.
- Foreign keys.
- Unique constraints.
- Check constraints for ETL execution statuses.

## Project Structure

```text
ProductDataPlatform_v3/
│
├── ingestion/
│   ├── api_extract.py
│   ├── load_bronze.py
│   ├── test_sql_connection.py
│   └── transform_products.py
│
├── SSIS/
│   └── PRODUCT-DATA-PLATFORMV3/
│       ├── 01_Load_Products.dtsx
│       ├── PRODUCT-DATA-PLATFORMV3.database
│       ├── PRODUCT-DATA-PLATFORMV3.dtproj
│       ├── PRODUCT-DATA-PLATFORMV3.slnx
│       └── Project.params
│
├── sql/
│   └── ProductDataPlatform_v3.sql
│
├── docs/
│   └── samples/
│       └── products_sample.json
│
├── powerbi/
│   └── Product_Data_Platform.pbix
│
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.x
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- Visual Studio with SQL Server Integration Services Projects extension
- Power BI Desktop (optional)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/rhenangp021/product-DW-platformV3.git

cd product-DW-platformV3
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install requests pyodbc
```

### 4. Configure SQL Server connection

Review the connection settings in the Python ingestion scripts and configure them for your SQL Server environment.

### 5. Deploy the database

Execute the SQL deployment script:

`sql/ProductDataPlatform_v3.sql`

This script creates the database objects required by the pipeline. It is intended for a fresh database deployment.

### 6. Run API extraction

```bash
python ingestion/api_extract.py
```

### 7. Load data into Bronze

```bash
python ingestion/load_bronze.py
```

### 8. Execute the SSIS package

Open the SSIS solution in Visual Studio and execute:

`SSIS/PRODUCT-DATA-PLATFORMV3/01_Load_Products.dtsx`

The package processes the Silver and Gold layers and records execution details in the audit tables.

## Future Improvements

- Implement API pagination to retrieve all available products.
- Automate the complete pipeline execution.
- Improve error handling and retry mechanisms.
- Expand data quality validations.
- Extend historical analysis and Power BI reporting.

## Author

**Rhenan Guimarães**

Senior Database Administrator | Data Engineering

GitHub: [github.com/rhenangp021](https://github.com/rhenangp021)
