# YouTube Music Analytics Dashboard
### A Big Data Analysis Mini Project

## Project Overview
This project performs comprehensive big data analysis on YouTube's top songs dataset, featuring **6,327 song records** with detailed statistics including view counts, channel information, duration, and more.

## Features
- **Data Loading & Cleaning**: Automated data preprocessing and cleaning
- **Exploratory Data Analysis (EDA)**: Comprehensive statistical analysis
- **Advanced Visualizations**: 8+ professional charts and graphs
- **Statistical Insights**: Correlation analysis, distribution analysis, and trend identification
- **Automated Reporting**: Generated insights report with key findings

## Technologies Used
- **Python 3.x**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization

## Dataset Information
- **File**: `youtube-top-100-songs-2025.csv`
- **Records**: 6,327 songs
- **Columns**: 13 fields
  - title, fulltitle, description
  - view_count, duration, duration_string
  - channel, channel_url, channel_follower_count
  - categories, tags, live_status, thumbnail

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions
1. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Complete Analysis
Simply execute the main script:
```bash
python youtube_music_analytics.py
```

### What Happens When You Run It
The script will automatically:
1. Load and clean the CSV data
2. Perform exploratory data analysis
3. Generate statistical insights
4. Create 8+ visualizations
5. Generate a comprehensive insights report
6. Save all outputs to `analytics_output/` directory

### Expected Runtime
- Approximately 15-30 seconds (depending on your system)

## Output Files

### Generated Visualizations (PNG)
1. `01_top_15_songs.png` - Bar chart of most viewed songs
2. `02_top_10_channels.png` - Top channels by total views
3. `03_view_distribution.png` - Distribution of video views
4. `04_duration_vs_views.png` - Correlation between duration and views
5. `05_duration_distribution.png` - Song duration distribution
6. `07_popularity_distribution.png` - Pie chart of popularity categories
7. `08_top_channels_by_count.png` - Channels with most songs
8. `09_correlation_heatmap.png` - Correlation matrix visualization

### Generated Reports
- `INSIGHTS_REPORT.txt` - Comprehensive analysis report with key findings

## Key Analysis Features

### 1. Top Performers Analysis
- Identifies top 20 most viewed songs
- Ranks top 10 channels by total views
- Analyzes top channels by song count

### 2. Statistical Analysis
- View count distribution (mean, median, std dev, percentiles)
- Duration analysis and patterns
- Correlation analysis between metrics

### 3. Data Insights
- Popularity categorization (Mega Hits, Popular, Moderate)
- Channel performance metrics
- Duration vs popularity relationship
- Follower count vs view count correlation

### 4. Visualizations
- Professional, high-resolution charts (300 DPI)
- Color-coded for easy interpretation
- Includes trend lines and statistical annotations

## Sample Insights From Analysis

**Dataset Statistics:**
- Total songs: 100 (sample from 6,327)
- Unique channels: 65
- Combined views: 10.59 billion
- Average views per song: 105.9 million

**Top Performers:**
- Most viewed: ROSÉ & Bruno Mars - APT. (2+ billion views)
- Top channel: ROSÉ with 2.24 billion total views

**Key Findings:**
- 2% of songs achieve "mega hit" status (≥1B views)
- Average song duration: 3.40 minutes
- Optimal duration appears to be 3-4 minutes
- Strong correlation between channel size and video performance

## Project Structure
```
BigData2/
├── youtube-top-100-songs-2025.csv    # Dataset (6,327 records)
├── youtube_music_analytics.py        # Main analysis script
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── analytics_output/                 # Generated outputs
    ├── 01_top_15_songs.png
    ├── 02_top_10_channels.png
    ├── 03_view_distribution.png
    ├── 04_duration_vs_views.png
    ├── 05_duration_distribution.png
    ├── 07_popularity_distribution.png
    ├── 08_top_channels_by_count.png
    ├── 09_correlation_heatmap.png
    └── INSIGHTS_REPORT.txt
```

## Code Architecture

### Main Class: `YouTubeMusicAnalytics`
The project uses an object-oriented approach with a main analytics class:

**Methods:**
- `load_and_clean_data()` - Data loading and preprocessing
- `exploratory_data_analysis()` - EDA and top performers
- `statistical_analysis()` - Statistical computations
- `create_visualizations()` - Generate all charts
- `generate_insights_report()` - Create final report
- `run_analysis()` - Execute complete pipeline

## Customization

### Analyzing Different Data
To analyze your own CSV file:
```python
dashboard = YouTubeMusicAnalytics('your_file.csv')
dashboard.run_analysis()
```

### Adjusting Visualization Settings
Modify these parameters in the script:
```python
plt.rcParams['figure.figsize'] = (12, 6)  # Chart size
sample_size = 2000  # Number of points in scatter plots
bins = 50  # Histogram bins
```

## Big Data Concepts Demonstrated

1. **Data Processing**: Handling large datasets with 6,327+ records
2. **ETL Pipeline**: Extract, Transform, Load workflow
3. **Statistical Analysis**: Descriptive statistics and correlations
4. **Data Visualization**: Multiple chart types for insights
5. **Automation**: End-to-end automated analysis pipeline
6. **Scalability**: Modular design for larger datasets

## Troubleshooting

**Issue: ModuleNotFoundError**
```bash
# Solution: Install missing package
pip install [package_name]
```

**Issue: Unicode encoding errors on Windows**
- The script automatically handles Windows encoding issues
- If problems persist, run in UTF-8 mode: `chcp 65001`

**Issue: Memory errors with large dataset**
- Increase Python memory limit
- Process data in chunks using pandas `chunksize` parameter

## Future Enhancements

Potential additions to the project:
- Machine learning prediction models
- Time series analysis if date data available
- Natural Language Processing on titles/descriptions
- Interactive dashboard using Plotly/Dash
- Real-time data ingestion simulation
- PySpark implementation for distributed processing
- Web scraping to update dataset automatically

## Learning Outcomes

This project demonstrates:
- Data analysis with Pandas
- Statistical computing with NumPy
- Data visualization with Matplotlib/Seaborn
- Python OOP principles
- Big data processing techniques
- Automated reporting systems

## Author
Big Data Analysis Project
Date: 2025-10-14

## License
This project is for educational purposes.

---

**Note**: This is a mini project designed to demonstrate big data analysis concepts using real YouTube music data. The dataset contains 6,327 songs with comprehensive metadata.
