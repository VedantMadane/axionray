# AxionRay Data Analysis

This folder contains data analysis scripts for the AxionRay assignment, focusing on vehicle defect and repair analysis.

## Project Structure

```
data/
├── raw/               # Original Excel data files
└── processed/         # Processed CSV files

src/
├── task1/            # Scripts for Task 1 analysis
├── task2/            # Scripts for Task 2 analysis
└── charts/           # Chart generation scripts

outputs/
├── figures/          # Generated charts and visualizations
└── reports/          # Generated reports and findings
```

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Place your Excel data files in the `data/raw/` directory.

3. Run the main analysis script:
   ```
   python axionray_complete_analysis.py
   ```

## Usage

- `axionray_complete_analysis.py`: Main script that runs the complete analysis pipeline
- Individual task scripts are organized in their respective directories under `src/`
- Generated outputs are saved in the `outputs/` directory
