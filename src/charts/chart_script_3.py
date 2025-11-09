import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"Year": "2022", "Metric": "Total Cost ($)", "Value": 28198.39},
    {"Year": "2022", "Metric": "Total Hours", "Value": 1729.33},
    {"Year": "2023", "Metric": "Total Cost ($)", "Value": 38457.43},
    {"Year": "2023", "Metric": "Total Hours", "Value": 4352.44},
    {"Year": "2024", "Metric": "Total Cost ($)", "Value": 53165.44},
    {"Year": "2024", "Metric": "Total Hours", "Value": 2934.77}
]

df = pd.DataFrame(data)

# Pivot the data to get separate columns for each metric
df_pivot = df.pivot(index='Year', columns='Metric', values='Value')

# Create the grouped bar chart with dual y-axes
fig = go.Figure()

# Add bars for Total Cost (left y-axis)
fig.add_trace(go.Bar(
    name='Cost ($)',
    x=df_pivot.index,
    y=df_pivot['Total Cost ($)'],
    marker_color='#1FB8CD',
    yaxis='y',
    offsetgroup=1
))

# Add bars for Total Hours (right y-axis)
fig.add_trace(go.Bar(
    name='Hours',
    x=df_pivot.index,
    y=df_pivot['Total Hours'],
    marker_color='#DB4545',
    yaxis='y2',
    offsetgroup=2
))

# Update layout with dual y-axes
fig.update_layout(
    title='Yearly Repair Trends: Cost vs Hours',
    xaxis_title='Year',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    yaxis=dict(
        title='Cost ($)',
        side='left',
        tickformat='.2s'
    ),
    yaxis2=dict(
        title='Hours',
        side='right',
        overlaying='y',
        tickformat='.2s'
    )
)

# Update traces
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image('outputs/figures/yearly_repair_trends.png')