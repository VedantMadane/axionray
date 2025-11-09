import plotly.graph_objects as go
import pandas as pd

# Data from the provided JSON
data = [
    {"Product_Category": "APPL", "Average_Cost": 685.98, "Count": 43, "Min_Cost": -3000.0, "Max_Cost": 28636.33},
    {"Product_Category": "SPRAYS", "Average_Cost": 210.55, "Count": 415, "Min_Cost": -750.0, "Max_Cost": 15887.02},
    {"Product_Category": "FLOATE", "Average_Cost": 131.58, "Count": 10, "Min_Cost": 8.96, "Max_Cost": 614.57},
    {"Product_Category": "BALER", "Average_Cost": 55.20, "Count": 24, "Min_Cost": 0.52, "Max_Cost": 152.0},
    {"Product_Category": "TRACT2", "Average_Cost": 38.28, "Count": 8, "Min_Cost": 0.0, "Max_Cost": 79.98}
]

# Convert to DataFrame and sort by average cost
df = pd.DataFrame(data)
df = df.sort_values('Average_Cost', ascending=True)

# Define colors from the brand palette
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df['Average_Cost'],
    y=df['Product_Category'],
    orientation='h',
    marker_color=colors[:len(df)],
    text=[f'{count} repairs' for count in df['Count']],
    textposition='outside',
    textfont=dict(color='black', size=11),
    hovertemplate='<b>%{y}</b><br>Avg Cost: $%{x:.2f}<br>Repairs: %{text}<extra></extra>'
))

# Update layout
fig.update_layout(
    title='Repair Cost Analysis by Category',
    xaxis_title='Avg Cost ($)',
    yaxis_title='Category',
    showlegend=False
)

# Update traces for styling
fig.update_traces(cliponaxis=False)

# Update axes formatting
fig.update_xaxes(tickformat='$,.0f')

# Save the chart
fig.write_image('outputs/figures/repair_costs_chart.png')