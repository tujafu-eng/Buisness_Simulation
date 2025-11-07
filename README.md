# 🧃 Soda Market Simulation

**Author:** Tucker Fuller  
**Tech Stack:** Python · Streamlit · Pandas · Matplotlib  
**Focus Areas:** Simulation · Data Visualization · Event Systems · OOP Design

---

## 📖 Overview

This project simulates the operations of a fictional **soda company**, modeling everything from **resource production and factory management** to **customer behavior, marketing events, and profit generation**.

The simulation tracks:
- Dynamic **production rates** for sugar, glass, and water  
- Randomized **market and popularity events**  
- **Profit/loss** tracking and performance visualization  
- A clean **Streamlit dashboard** for interactive exploration  

This project demonstrates **Python programming, data analytics, and system design skills** — valuable for my transition into **network engineering and IT systems automation**.

---

## 🧩 Features

### 🏭 Factory Management
- Adjustable factory settings: growth rate, resource count, maintenance cost.  
- Produces water, sugar, and glass each turn using stochastic generation.

### 💸 Market Simulation
- AI-driven **agents (customers)** simulate purchases based on:
  - Income level  
  - Health preference  
  - Marketing influence  
  - Event modifiers  
- Popularity and price dynamically affect total sales.

### ⚙️ Event System
- Randomized market events with durations and cooldowns.  
- Impacts popularity, production, or customer behavior.  
- Balanced positive/negative probability system for realism.

### 📊 Visualization & Analytics
- **Streamlit dashboard** with:
  - Profit and inventory metrics  
  - Production and sales over time  
  - Pie chart showing profit distribution  
- **CSV Export** for post-simulation analysis.

---

## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/Soda-Market-Simulation.git
cd Soda-Market-Simulation
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
(If you don’t have Streamlit, install it manually:)

bash
Copy code
pip install streamlit pandas matplotlib numpy
3️⃣ Run the simulation
bash
Copy code
streamlit run Soda_simulation.py
Then open the Streamlit app in your browser.
You’ll be able to configure settings and visualize simulation results in real-time.

🧠 Learning Objectives
This project was designed to strengthen:

Object-Oriented Programming (OOP) in Python

Simulation logic and randomness modeling

Data analysis and visualization (Pandas / Matplotlib)

Web app deployment with Streamlit

System design for modularity and scalability

As a network engineering student, I built this to apply Python automation and analytics to a simulated production environment — a skillset that parallels real-world IT and infrastructure modeling.

📂 Project Structure
bash
Copy code
📁 Soda-Market-Simulation/
│
├── 📄 Soda_simulation.py            # Main simulation and Streamlit interface
├── 📄 Agent.py                      # Customer class and market simulation logic
├── 📄 Production.py                 # Resource production systems (water, sugar, glass)
├── 📄 Event List and calculator.py  # Event management and random modifiers
├── 📄 requirements.txt              # Dependency list
└── 📄 README.md                     # Project overview (this file)
🧮 Example Outputs
Profit Chart:
Displays the company’s cumulative profit over time.

Production Metrics:
Tracks individual production lines and bottlenecks.

Event Log:
Summarizes positive and negative market events that occurred during the run.

Exportable CSV Example:

Time	Profit	Soda Sold	Water	Sugar	Glass
1	13400	92	120	85	100
2	27850	108	121	89	104

🔧 Future Improvements
Implement AI optimization to automatically adjust production resources for max profit.

Add multifactory networking (simulate distributed production sites).

Create visual event reports showing which types most affected performance.

Improve the Streamlit UI with cached data and tooltips.

💼 Career Relevance
This project serves as a portfolio piece demonstrating:

Practical Python programming for system-level simulation

Understanding of event-driven models and data pipelines

Skills applicable to network monitoring, automation, and analytics

As I pursue certifications in:

CCNA → Security+ → AWS Certified Cloud Practitioner,
this project shows my ability to combine technical networking goals with software and data engineering tools.

🏁 Acknowledgements
Built with:

Streamlit for interactive visualization

Matplotlib and Pandas for data analysis
