import plotly.express as px
import pandas as pd

# Create dataframe from the provided data
data = [
    {"Cost_Severity": "CRITICAL", "Count": 3},
    {"Cost_Severity": "HIGH", "Count": 35},
    {"Cost_Severity": "MEDIUM", "Count": 59},
    {"Cost_Severity": "LOW", "Count": 3}
]

df = pd.DataFrame(data)

# Define color mapping according to instructions
color_map = {
    'CRITICAL': '#DB4545',  # Red
    'HIGH': '#FFA500',      # Orange
    'MEDIUM': '#1FB8CD',    # Blue (using brand cyan)
    'LOW': '#2E8B57'        # Green
}

# Create the bar chart with specific color mapping
fig = px.bar(df, x='Cost_Severity', y='Count', 
             title='Repair Cost Severity Distribution',
             color='Cost_Severity',
             color_discrete_map=color_map)

# Update traces
fig.update_traces(cliponaxis=False)

# Update layout with axis titles
fig.update_xaxes(title='Cost Severity')
fig.update_yaxes(title='Cases')

# Center legend under title (4 items, fewer than 5)
fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5))

# Save the chart
fig.write_image('outputs/figures/repair_cost_severity_chart.png')
fig.show()