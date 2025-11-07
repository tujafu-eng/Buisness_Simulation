import random

def Water_prod(resources):
    water = 0
    for _ in range(resources["waterpumps"]):
        water += random.randint(30, 60)  # Increased by 10 (was 20-50, now 30-60)
    return water

def Sugar_prod(resources):
    sugar_cane = 0
    for _ in range(resources["farms"]):
        sugar_cane += random.randint(30, 60)  # Increased by 10 (was 20-50, now 30-60)
    sugar = sugar_cane // 2  # 2 sugarcane = 1 sugar
    return sugar

def Glass_prod(resources):
    sand = 0
    for _ in range(resources["mines"]):
        sand += random.randint(30, 60)  # Increased by 10 (was 20-50, now 30-60)
    glass = sand // 3  # 3 sand = 1 glass
    return glass
