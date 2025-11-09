import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Create dataframe from the provided data
data = [
    {"Actual_Hours": 1.0, "Cost_Numeric": 145.60, "Failed_Component": "Sensor"},
    {"Actual_Hours": 6.38, "Cost_Numeric": 96.20, "Failed_Component": "Cab, Not Achieving"},
    {"Actual_Hours": 6.38, "Cost_Numeric": 5.51, "Failed_Component": "Not Mentioned"},
    {"Actual_Hours": 3.9, "Cost_Numeric": 0.00, "Failed_Component": "Not Mentioned"},
    {"Actual_Hours": 3.68, "Cost_Numeric": -40.00, "Failed_Component": "Suspension, Unavailable"},
    {"Actual_Hours": 19.40, "Cost_Numeric": 0.00, "Failed_Component": "Light, Out"},
    {"Actual_Hours": 2.55, "Cost_Numeric": 0.00, "Failed_Component": "Machine, Blocked"},
    {"Actual_Hours": 10.02, "Cost_Numeric": -100.0, "Failed_Component": "Mast"},
    {"Actual_Hours": 16.4, "Cost_Numeric": 89.45, "Failed_Component": "Not Mentioned"},
    {"Actual_Hours": 29.83, "Cost_Numeric": 0.00, "Failed_Component": "Harness"},
    {"Actual_Hours": 13.0, "Cost_Numeric": 250.00, "Failed_Component": "Boom"},
    {"Actual_Hours": 8.5, "Cost_Numeric": 175.50, "Failed_Component": "Machine"},
    {"Actual_Hours": 5.2, "Cost_Numeric": 95.30, "Failed_Component": "Steering"},
    {"Actual_Hours": 12.1, "Cost_Numeric": 210.75, "Failed_Component": "Air Conditioner"},
    {"Actual_Hours": 7.8, "Cost_Numeric": 125.40, "Failed_Component": "Hose"}
]

df = pd.DataFrame(data)

# Count component frequency to find top 5
component_counts = df['Failed_Component'].value_counts()

# Get top 5 most common components
top_5_components = component_counts.head(5).index.tolist()

# Filter data to top 5 components only
df_filtered = df[df['Failed_Component'].isin(top_5_components)].copy()

# Shorten component names to fit 15 character limit
component_mapping = {
    'Not Mentioned': 'Not Mentioned',
    'Cab, Not Achieving': 'Cab Issue',
    'Suspension, Unavailable': 'Suspension',
    'Light, Out': 'Light',
    'Sensor': 'Sensor'
}

df_filtered['Component'] = df_filtered['Failed_Component'].map(component_mapping)

# Define colors for the 5 components
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Create scatter plot
fig = px.scatter(df_filtered, 
                x='Actual_Hours', 
                y='Cost_Numeric',
                color='Component',
                title='Repair Cost vs Hours by Component',
                labels={'Actual_Hours': 'Hours', 'Cost_Numeric': 'Cost ($)'},
                color_discrete_sequence=colors)

# Increase marker size for better visibility and update traces
fig.update_traces(marker_size=12, cliponaxis=False)

# Add trend line for overall correlation using all filtered data
x_vals = df_filtered['Actual_Hours'].values
y_vals = df_filtered['Cost_Numeric'].values

# Calculate trend line
if len(x_vals) > 1:
    z = np.polyfit(x_vals, y_vals, 1)
    p = np.poly1d(z)
    
    # Create trend line points
    x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_trend = p(x_trend)
    
    # Add trend line without showing in legend
    fig.add_trace(go.Scatter(x=x_trend, y=y_trend, 
                            mode='lines',
                            name='Trend Line',
                            line=dict(color='black', dash='dash', width=2),
                            showlegend=False))

# Update axis ranges to ensure all points are visible with some padding
x_range = df_filtered['Actual_Hours'].max() - df_filtered['Actual_Hours'].min()
y_range = df_filtered['Cost_Numeric'].max() - df_filtered['Cost_Numeric'].min()

x_margin = max(x_range * 0.1, 1)  # At least 1 hour margin
y_margin = max(y_range * 0.1, 10)  # At least $10 margin

fig.update_xaxes(range=[df_filtered['Actual_Hours'].min() - x_margin, 
                       df_filtered['Actual_Hours'].max() + x_margin])
fig.update_yaxes(range=[df_filtered['Cost_Numeric'].min() - y_margin, 
                       df_filtered['Cost_Numeric'].max() + y_margin])

# Since we have 5 legend items, center the legend horizontally
fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5))

# Save the chart
fig.write_image('outputs/figures/repair_cost_scatter.png')