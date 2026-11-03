# Strategic Sourcing Intelligence

Using **synthetic 2025 procurement data**, this project demonstrates how automated analytics and foundational data governance controls can support more transparent, consistent, and defensible business decisions.

**Core Focus:** Strategic Sourcing | Supplier Data Governance | Spend Analytics | Procurement Controls | Financial Modeling | Executive Reporting

> **Portfolio Disclaimer:** All procurement transactions, supplier identities, and financial results are fictional. Savings opportunities represent modeled scenarios rather than realized financial benefits.

---

## 📋 1. Business Problem & Objective

### The Business Challenge

Enterprise procurement teams frequently manage large purchasing volumes across multiple suppliers, business categories, and contractual arrangements.

Without consistent supplier information and centralized spend visibility, organizations may struggle to identify:

- Off-contract purchasing and missed negotiation opportunities.
- Fragmented purchasing activity across suppliers and categories.
- Supplier concentration and associated sourcing risks.
- Inconsistent supplier references and potentially duplicate invoices.
- Opportunities to improve contract utilization and purchasing discipline.
- Financial opportunities that warrant leadership consideration.

### The Solution

This project implements an automated Python analytics workflow that:

- Validates procurement transactions and supplier references.
- Aggregates spending by supplier and purchasing category.
- Measures contract coverage and off-contract purchasing exposure.
- Identifies potentially duplicate invoices and supplier concentration.
- Models potential savings under multiple financial assumptions.
- Prioritizes sourcing categories based on estimated opportunity.
- Generates structured CSV reports and an executive dashboard.

### Intended Business Value

Provide a repeatable analytical framework that helps procurement stakeholders identify sourcing opportunities, evaluate financial scenarios, and monitor purchasing activity.

**Executive Question:** How can procurement leadership use reliable transaction-level data to identify, quantify, and prioritize cost optimization opportunities?

---

## 🏢 2. Fictional Business Scenario

A fictional enterprise manages procurement activity across hundreds of suppliers and multiple purchasing categories.

Its supplier network includes **KG Soundworks**, a fictional North American electronics supplier used as a portfolio identity.

Procurement leadership wants to understand purchasing patterns, assess contract utilization, identify potential inefficiencies, and establish a consistent basis for sourcing decisions.

The project simulates this environment using synthetic supplier and transaction data.

The presence of a named supplier does not imply an actual commercial relationship or verified supplier performance.

---

## 🛠️ 3. Technical Architecture & Analytics Workflow

**Technology:** Python | pandas | matplotlib | CSV Data Processing

### Stage 1: Data Ingestion

Synthetic procurement transactions and supplier reference data provide the foundation for the analysis.

### Stage 2: Data Validation

The analysis validates transaction records and supplier references before generating procurement metrics.

This supports consistency between purchasing activity and the supplier information used for reporting.

### Stage 3: Spend Classification & Aggregation

Transactions are analyzed to calculate:

- Total procurement spend.
- Supplier-level spending.
- Category-level spending.
- Contracted versus off-contract purchasing.
- Supplier concentration.

### Stage 4: Procurement Exception Identification

The analysis identifies potentially duplicate invoice records and supplier concentration indicators for further review.

These indicators are analytical flags, not confirmed instances of payment duplication, fraud, or supplier risk.

### Stage 5: Financial Opportunity Modeling

Three savings scenarios are calculated using assumptions for:

- Addressable off-contract spend.
- Achievable savings rates.
- Estimated annual savings opportunities.

### Stage 6: Executive Reporting

The workflow generates structured reports and an executive dashboard to communicate findings and sourcing priorities.

---

## 🛡️ 4. Enterprise Supplier Data Governance & Procurement Controls

Reliable procurement intelligence depends on consistent supplier identities, accurate transaction records, and clearly defined business rules.

This project demonstrates selected foundational controls while identifying additional governance practices suitable for an enterprise implementation.

### Implemented Data Quality & Analytical Controls

| Control Area | Existing Analytical Capability | Governance Purpose |
|---|---|---|
| Supplier Reference Validation | Validation of supplier references | Support consistency between transactions and supplier records |
| Transaction Validation | Checks on procurement transaction records | Improve reliability of analytical inputs |
| Invoice Exception Monitoring | Potential duplicate invoice flags | Identify records requiring further investigation |
| Contract Coverage Monitoring | Off-contract spending calculations | Provide visibility into purchasing outside contracted arrangements |
| Supplier Concentration | Supplier spending and concentration indicators | Identify potential sourcing dependencies |
| Financial Scenario Transparency | Explicit addressable-spend and savings-rate assumptions | Distinguish modeled opportunities from realized outcomes |
| Reporting Consistency | Automated CSV reports and dashboard generation | Support repeatable analytical reporting |

