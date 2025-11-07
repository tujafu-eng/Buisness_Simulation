import random
import matplotlib.pyplot as plt
import streamlit as st
import importlib.util

# Import Event class from file with spaces in name
spec = importlib.util.spec_from_file_location("event_module", "Event List and caculator.py")
event_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(event_module)
Event = event_module.Event

# Import Production functions
spec_prod = importlib.util.spec_from_file_location("production_module", "Production.py")
production_module = importlib.util.module_from_spec(spec_prod)
spec_prod.loader.exec_module(production_module)
Water_prod = production_module.Water_prod
Sugar_prod = production_module.Sugar_prod
Glass_prod = production_module.Glass_prod


# ------------------------------
# Factory Class
# ------------------------------
class Factory:
    def __init__(self, resources=None):
        self.soda_produced = 0
        self.soda_stored = 0
        self.resources = resources if resources else {"farms": 1, "waterpumps": 1, "mines": 1}

    def produce_soda(self, growth_rate, production_multiplier=1.0):
        """Simulate soda production based on available resources."""
        # Get raw materials from resources
        water = Water_prod(self.resources)
        sugar = Sugar_prod(self.resources)
        glass = Glass_prod(self.resources)
        
        # Production is limited by the scarcest resource
        # Each recipe (1 water + 1 sugar + 1 glass) produces 10 sodas
        max_production = min(water, sugar, glass)
        
        # Apply production multiplier (events can affect this)
        # Growth rate is a percentage increase: 0.05 = 5% growth = 105% of base (1.0 + 0.05 = 1.05)
        production_efficiency = 1.0 + growth_rate  # Add 1 to make it a multiplier (0.05 becomes 1.05 = 105%)
        base_production = int(max_production * production_efficiency * production_multiplier * 10)  # 10x production per recipe
        
        # Realistic production variation (scaled for higher production)
        produced = base_production + random.randint(-50, 50)
        produced = max(0, produced)  # Ensure production is never negative
        self.soda_produced = produced
        return produced
    
    def update_resources(self, resources):
        """Update resource counts."""
        self.resources = resources


# ------------------------------
# Agent Class
# ------------------------------
class Agent:
    def __init__(self, name):
        self.name = name
        self.create_customer()

    def create_customer(self):
        locations = ['Store 1', 'Store 2', 'Store 3', 'Store 4', 'Store 5']
        self.base = random.randint(80, 100)
        self.age = random.randint(18, 70)
        self.salary = random.randint(5000, 12000)
        self.influence = random.uniform(0, 1)
        self.location = random.choice(locations)
        self.health = random.randint(50, 100)
        self.alternative_pull = random.uniform(0, 1)
        self.festivity = random.uniform(0, 1)


# ------------------------------
# Simulation Functions
# ------------------------------
def create_population(size: int):
    return [Agent(f"Customer_{i+1}") for i in range(size)]


def simulate_market(population, soda_price=1.25, base_popularity=1.0):
    total_sales = 0
    total_revenue = 0
    store_sales = {f"Store {i}": 0 for i in range(1, 6)}
    popularity = base_popularity

    for agent in population:
        buy_chance = agent.base / 100

        # Adjust buy chance
        if 18 <= agent.age <= 28:
            buy_chance += 0.03
        elif agent.age >= 70:
            buy_chance -= 0.03

        if agent.salary < 7000:
            buy_chance += 0.10
        elif agent.salary < 10000:
            buy_chance += 0.07
        else:
            buy_chance += 0.04

        if agent.health >= 90:
            buy_chance -= 0.05
        elif 50 <= agent.health < 89:
            buy_chance += 0.03

        if agent.festivity >= 0.8:
            buy_chance += 0.1
        if agent.alternative_pull >= 0.7:
            buy_chance -= 0.15

        buy_chance = max(0, min(buy_chance, 1))

        # Decide if agent buys
        if random.random() <= buy_chance:
            # Realistic: customers buy more cans to increase sales volume
            # Higher chance of buying 6-packs or multiple cans
            if random.random() < 0.5:  # 50% chance of buying a 6-pack
                cans = 6
            elif random.random() < 0.3:  # 30% chance of buying 4-5 cans
                cans = random.randint(4, 5)
            else:  # 20% chance of buying 1-3 individual cans
                cans = random.randint(1, 3)
            total_sales += cans
            total_revenue += soda_price * cans
            store_sales[agent.location] += cans

            if agent.influence >= 0.7:
                popularity += 0.02

    # Best store bonus
    best_store = max(store_sales, key=store_sales.get)
    if store_sales[best_store] > len(population) * 3:
        popularity += 0.03

    # Convert to list format for charts
    store_sales_list = [{"store": k, "sales": v} for k, v in store_sales.items()]
    return total_sales, total_revenue, popularity, store_sales_list


