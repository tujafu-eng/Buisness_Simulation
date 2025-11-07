import csv
import random
import matplotlib.pyplot as plt
import csv as cs
import streamlit as st

class Factory:
    def __init__(self, growth=1, water_cost=0.05, sugar_cost=0.25, glass_cost=0.50):
        self.growth = growth
        self.water_cost = water_cost
        self.sugar_cost = sugar_cost
        self.glass_cost = glass_cost

        self.water = 0
        self.sugar = 0
        self.glass = 0
        self.soda = 0

    def produce_resources(self):
        # Simulate resource generation
        self.glass += random.gauss(2500, 300) * self.growth
        self.sugar += random.gauss(2500, 300) * self.growth
        self.water += random.gauss(2500, 300) * self.growth

    def soda_produced(self):
        soda_made = 0
        while self.water >= 3 and self.sugar >= 2 and self.glass >= 1:
            soda_made += 1
            self.water -= 3
            self.sugar -= 2
            self.glass -= 1
        self.soda += soda_made
        return soda_made

    def production_cost(self, soda_count):
        return (soda_count * (3 * self.water_cost + 2 * self.sugar_cost + 1 * self.glass_cost))


class Market:
    def __init__(self, popularity=1.0):
        self.popularity = popularity

    def update_popularity(self, base, growth=1):
        delta = random.uniform(-0.02, 0.03)
        self.popularity = max(0.5, min(2.0, self.popularity + delta * base)) * growth
        return self.popularity

    def demand(self, popularity):
        base = random.randint(2000, 3000)
        return int(base * popularity)


class Simulation:
    def __init__(self, years=1, growth_rate=0.05):
        self.factory = Factory()
        self.market = Market()
        self.years = years
        self.month = 1
        self.year = 0
        self.growth_rate = growth_rate

        # Tracking
        self.sales_history = []
        self.profit_history = []
        self.time = []

    def run(self):
        for _ in range(self.years * 12):
            # Month & Year handling
            if self.month > 12:
                self.month = 1
                self.year += 1

            # Seasonal popularity effect
            base_pop = self.monthly_popularity_base()

            # Production phase
            self.factory.produce_resources()
            soda_made = self.factory.soda_produced()

            # Market & Sales
            popularity = self.market.update_popularity(base_pop)
            sales = min(soda_made, self.market.demand(popularity))

            # Finance
            cost = self.factory.production_cost(soda_made)
            revenue = sales * 3.25
            profit = round(revenue - cost, 3)

            # Tracking
            self.sales_history.append(revenue)
            self.profit_history.append(profit)
            self.time.append(f"Year {self.year} Month {self.month}")

            # Growth
            self.factory.growth += self.growth_rate
            self.month += 1

            print(f"Year {self.year}, Month {self.month}: Popularity={popularity:.2f}, Sales={sales}, Profit=${profit:.2f}")

    def export_to_csv(self, filename='Output_data.csv'):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Time", "Revenue", "Profit"])
            for t, revenue, profit in zip(self.time, self.sales_history, self.profit_history):
                writer.writerow([t, revenue, profit])
        print(f"Data exported to {filename}")

    def monthly_popularity_base(self):
        month_bases = {
            1: 0.75, 2: 0.85, 3: 0.9, 4: 1.0, 5: 1.2, 6: 1.5,
            7: 1.5, 8: 1.0, 9: 0.95, 10: 0.9, 11: 0.85, 12: 0.85
        }
        return month_bases.get(self.month, 1.0)

    def plot(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.sales_history, label="Sales ($)")
        plt.plot(self.profit_history, label="Profit ($)")
        plt.legend()
        plt.title("Sales and Profit Over Time")
        plt.xlabel("Month")
        plt.ylabel("Value ($)")
        plt.grid(True)
        plt.show()


# ---- Run the simulation ----
# Get user input
years = st.number_input("How many years to simulate?", min_value=1, max_value=50, value=5, step=1)
growth_rate = st.number_input("Enter growth rate (e.g. 0.05):", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

# Initialize Simulation correctly
sim = Simulation(years=int(years), growth_rate=float(growth_rate))

sim.run()
sim.plot()
sim.export_to_csv()
