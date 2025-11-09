import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Create dataframe from the provided data
data = [
  {"Vehicle_Age": 6, "Total_Cost": 370.03},
  {"Vehicle_Age": 5, "Total_Cost": 307.32},
  {"Vehicle_Age": 9, "Total_Cost": 3205.45},
  {"Vehicle_Age": 10, "Total_Cost": 445.28},
  {"Vehicle_Age": 0, "Total_Cost": 1439.65},
  {"Vehicle_Age": 0, "Total_Cost": 216.75},
  {"Vehicle_Age": 2, "Total_Cost": 1488.94},
  {"Vehicle_Age": 3, "Total_Cost": 427.08},
  {"Vehicle_Age": 21, "Total_Cost": 27.69},
  {"Vehicle_Age": 4, "Total_Cost": 1147.09},
  {"Vehicle_Age": 8, "Total_Cost": 476.16},
  {"Vehicle_Age": 6, "Total_Cost": 509.37},
  {"Vehicle_Age": 0, "Total_Cost": 438.06},
  {"Vehicle_Age": 12, "Total_Cost": 227.20},
  {"Vehicle_Age": 35, "Total_Cost": 519.97},
  {"Vehicle_Age": 0, "Total_Cost": 411.41},
  {"Vehicle_Age": 10, "Total_Cost": 284.04},
  {"Vehicle_Age": 32, "Total_Cost": 445.12},
  {"Vehicle_Age": 3, "Total_Cost": 500.38},
  {"Vehicle_Age": 15, "Total_Cost": 623.41},
  {"Vehicle_Age": 50, "Total_Cost": 1126.84}
]

df = pd.DataFrame(data)

# Create category for high-cost outliers (above $1000)
df['Cost_Category'] = df['Total_Cost'].apply(lambda x: 'High Cost' if x > 1000 else 'Normal Cost')

# Create scatter plot
fig = go.Figure()

# Add scatter points for normal cost
normal_cost = df[df['Cost_Category'] == 'Normal Cost']
fig.add_trace(go.Scatter(
    x=normal_cost['Vehicle_Age'],
    y=normal_cost['Total_Cost'],
    mode='markers',
    name='Normal Cost',
    marker=dict(color='#1FB8CD', size=8),
    hovertemplate='Age: %{x} yrs<br>Cost: $%{y:.0f}<extra></extra>'
))

# Add scatter points for high cost
high_cost = df[df['Cost_Category'] == 'High Cost']
fig.add_trace(go.Scatter(
    x=high_cost['Vehicle_Age'],
    y=high_cost['Total_Cost'],
    mode='markers',
    name='High Cost',
    marker=dict(color='#DB4545', size=8),
    hovertemplate='Age: %{x} yrs<br>Cost: $%{y:.0f}<extra></extra>'
))

# Calculate trend line using numpy polyfit
x = df['Vehicle_Age'].values
y = df['Total_Cost'].values
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

x_trend = np.linspace(df['Vehicle_Age'].min(), df['Vehicle_Age'].max(), 100)
y_trend = p(x_trend)

fig.add_trace(go.Scatter(
    x=x_trend,
    y=y_trend,
    mode='lines',
    name='Trend Line',
    line=dict(color='#2E8B57', width=2, dash='dash'),
    hovertemplate='<extra></extra>'
))

# Update layout
fig.update_layout(
    title="Vehicle Age vs Repair Cost Analysis",
    xaxis_title="Vehicle Age",
    yaxis_title="Repair Cost ($)",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

fig.update_traces(cliponaxis=False)

# Format y-axis to show abbreviated numbers
fig.update_yaxes(tickformat='.0f')

# Save the chart
fig.write_image("vehicle_age_repair_cost_analysis.png")