# ------------------------------
# Event Manager
# ------------------------------
class EventManager:
    def __init__(self):
        self.active_events = []  # List of (event, months_remaining)
        self.event_cooldowns = {}  # Dict of event_name: months_until_available
        self.event_history = []  # List of events that occurred
        
    def update_events(self):
        """Update active events and cooldowns."""
        # Decrease time for active events
        self.active_events = [(event, time - 1) for event, time in self.active_events if time > 1]
        
        # Decrease cooldowns
        for event_name in list(self.event_cooldowns.keys()):
            self.event_cooldowns[event_name] -= 1
            if self.event_cooldowns[event_name] <= 0:
                del self.event_cooldowns[event_name]
    
    def trigger_random_event(self, chance=0.15, current_month=0):
        """Try to trigger a random event."""
        if random.random() > chance:
            return None
        
        # Get available events (not on cooldown)
        available_events = [e for e in Event.Event_List 
                           if e["Name"] not in self.event_cooldowns]
        
        if not available_events:
            return None
        
        # Select random event
        event = random.choice(available_events)
        
        # Add to active events
        self.active_events.append((event, event["Time"]))
        
        # Add to cooldown
        self.event_cooldowns[event["Name"]] = event["CoolDown"]
        
        # Add to history with current month
        self.event_history.append((event, current_month + 1))
        
        return event
    
    def get_popularity_modifier(self):
        """Get total popularity modifier from active events."""
        modifier = 0
        for event, _ in self.active_events:
            if event["Classification"] == "Popularity":
                modifier += event["Effect"]
        return modifier / 100.0  # Convert to percentage
    
    def get_production_modifier(self):
        """Get total production modifier from active events."""
        modifier = 0
        for event, _ in self.active_events:
            if event["Classification"] == "Production":
                modifier += event["Effect"]
        # Negative effects reduce production, so convert to multiplier
        # Effect of -2 means 2% reduction = 0.98 multiplier
        return max(0.1, 1.0 + (modifier / 100.0))  # Clamp between 0.1 and above
    
    def get_market_modifier(self):
        """Get market modifier (affects sales)."""
        modifier = 0
        for event, _ in self.active_events:
            if event["Classification"] == "Market":
                modifier += event["Effect"]
        return modifier / 100.0  # Convert to percentage


