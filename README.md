# ReadyNest Data Analytics Suite — Week 2 Task 📊🚀
> **Project Title:** Customer Insights & Recommendation Project  
> **Tagline:** Analyze. Understand. Suggest. Grow.

An interactive analytics application engineered to fulfill the ReadyNest Week 2 core milestone. This system processes transactional customer datasets to uncover deep operational insights, handle behavioral segment profiles, and present data-driven business recommendations through a web-based Single Page Application (SPA).

---

## 🎯 Task Objectives & Analysis Areas
As outlined in the assignment brief, this project systematically addresses five critical business layers:

1. Customer Analysis: Identifying top high-spending consumers, monitoring new vs. returning buyer ratios, and auditing baseline transaction frequency.
2. Behavior Analysis: Tracking product category popularity, monthly sales trends, and cross-border distribution channels.
3. Customer Segmentation: Programmatically bucketizing the user base into distinct value pillars: High Value (Elite 6%), Medium Value (Core 44%), and Low Value (Introductory 50%) segments based on total lifetime spend.
4. Interactive Dashboarding: Crafting an enterprise-grade workspace featuring live data streams, key KPI rows, structural matrices, and real-time interactive slicing components.
5. Business Suggestions: Translating quantitative charts into clear, qualitative tactical playbooks to isolate churn risk and expand average order value (AOV).

---

## 💡 Key Business Questions Answered
The analytical pipeline evaluates the dataset to solve these exact problem spaces:
* Who are our top customers? Handled via a dynamic, interactive live revenue leaderboard component.
* Which products are performing the best? Surfaces the top 5 trending products directly out of the transactional logs.
* Which regions are most profitable? Geographically pinpointed through spatial mapping layers filtered via an active market slicer.
* How can we increase customer retention & sales? Accompanied by integrated automated marketing action strategies mapped by cohort status.

---

## 📦 Project Deliverables Provided
* Cleaned & Prepared Dataset: Automated ingestion & parsing layers handling over 100,000 rows.
* Exploratory Data Analysis (EDA): Interactive visualization matrices (Donut charts, Scatter grids, Bar distributions, and Line graphs).
* Geographic Revenue Footprint: Interactive Leaflet maps reflecting custom sales coordinates dynamically.
* Business Insights Report: Integrated dynamic text compilation engine streaming deep tactical analysis right to the terminal UI screen.

---

## 🛠️ Architecture & Stack
* Data Processing Layer: Python 3.x, Pandas DataFrames
* Application API Layer: Native Python http.server running custom REST paths with query parameters
* Interface & Rendering Engine: HTML5, CSS3 Glassmorphic UI design, Vanilla JS (ES6 Core, Async Fetch APIs), Chart.js, Leaflet.js

---

## 🏃‍♂️ Quick Start Guide

### 1. Install Dependencies
Ensure you have Python 3 installed. Run the tracking dependency installations directly from your terminal:

    pip install -r requirements.txt

### 2. Boot up the Dashboard Pipeline
Launch the background database and routing engine script:

    python server.py

### 3. Open the Workspace UI
Navigate to the hosted server instance via your preferred web browser window:

    http://localhost:8000/dashboard/web/index.html

---

## 📂 Project Directory Structure

    📂 readynest-analytics-hub/
    ├── 📄 server.py                    # Core Python HTTP serving infrastructure & API filter routes
    ├── 📄 README.md                    # Repository documentation matching week2.png briefs
    ├── 📄 requirements.txt             # Project engine package dependencies
    ├── 📂 outputs/
    │   ├── 📄 cleaned_customer_dataset.csv  # Cleaned raw master transaction row file 
    │   └── 📄 business_insight_summary.txt # Raw executive narrative text summary report
    └── 📂 dashboard/
        └── 📂 web/
            ├── 📄 index.html           # Main SPA workspace layout panel shell
            ├── 📄 app.js               # Frontend routing mechanism & interactive graphing engines
            └── 📄 style.css            # Dark enterprise design system sheets