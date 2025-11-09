import plotly.express as px
import pandas as pd

# Data
data = [
    {"Symptom": "MATERIAL_DEGRADATION", "Count": 28},
    {"Symptom": "HEATING_RELATED", "Count": 24},
    {"Symptom": "FUNCTIONAL_FAILURE", "Count": 17},
    {"Symptom": "DRIVER_ASSISTANCE", "Count": 9},
    {"Symptom": "WARNING_SYSTEM", "Count": 9},
    {"Symptom": "NOISE_ISSUE", "Count": 4}
]

df = pd.DataFrame(data)

# Abbreviate symptom names to fit 15 character limit
symptom_mapping = {
    "MATERIAL_DEGRADATION": "Material Degrd",
    "HEATING_RELATED": "Heating Related",
    "FUNCTIONAL_FAILURE": "Functional Fail",
    "DRIVER_ASSISTANCE": "Driver Assist", 
    "WARNING_SYSTEM": "Warning System",
    "NOISE_ISSUE": "Noise Issue"
}

df['Symptom_Short'] = df['Symptom'].map(symptom_mapping)

# Sort by count for better visualization
df = df.sort_values('Count', ascending=True)

# Create custom color scale using brand colors
brand_colorscale = [
    [0.0, '#B4413C'],
    [0.2, '#D2BA4C'], 
    [0.4, '#5D878F'],
    [0.6, '#2E8B57'],
    [0.8, '#DB4545'],
    [1.0, '#1FB8CD']
]

# Create horizontal bar chart
fig = px.bar(df, 
             x='Count', 
             y='Symptom_Short', 
             orientation='h',
             color='Count',
             color_continuous_scale=brand_colorscale,
             title='Customer Failure Symptoms Analysis')

# Update traces
fig.update_traces(cliponaxis=False)

# Update layout
fig.update_layout(
    xaxis_title='Count',
    yaxis_title='Symptoms'
)

# Save the chart
fig.write_image('outputs/figures/failure_symptoms_chart.png')