# ------------------------------
# Simulation Class
# ------------------------------
class Simulation:
    def __init__(self, months, growth_rate, population_size, resources=None):
        self.months = months
        self.growth_rate = growth_rate
        self.population_size = population_size
        self.resources = resources if resources else {"farms": 1, "waterpumps": 1, "mines": 1}
        self.factory = Factory(self.resources)
        self.population = create_population(population_size)
        self.event_manager = EventManager()

        # Tracking lists
        self.profit_history = []  # Total profit (revenue - costs)
        self.revenue_history = []
        self.popularity_history = []
        self.storage_history = []
        self.production_history = []
        self.sold_history = []
        self.monthly_events = []  # Track events per month
        self.monthly_profit_history = []  # Track monthly profit (not cumulative)
        self.production_costs_history = []  # Track production costs
        self.resource_costs_history = []  # Track resource maintenance costs
        self.total_expenses_history = []  # Track total expenses (production + resource costs)

    def run(self):
        base_popularity = 1.0
        cumulative_profit = 0.0  # Track cumulative profit across all months
        for month in range(self.months):
            # Update event manager
            self.event_manager.update_events()
            
            # Try to trigger a random event
            new_event = self.event_manager.trigger_random_event(chance=0.15, current_month=month)
            month_events = []
            if new_event:
                month_events.append(new_event)
            
            # Get event modifiers
            popularity_mod = self.event_manager.get_popularity_modifier()
            production_mod = self.event_manager.get_production_modifier()
            market_mod = self.event_manager.get_market_modifier()
            
            # Apply popularity modifier to base popularity
            adjusted_popularity = base_popularity * (1.0 + popularity_mod)
            
            # Simulate market with adjusted popularity
            total_sales, total_revenue, popularity, store_sales = simulate_market(
                self.population, soda_price=1.25, base_popularity=adjusted_popularity
            )
            
            # Apply market modifier to sales (affects demand)
            if market_mod != 0:
                total_sales = int(total_sales * (1.0 + market_mod))
                total_revenue = total_revenue * (1.0 + market_mod)
            
            # Produce soda with production modifier
            produced = self.factory.produce_soda(self.growth_rate, production_mod)
            available = max(0, produced + self.factory.soda_stored)  # Ensure available is never negative

            # Cap sales by available soda and adjust revenue proportionally
            original_sales = total_sales
            total_sales = min(total_sales, available)
            total_sales = max(0, total_sales)  # Ensure sold is never negative
            if original_sales > 0:
                total_revenue = total_revenue * (total_sales / original_sales)
            total_revenue = max(0, total_revenue)  # Ensure revenue is never negative

            # Calculate production costs (realistic cost structure)
            # Cost per can includes: ingredients, bottling, packaging
            # Reduced cost due to economies of scale with 10x production efficiency
            cost_per_can = 0.25  # Lower cost per can due to batch production efficiency
            production_costs = total_sales * cost_per_can  # Only cost for sold cans
            
            # Calculate resource maintenance costs (scaled to be profitable at reasonable scale)
            # These represent labor, utilities, maintenance for each facility
            # Costs are lower to allow profitability with smaller customer bases
            farm_cost = self.resources["farms"] * 40  # $40 per farm per month (labor, land, equipment)
            waterpump_cost = self.resources["waterpumps"] * 25  # $25 per waterpump per month (utilities, maintenance)
            mine_cost = self.resources["mines"] * 35  # $35 per mine per month (labor, equipment, processing)
            resource_costs = farm_cost + waterpump_cost + mine_cost
            
            # Calculate monthly profit (revenue - production costs - resource costs)
            monthly_profit = total_revenue - production_costs - resource_costs
            # Allow negative profit (losses) - no max(0) constraint
            
            # Add monthly profit to cumulative total
            cumulative_profit += monthly_profit
            
            # Track monthly costs
            total_expenses = production_costs + resource_costs
            self.production_costs_history.append(production_costs)
            self.resource_costs_history.append(resource_costs)
            self.total_expenses_history.append(total_expenses)
            self.monthly_profit_history.append(monthly_profit)

            # Update storage
            if total_sales > produced:
                self.factory.soda_stored -= (total_sales - produced)
                self.factory.soda_produced = 0
            else:
                self.factory.soda_stored += produced - total_sales
            self.factory.soda_stored = max(0, self.factory.soda_stored)  # Ensure storage is never negative

            # Record data
            self.profit_history.append(cumulative_profit)  # Cumulative profit (adds up year to year)
            self.revenue_history.append(total_revenue)
            self.popularity_history.append(popularity)
            self.storage_history.append(self.factory.soda_stored)
            self.production_history.append(produced)
            self.sold_history.append(total_sales)  # Sold = quantity of sodas
            self.monthly_events.append(month_events)

            # Apply popularity depreciation of 0.05 per month
            base_popularity = max(0.0, popularity - 0.05)

        # Return the last store_sales list
        return store_sales


# ------------------------------

