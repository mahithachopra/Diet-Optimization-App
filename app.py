import streamlit as st
import pulp
import pandas as pd
import matplotlib.pyplot as plt

st.title("🍱 Diet Optimization App")
st.markdown("Minimize diet cost while meeting your daily nutritional needs.")

# Food data
foods = ["Oats", "Milk", "Eggs", "Bread", "PeanutB"]
cost = {"Oats": 20, "Milk": 15, "Eggs": 10, "Bread": 12, "PeanutB": 25}
protein = {"Oats": 5, "Milk": 8, "Eggs": 6, "Bread": 4, "PeanutB": 7}
carbs = {"Oats": 30, "Milk": 20, "Eggs": 1, "Bread": 40, "PeanutB": 15}
fat = {"Oats": 2, "Milk": 5, "Eggs": 5, "Bread": 1, "PeanutB": 15}

# Nutritional ranges from user
st.sidebar.header("Set Nutritional Requirements (grams)")
min_protein = st.sidebar.slider("Min Protein", 0, 150, 50)
max_protein = st.sidebar.slider("Max Protein", min_protein, 200, 100)
min_carbs = st.sidebar.slider("Min Carbs", 0, 300, 130)
max_carbs = st.sidebar.slider("Max Carbs", min_carbs, 400, 250)
min_fat = st.sidebar.slider("Min Fat", 0, 100, 30)
max_fat = st.sidebar.slider("Max Fat", min_fat, 150, 70)

# Create the model
model = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)
food_vars = pulp.LpVariable.dicts("Units", foods, lowBound=0, cat='Continuous')

# Objective: minimize cost
model += pulp.lpSum([cost[i] * food_vars[i] for i in foods]), "Total_Cost"

# Constraints
model += pulp.lpSum([protein[i] * food_vars[i] for i in foods]) >= min_protein
model += pulp.lpSum([protein[i] * food_vars[i] for i in foods]) <= max_protein
model += pulp.lpSum([carbs[i] * food_vars[i] for i in foods]) >= min_carbs
model += pulp.lpSum([carbs[i] * food_vars[i] for i in foods]) <= max_carbs
model += pulp.lpSum([fat[i] * food_vars[i] for i in foods]) >= min_fat
model += pulp.lpSum([fat[i] * food_vars[i] for i in foods]) <= max_fat

# Solve
model.solve()

if pulp.LpStatus[model.status] == "Optimal":
    st.success("✅ Optimal Diet Plan Found!")

    # Display results
    results = {f: food_vars[f].varValue for f in foods}
    df = pd.DataFrame.from_dict(results, orient='index', columns=["Units"])
    df["Cost (₹)"] = df.index.map(cost)
    df["Total Cost"] = df["Units"] * df["Cost (₹)"]
    st.dataframe(df.style.format(subset=["Units", "Total Cost"], precision=2))

    st.metric("Minimum Total Cost", f"₹{pulp.value(model.objective):.2f}")

    # Bar chart
    st.subheader("📊 Food Quantity Chart")
    st.bar_chart(df["Units"])
else:
    st.error("❌ No feasible solution found. Try adjusting the sliders.")
