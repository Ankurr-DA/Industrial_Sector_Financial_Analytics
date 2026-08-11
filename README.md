# Industrial Sector Financial Analytics

---

## Project Overview
This end-to-end data pipeline project transforms raw client, invoice, and payment records into structured Excel billing reports and an interactive executive dashboard. The objective is to audit invoice-to-payment completeness, measure collection performance across industries and client segments, and quantify outstanding and uncollected exposure across the business.

## Data Pipeline & Architecture
The project follows a structured ETL (Extract, Transform, Load) pipeline:  
**CSV → MySQL → SQL Views → Python Data Cleaning → Excel → Tableau**

1. **Database Ingestion:** Ingested three core raw datasets (`clients`, `invoices`, `payments`) totaling **7,206** invoice records into a MySQL database (`sql_analytics5`) using the Python `sqlalchemy` engine.
2. **SQL Auditing & Views:** Ran comprehensive data quality checks to identify missing segment/industry/term values, currency-formatted amounts (₹, Rs., commas), invalid date formats, and duplicate primary keys across all three tables. Deduplicated records using window functions, removed orphan invoices and orphan payments via inner joins, and created optimized SQL views (`v_invoices` and `v_payments`) for downstream processing.
3. **Python Cleaning & Normalization:** Standardized text fields (`client_segment`, `industry`, `agreed_terms`), parsed currency-formatted `invoice_amount` and `amount_paid` values, converted string timestamps to `datetime` objects, and mapped inconsistent contract terms (e.g. `net15`, `15 days`) to a standard `Net-15 / Net-30 / Net-60` format using `pandas`.
4. **Audit & Collections Analysis:** Built a rule-based **Audit Status** engine (Complete / Pending / Incomplete) based on payment status, due dates, and data completeness, producing two core executive exports:
   * **Industry Billing Report:** Aggregates invoice volume, billed value, and collected revenue by industry and audit status, calculating outstanding balance and collection rate.
   * **Segment Billing Report:** Aggregates invoices issued, billed exposure, and cash recovered by client segment and audit status, calculating uncollected exposure.
5. **Dashboard Visualization:** Connected the output reports into a Tableau dashboard highlighting KPI metric cards, large interactive Transaction Status filter buttons (Complete/Incomplete/Pending), outstanding balance by industry, uncollected exposure by segment, collection rate by industry, and billed vs. recovered cash by segment.

---

## Project Deliverables & Visual Preview

### 1. Industry Billing Report
Breaks down every invoice by **Industry** and **Audit Status** (Complete / Incomplete / Pending), reporting Invoice Volume, Billed Value, Collected Revenue, Outstanding Balance, and Collection Rate for each combination. The report totals **7,206** invoices with a combined Billed Value of **₹6.97B** and Collected Revenue of **₹5.26B**, leaving an Outstanding Balance of **₹1.71B**.

<img width="1007" height="502" alt="image" src="https://github.com/user-attachments/assets/665324a7-059f-4b9e-b50f-ad102ff5dd5d" />


### 2. Segment Billing Report
Breaks down every invoice by **Client Segment** (Enterprise / Mid Market / SMB) and **Audit Status**, reporting Invoices Issued, Billed Exposure, Cash Recovered, and Uncollected Exposure for each combination. The report totals **7,206** invoices with a combined Billed Exposure of **₹6.97B** and Cash Recovered of **₹5.26B**, leaving an Uncollected Exposure of **₹1.71B**.

<img width="1074" height="265" alt="image" src="https://github.com/user-attachments/assets/0151eaed-217d-4ffa-9071-a5ead7eb166f" />

### 3. Live Tableau Executive Dashboard
An interactive dashboard displaying key billing metrics: **₹6.97B** Total Invoice Amount, **₹5.26B** Total Collected Volume, **₹1.71B** Total Outstanding Balance, and **7,206** Total Invoices. The dashboard features breakdown charts for Outstanding Balance by Industry, Uncollected Exposure per Segment, Collection Rate per Industry, and Billed vs. Recovered Cash per Segment.

#### Interactive Transaction Status Filters
The dashboard features large **Complete / Incomplete / Pending** filter buttons at the top, allowing users to instantly filter every chart on the dashboard down to a single audit status — isolating fully reconciled invoices, invoices with data or payment gaps, or invoices still awaiting payment.

> 📄 [**Tableau Dashboard Direct Link**](https://public.tableau.com/views/IndustrialSectorFinancialAnalytics/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) <!-- Add your published Tableau Public link here -->

<img width="1164" height="776" alt="industrial_sector_dashboard_no_margin" src="https://github.com/user-attachments/assets/d2f08ead-b381-4d00-b284-329f49a90a4b" />

---

## Repository Structure

* [`clients.csv`](./clients.csv)
* [`invoices.csv`](./invoices.csv)
* [`payments.csv`](./payments.csv)

---

* [`data_transfer5.py`](./data_transfer5.py)
 --> [`SQL_Analytics5.sql`](./SQL_Analytics5.sql)
 --> [`python_analytics5.py`](./python_analytics5.py)

---

* [`Industry_Billing.xlsx`](./Industry__Billing.xlsx)
* [`Segment_Billing.xlsx`](./Segment__Billing.xlsx)

---

* [`Industrial_Sector_Financial_Analytics.twbx`](./Industrial_Sector_Financial_Analytics.twbx)

---

## Technologies Used
* **Languages:** Python (`pandas`, `sqlalchemy`, `numpy`), SQL
* **Database:** MySQL
* **Reporting & Viz:** Excel, Tableau
* **Environment:** VS Code
