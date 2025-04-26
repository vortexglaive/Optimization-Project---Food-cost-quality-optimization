import pandas as pd
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('Indian_Food_Nutrition_Processed.csv')
data = data.dropna()

# Assign random price (mean ~ uniform(10,100), std dev = 10% of mean)
data['MeanPrice'] = np.random.uniform(10, 100, size=len(data))
data['StdPrice'] = 0.1 * data['MeanPrice']

# Nutritional constraints (per day)
req_protein = 50
req_carb = 130
req_fat = 20
req_fiber = 25

# Objective: minimize total cost
c = data['MeanPrice'].values

# Constraints matrix
A = [
    -data['Protein (g)'].values,
    -data['Carbohydrates (g)'].values,
    -data['Fats (g)'].values,
    -data['Fibre (g)'].values
]
b = [-req_protein, -req_carb, -req_fat, -req_fiber]

# Bounds for each food (non-negative quantities)
bounds = [(0, None) for _ in range(len(data))]

# Solve linear program
result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

if result.success:
    print(f"Minimum cost: INR {result.fun:.2f}")
else:
    print("Optimization failed.")

# Plotting
'''
plt.hist(data['Protein (g)'], bins=30)
plt.title('Histogram of Protein Content')
plt.xlabel('Protein (g) per 100g')
plt.ylabel('Frequency')
plt.show()'''

plt.boxplot(data['MeanPrice'])
plt.title('Boxplot of Food Prices')
plt.ylabel('Price (INR per 100g)')
plt.show()