### Supplier Master Data Governance

In an enterprise environment, supplier master data governance helps maintain consistent supplier identities and attributes across procurement systems.

Potential critical data elements include:

| Critical Data Element | Governance Consideration |
|---|---|
| Supplier ID | Unique, stable identifier for supplier records |
| Supplier Name | Consistent naming and approved change procedures |
| Geographic Region | Standardized geographic classification |
| Purchasing Category | Controlled category definitions |
| Contract Status | Clear definitions and validation of contract-related attributes |
| Transaction Reference | Consistent identifiers supporting transaction traceability |

These are illustrative governance considerations. The project does not implement a formal supplier master data management platform.

### Proposed Data Stewardship Model

| Enterprise Role | Illustrative Responsibility |
|---|---|
| Procurement Data Owner | Establish supplier data quality expectations and business accountability |
| Supplier Data Steward | Maintain supplier definitions and coordinate data issue resolution |
| Strategic Sourcing Analyst | Investigate spending anomalies and evaluate sourcing opportunities |
| Procurement Operations | Review transaction exceptions and contract-related discrepancies |
| Data Engineering / IT | Maintain data pipelines, validation logic, and reporting processes |
| Internal Audit | Independently evaluate relevant controls and supporting evidence |

*This responsibility model is proposed documentation, not an implemented assignment or approval system.*

### Audit Support & Exception Management

The generated reports provide useful starting points for procurement control reviews.

For example:

- `duplicate_invoice_flags.csv` identifies potential duplicate invoice records.
- `concentration_flags.csv` highlights supplier concentration indicators.
- `supplier_spend.csv` supports supplier-level spending analysis.
- `category_spend.csv` supports category-level review.
- `executive_summary.csv` consolidates key analytical metrics.

These outputs support analytical review but do not constitute a complete procurement audit trail or formal exception-resolution workflow.

---

## 📊 5. Executive Dashboard & Key Findings

![Strategic Sourcing Executive Dashboard](./sourcing_dashboard.png)

### Procurement Performance Indicators

| Key Performance Indicator | Result |
|---|---:|
| Annual Procurement Spend | $22.69M |
| Active Suppliers | 248 |
| Off-Contract Spend | $5.82M |
| Off-Contract Spend Share | 25.7% |
| Moderate Savings Opportunity | $145.5K |
| Top 10 Supplier Spend Share | 52.21% |

### Executive Insight

Approximately one-quarter of procurement spend falls outside contracted agreements.

This suggests an opportunity to investigate contract coverage, purchasing behavior, and potential negotiated pricing improvements.

The analysis also provides visibility into supplier concentration and purchasing categories that may warrant additional sourcing review.

All findings are derived from synthetic demonstration data.

---

## 💰 6. Financial Opportunity & Savings Scenarios

The financial model evaluates potential savings using different assumptions for addressable off-contract spend and achievable savings rates.

| Scenario | Addressable Spend | Assumed Savings Rate | Estimated Annual Savings |
|---|---:|---:|---:|
| Conservative | 25% | 2% | $29.1K |
| Moderate | 50% | 5% | $145.5K |
| Ambitious | 75% | 8% | $349.3K |

### Moderate Scenario

Addressing 50% of the approximately $5.82M in off-contract spend at an assumed 5% savings rate produces an estimated annual savings opportunity of **$145.5K**.

These figures are illustrative financial scenarios, not realized savings, validated supplier quotations, or guaranteed outcomes.

### Prioritized Sourcing Opportunities

The analysis ranks categories according to modeled savings opportunities under the moderate scenario.

| Priority | Purchasing Category | Estimated Savings |
|---|---|---:|
| 1 | Professional Services | $43.9K |
| 2 | MRO | $28.7K |
| 3 | Packaging | $27.7K |
| 4 | Raw Materials | $21.2K |
| 5 | Electronics | $15.9K |

The ranking reflects off-contract spending exposure and uniform savings assumptions. It does not independently establish supplier negotiability or implementation feasibility.

---

## 🎯 7. Executive Recommendations

### Priority 1: Strengthen Contract Coverage

Review high-value off-contract purchasing activity, beginning with Professional Services.

Evaluate opportunities to establish negotiated agreements, improve contract adoption, and reduce unmanaged spending.

### Priority 2: Target High-Impact Purchasing Categories

Assess MRO and Packaging for potential purchasing consolidation, supplier negotiations, and standardized buying practices.

### Priority 3: Improve Supplier Data Governance

