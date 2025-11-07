# 🛫 Akasa Air – Data Engineering Assessment

> Goal: Developing an ETL pipeline to process and analyze customer and order data from multiple sources (CSV and XML) using both database table and data-frame (in-memory) approaches. Computes KPIs and visualizations for the insights. Rerunable ETL pipeline without any human intervention daily.

---

## 📘 Project Overview

This project implements the *Akasa Air Data Engineer Task-1* requirements:
1. Process two daily source files:
   - task_DE_new_customers.csv
   - task_DE_new_orders.xml
2. Implement *two approaches*:
   - 🧱 *Table-Based Approach (MySQL)* → cleaning, loading, SQL-based KPIs  
   - 🧠 *In-Memory Approach (Python Pandas)* → cleaning, joining, KPI functions
3. Compute 4 KPIs:
   - Repeat Customers  
   - Monthly Order Trends  
   - Regional Revenue  
   - Top Customers (Last 30 Days)
4. Includes:
   - Time-zone normalization (Asia/Kolkata → UTC)
   - Daily re-runnable ETL
   - Visualizations for insights (via Streamlit + Plotly)
   - Secure credential handling (.env)
   - Logging & automation (Windows Task Scheduler)

---

## 🧩 Tech Stack

| Layer | Tool / Library | Purpose |
|-------|----------------|----------|
| *Language* | Python 3.12 | Main ETL & analytics logic |
| *Database* | MySQL 8.x | Persistent storage (table-based approach) |
| *Libraries* | pandas, lxml, sqlalchemy, pymysql, python-dotenv, pytz, plotly, streamlit | Data handling, XML parsing, DB I/O, time-zone, visualization |
| *Automation* | Windows Task Scheduler | Daily ETL re-runs |
| *IDE* | Visual Studio Code | Development environment |
| *OS* | Windows 11 | Execution environment |

---

---

## 🧭 System Design

### 🔹 High-Level Flow (Mermaid Diagram)

mermaid
flowchart TD
    A[Daily Source Files<br>CSV + XML] --> B[Preprocessing Layer]
    B --> C1[In-Memory Clean DataFrame]
    B --> C2[MySQL Clean Tables]
    C1 --> D1[In-Memory KPI + Visuals]
    C2 --> D2[SQL KPI Queries]
    D1 --> E[Streamlit Dashboard]
    D2 --> E
    E --> F[User Insights]
    F -->|Automated daily 9 AM run| G[Windows Task Scheduler]

----

## 🏗 Project Structure

akasaair_de_task/
├─ README.md
├─ run_pipeline.py # orchestrates both approaches
├─ requirements.txt
├─ .env.example # sample env configuration
├─ data/ # source data
│ ├─ task_DE_new_customers.csv
│ └─ task_DE_new_orders.xml
├─ src/
│ ├─ common/ # shared utilities
│ │ ├─ config.py
│ │ ├─ io_sources.py
│ │ └─ tz_utils.py
│ ├─ in_memory/ # In-Memory approach
│ │ ├─ preprocess_inmem.py
│ │ ├─ kpi_inmem.py
│ │ └─ insights_inmem.py
│ ├─ table_based/ # Table-Based (MySQL) approach
│ │ ├─ db.py
│ │ ├─ preprocess_table.py
│ │ ├─ load_table.py
│ │ └─ kpi_sql.sql
│ └─ dashboard/ # visualization layer
│ └─ streamlit_app.py
└─ setup_and_run_etl.bat # runs ETL + schedules daily job

-----

## 🧩 Implementation Details

### 🧠 In-Memory Approach
- Cleans & preprocesses data entirely with *Pandas*.  
- Normalizes mobile numbers (last 10 digits, int64).  
- Converts timestamps from *Asia/Kolkata → UTC*.  
- Merges CSV & XML → unified_df.  
- Computes KPIs via Python functions.  
- Visualizes results using *Plotly* charts inside Streamlit.


### 🗃 Table-Based Approach
- Performs equivalent cleaning using the same logic.  
- Loads data into *MySQL* (customers, orders_fact, order_items).  
- Executes *SQL queries* (in kpi_sql.sql) to compute KPIs.  
- Streamlit dashboard can toggle between both approaches.

---

### ⏰ Scheduling (Re-runnable Daily ETL)
- *Batch file:* setup_and_run_etl.bat  
  - Activates the Python virtual environment.  
  - Runs the ETL (python run_pipeline.py).  
  - Registers itself in *Windows Task Scheduler* to run every day at *9:00 AM*.
 
  -----

## 🧩 Setup & Run Guide
### 1) Clone the repository

git clone <repo-url>
cd <working-dir>

### Create virtual environment

python -m venv .venv
.venv\Scripts\activate

###3️⃣ Install dependencies

pip install -r requirements.txt


### 4️⃣ Configure environment

DB_HOST=localhost
DB_PORT=3306
DB_USER=user_name
DB_PASSWORD=user_password
DB_NAME=akasa_de
TIMEZONE=Asia/Kolkata

### 5️⃣ Run ETL once manually

python run_pipeline.py


Expected:

In-memory unified view:
...
Table-based load completed.



### 6️⃣ Test dashboard

streamlit run src/dashboard/streamlit_app.py


### 7️⃣ Automate daily run (Windows)
Run as Administrator:

setup_and_run_etl.bat


✅ This will:
- Run ETL immediately
- Create a Windows scheduled task named AkasaAir_Daily_ETL
- Run every day at 9 AM
  
------------

## 📊 KPIs & Insights

| *KPI* | *Description* | *Visualization* |
|----------|------------------|--------------------|
| *Repeat Customers* | Customers placing more than one order | Table |
| *Monthly Order Trends* | Total orders & revenue per month | Line Chart |
| *Regional Revenue* | Total revenue grouped by region | Funnel Chart |
| *Top Customers (30 Days)* | Top 10 customers by spend in the last 30 days | Horizontal Bar Chart |

-------
## 🕒 Time-Zone Awareness
All order_date_time values are localized from Asia/Kolkata to UTC before KPI calculations and storage, ensuring consistent 30-day rolling calculations regardless of system time.

----------
## ⚙ Scalability & Improvements

| *Area* | *Improvement* |
|-----------|-----------------|
| *Scheduling* | Convert .bat to *Airflow DAG* or *Prefect* flow |
| *Monitoring* | Add logging & email alerts |
| *Validation* | Integrate *Great Expectations* for schema checks |
| *Deployment* | Dockerize *ETL + MySQL + Streamlit* for portability |

----------
## 🪄 Key Highlights

- ✅ Two complete ETL approaches  
- ✅ Time-zone normalization (mandatory)  
- ✅ Daily re-runnable pipeline  
- ✅ Visual KPI dashboard  
- ✅ Clean, modular, well-commented code  
- ✅ Professional documentation (this README)