# Helper function to format month as Year/Month
def format_year_month(month_num):
    """Convert month number (1-based) to Year/Month format."""
    year = ((month_num - 1) // 12) + 1
    month = ((month_num - 1) % 12) + 1
    return f"Year {year}, Month {month}"


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Soda Factory Simulation", layout="wide")
st.title("🥤 Soda Factory Simulation Dashboard")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Simulation Settings")
    years = st.slider("Years to simulate", 1, 10, 1)
    months = years * 12  # Convert years to months for simulation
    growth_rate = st.number_input("Monthly Growth Rate", value=0.05, step=0.01)
    size_button = st.number_input("Population size", value=50, step=1, min_value=1)
    
    st.header("Resources")
    st.write("Adjust the number of production facilities:")
    st.caption("💡 Operating costs: Farm $40/mo, Water Pump $25/mo, Mine $35/mo")
    farms = st.number_input("Farms", min_value=0, value=1, step=1, help="Produces sugar - $40/month operating cost")
    waterpumps = st.number_input("Water Pumps", min_value=0, value=1, step=1, help="Produces water - $25/month operating cost")
    mines = st.number_input("Mines", min_value=0, value=1, step=1, help="Produces glass - $35/month operating cost")
    
    resources = {"farms": farms, "waterpumps": waterpumps, "mines": mines}
    
    run_button = st.button("Run Simulation")

# --- Run simulation only when user clicks ---
if run_button:
    sim = Simulation(months=months, growth_rate=growth_rate, population_size=int(size_button), resources=resources)
    store_sales = sim.run()

    # Convert simulation data to a simple DataFrame for display
    import pandas as pd

    # Create Year/Month labels
    year_month_labels = [format_year_month(m) for m in range(1, months + 1)]

    df = pd.DataFrame({
        "Year/Month": year_month_labels,
        "Total Profit": sim.profit_history,
        "Monthly Profit": sim.monthly_profit_history,
        "Revenue": sim.revenue_history,
        "Total Expenses": sim.total_expenses_history,
        "Production Costs": sim.production_costs_history,
        "Resource Costs": sim.resource_costs_history,
        "Popularity": sim.popularity_history,
        "Storage": sim.storage_history,
        "Production": sim.production_history,
        "Sold": sim.sold_history,
    })

    st.session_state["df"] = df
    st.session_state["store_sales"] = store_sales
    st.session_state["sim"] = sim
    st.session_state["months"] = months

# --- Display results ---
if "df" in st.session_state:
    df = st.session_state["df"]

    # Key Metrics Summary
    if "sim" in st.session_state:
        sim = st.session_state["sim"]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            final_profit = sim.profit_history[-1] if sim.profit_history else 0
            st.metric("Total Profit", f"${final_profit:,.2f}")
        
        with col2:
            avg_monthly_profit = sum(sim.monthly_profit_history) / len(sim.monthly_profit_history) if sim.monthly_profit_history else 0
            st.metric("Avg Monthly Profit", f"${avg_monthly_profit:,.2f}")
        
        with col3:
            best_month_idx = sim.monthly_profit_history.index(max(sim.monthly_profit_history)) if sim.monthly_profit_history else 0
            best_month_profit = max(sim.monthly_profit_history) if sim.monthly_profit_history else 0
            st.metric("Best Month", f"${best_month_profit:,.2f}", 
                     delta=format_year_month(best_month_idx + 1) if sim.monthly_profit_history else "")
        
        with col4:
            total_revenue_sum = sum(sim.revenue_history)
            st.metric("Total Revenue", f"${total_revenue_sum:,.2f}")
    
    st.subheader("📊 Simulation Data")
    st.dataframe(df, use_container_width=True, height=300)
    
    # Display events that occurred
    if "sim" in st.session_state and st.session_state["sim"].event_manager.event_history:
        st.subheader("📅 Events That Occurred")
        events_df = []
        for event, month_num in st.session_state["sim"].event_manager.event_history:
            events_df.append({
                "Year/Month": format_year_month(month_num),
                "Event": event["Name"],
                "Effect": f"{event['Effect']:+d}%",
                "Duration": f"{event['Time']} months",
                "Type": event["Classification"],
                "Description": event["Text"]
            })
        if events_df:
            import pandas as pd
            events_display = pd.DataFrame(events_df)
            st.dataframe(events_display, use_container_width=True, height=200)

    st.subheader("📈 Graphs")
    graph_options = st.multiselect(
        "Select data to display on chart (can select multiple to overlay):",
        options=["Production", "Revenue", "Storage", "Total Profit", "Monthly Profit", 
                "Total Expenses", "Production Costs", "Resource Costs", "Popularity", "Sold"],
        default=["Total Profit"]  # Default to "Total Profit"
    )

    if graph_options:
        # Create a chart with selected metrics overlaid
        chart_data = df.set_index("Year/Month")[graph_options]
        st.line_chart(chart_data, height=400, use_container_width=True)
    else:
        st.info("Select at least one metric to display on the chart.")

    if "store_sales" in st.session_state:
        data = st.session_state["store_sales"]
        labels = [d["store"] for d in data]
        values = [d["sales"] for d in data]
        colors = ['#3c4da6', '#092142', '#275b66', '#a63c46','#092f42']

        st.subheader("Store Sales Breakdown")
        fig, ax = plt.subplots(figsize=(5, 5))

        patches, texts, autotexts = ax.pie(values, labels=labels,colors=colors, autopct="%1.1f%%", startangle=0)
        autotexts.extend(texts)
        for autotext in autotexts:
            autotext.set_color('white')  # Set the color to white
            autotext.set_fontsize(10)
        fig.set_facecolor('none')
        ax.set_facecolor('none')
        ax.axis("equal")
        st.pyplot(fig)
    
    # Export functionality
    st.subheader("💾 Export Data")
    csv = df.to_csv(index=False)
    if "months" in st.session_state:
        years_export = st.session_state["months"] // 12
        st.download_button(
            label="Download simulation data as CSV",
            data=csv,
            file_name=f"soda_simulation_{years_export}years.csv",
            mime="text/csv"
        )
    else:
        st.download_button(
            label="Download simulation data as CSV",
            data=csv,
            file_name="soda_simulation.csv",
            mime="text/csv"
        )


else:
    st.info("Adjust the parameters and click **Run Simulation** to begin.")

