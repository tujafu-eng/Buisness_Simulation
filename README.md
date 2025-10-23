## Overview
This Python project simulates the operation of a soda factory over a given number of years.  
It models **resource production**, **soda creation**, **market demand**, and **financial performance** (sales and profit).  
Each month, the factory produces resources, manufactures soda, and sells based on market popularity — which fluctuates randomly and seasonally.

Results are visualized in a **matplotlib line graph** and exported to a **CSV file** for analysis.

---

## Features

-  **Dynamic Simulation:**  
  Runs for any number of years, with monthly production and sales cycles.

- **Growth System:**  
  Factory efficiency improves over time based on a user-defined growth rate.

-  **Market Popularity:**  
  Market demand changes monthly and seasonally, simulating real-world fluctuations.

-  **Profit Calculation:**  
  Revenue, production cost, and profit are computed monthly and displayed.

-  **Data Visualization:**  
  Generates a graph showing Sales and Profit over time.

-  **CSV Export:**  
  Saves all data (month, revenue, profit) into an easy-to-read CSV file.

---

##  Classes Breakdown

| Class | Description |
|--------|--------------|
| **Factory** | Handles production of water, sugar, and glass. Converts them into soda based on recipe and costs. |
| **Market** | Simulates changing demand and popularity. Affects monthly soda sales. |
| **Simulation** | Controls the simulation timeline, runs production/sales cycles, calculates finances, tracks data, and exports results. |

---

## Formula Details

- **Soda Recipe:**  
  `3 water + 2 sugar + 1 glass = 1 soda`

- **Production Cost (per soda):**  
  `(3 × water_cost) + (2 × sugar_cost) + (1 × glass_cost)`

- **Revenue (per soda):**  
  `$3.25`

- **Profit:**  
  `Revenue - Production Cost`

- **Popularity Growth:**  
  Randomized between `-0.02` and `+0.03`, scaled by a monthly base value.

---

## 🌦 Seasonal Popularity Base

| Month | Popularity Base |
|--------|----------------|
| Jan | 0.75 |
| Feb | 0.85 |
| Mar | 0.9 |
| Apr | 1.0 |
| May | 1.2 |
| Jun | 1.5 |
| Jul | 1.5 |
| Aug | 1.0 |
| Sep | 0.95 |
| Oct | 0.9 |
| Nov | 0.85 |
| Dec | 0.85 |

---

## How to Run

1. **Install dependencies**
   ```bash
   pip install matplotlib
