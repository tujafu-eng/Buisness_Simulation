import random

class Agent:
    def __init__(self, name):
        self.name = name
        self.create_customer()
        self.buy_chance = 0
        self.bought = False
        self.purchase_amount = 0

    def create_customer(self):
        """Assign randomized customer attributes."""
        locations = [f"Store {i}" for i in range(1, 6)]
        self.base = random.randint(80, 100)
        self.age = random.randint(18, 70)
        self.salary = random.randint(5000, 12000)
        self.influence = random.uniform(0, 1)
        self.location = random.choice(locations)
        self.health = random.randint(50, 100)
        self.alternative_pull = random.uniform(0, 1)
        self.festivity = random.uniform(0, 1)


def create_population(size: int):
    """Create a list of agents representing customers."""
    return [Agent(f"Customer_{i+1}") for i in range(size)]


def simulate_market(population, soda_price=3.25, base_popularity=1.0):
    """
    Simulate soda sales across all agents and store locations.

    Returns:
        total_sales (int)
        total_revenue (float)
        popularity (float)
        store_sales_list (list of dict)
    """
    total_sales = 0
    total_revenue = 0
    store_sales = {f"Store {i}": 0 for i in range(1, 6)}
    popularity = base_popularity

    for agent in population:
        # --- Buying probability logic ---
        agent.buy_chance = agent.base / 100

        # Age influence
        if 18 <= agent.age <= 28:
            agent.buy_chance += 0.03
        elif agent.age >= 70:
            agent.buy_chance -= 0.03

        # Salary influence
        if agent.salary < 7000:
            agent.buy_chance += 0.10
        elif agent.salary < 10000:
            agent.buy_chance += 0.07
        else:
            agent.buy_chance += 0.04

        # Health influence
        if agent.health >= 90:
            agent.buy_chance -= 0.05
        elif 50 <= agent.health < 89:
            agent.buy_chance += 0.03

        # Festivity and alternatives
        if agent.festivity >= 0.8:
            agent.buy_chance += 0.10
        if agent.alternative_pull >= 0.7:
            agent.buy_chance -= 0.15

        # Clamp between 0 and 1
        agent.buy_chance = max(0.0, min(agent.buy_chance, 1.0))

        # --- Purchase decision ---
        if random.random() <= agent.buy_chance:
            agent.bought = True
            cans_bought = 6
            total_sales += cans_bought
            total_revenue += soda_price * cans_bought
            store_sales[agent.location] += cans_bought

            # Influential boost
            if agent.influence >= 0.7:
                popularity += 0.02
        else:
            agent.bought = False

    # --- Store performance effects ---
    best_store = max(store_sales, key=store_sales.get)
    if store_sales[best_store] > (len(population) * 3):
        popularity += 0.03

    # Convert to list format for charts
    store_sales_list = [{"store": k, "sales": v} for k, v in store_sales.items()]

    return total_sales, total_revenue, popularity, store_sales_list