Consider establishing consistent supplier naming conventions, critical data element definitions, stewardship responsibilities, and formal exception-resolution procedures.

These governance activities would help strengthen the reliability of supplier-level reporting.

### Priority 4: Establish Recurring Procurement Performance Monitoring

Develop a recurring review process for contract coverage, off-contract spending, supplier concentration, sourcing opportunities, and validated realized savings.

These recommendations represent proposed management actions, not initiatives completed by the project.

---

## 🗓️ 8. Illustrative 90-Day Implementation Roadmap

| Timeline | Recommended Initiative | Expected Deliverable |
|---|---|---|
| Days 1–30 | Validate supplier master data, spend classifications, and off-contract purchasing drivers | Data quality and contract leakage assessment |
| Days 31–60 | Prioritize sourcing categories and define supplier data stewardship responsibilities | Category sourcing plans and proposed governance ownership matrix |
| Days 61–90 | Launch selected sourcing initiatives and establish recurring KPI reviews | Procurement performance scorecard and exception management procedures |

This roadmap is an illustrative enterprise implementation plan. It does not represent work completed within the repository.

---

## ⚙️ 9. Setup & Installation

### Technology Requirements

- Python 3
- pandas
- matplotlib
- Dependencies listed in `requirements.txt`

### Clone the Repository

```bash
git clone https://github.com/gkarnelle-lab/Strategic-Sourcing-Intelligence.git
cd Strategic-Sourcing-Intelligence
```

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Run the Procurement Analysis

```bash
python3 analyze.py
```

Generated analytical reports are saved in the `outputs/` directory.

### Key Outputs

- `executive_summary.csv`
- `savings_scenarios.csv`
- `sourcing_opportunities.csv`
- `supplier_spend.csv`
- `category_spend.csv`
- `duplicate_invoice_flags.csv`
- `concentration_flags.csv`
- `sourcing_dashboard.png`

The dashboard is also displayed in the README using `./sourcing_dashboard.png`.

---

## 📦 10. Repository Components

| Component | Purpose |
|---|---|
| `analyze.py` | Automated procurement analysis |
| `generate_data.py` | Synthetic procurement data generation |
| `requirements.txt` | Python dependency definitions |
| `outputs/` | Generated analytical reports |
| `sourcing_dashboard.png` | Executive dashboard displayed in the README |
| `README.md` | Project documentation |

The repository also contains synthetic procurement and supplier data used for the analysis.

---

## 🔭 11. Limitations & Future Enhancements

### Current Limitations

- All supplier and procurement data is synthetic.
- Financial scenarios are based on assumptions rather than verified commercial opportunities.
- Potential duplicate invoices are flagged for review, not confirmed as duplicate payments.
- Supplier concentration indicators do not independently establish supplier financial or operational risk.
- The project does not implement formal supplier stewardship approvals or enterprise master data management workflows.

### Potential Enterprise Enhancements

**Supplier Data Governance Framework**

Develop formal data definitions, ownership assignments, and quality standards for critical supplier attributes.

**Supplier Master Data Quality Scorecard**

Introduce recurring measures for completeness, consistency, uniqueness, and validity.

**Exception Management Workflow**

Document issue ownership, investigation status, remediation decisions, and reviewer approvals.

**Procurement Control Matrix**

Map key purchasing risks to control objectives, review frequencies, responsible roles, and evidence requirements.

**Data Lineage & Audit Documentation**

Expand documentation showing how source attributes contribute to procurement KPIs and analytical outputs.

**Realized Savings Validation**

Introduce a separate process for distinguishing forecast savings opportunities from verified financial results.

These are proposed future capabilities rather than functionality already implemented in the repository.

---

## 💼 12. Business & Technical Skills Demonstrated

**Strategic Sourcing:** Spend analysis, supplier concentration, contract coverage, category prioritization, and procurement efficiency.

**Financial Analytics:** Scenario modeling, estimated savings quantification, executive KPIs, and sourcing opportunity assessment.

**Data Governance:** Supplier reference validation, critical data element concepts, data quality controls, and proposed stewardship practices.

**Technical Execution:** Python automation, pandas transformations, CSV reporting, data validation, and matplotlib visualization.

**Enterprise Decision Support:** Translating analytical findings into executive recommendations, operational control considerations, and an illustrative implementation roadmap.

---

*This portfolio project demonstrates how procurement analytics and foundational data governance practices can work together to support reliable reporting, improved spending visibility, and informed sourcing decisions.*

**Data Disclaimer:** All data and financial outcomes are fictional. No proprietary company information, actual negotiated savings, or verified business results are represented.
