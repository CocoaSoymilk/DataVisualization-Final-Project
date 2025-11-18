# 🚗 Seoul Traffic Accident Analysis Dashboard

An interactive web-based dashboard for visualizing and analyzing traffic accident data across 25 districts in Seoul, South Korea.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.14+-green.svg)
![Plotly](https://img.shields.io/badge/plotly-5.18+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Source](#data-source)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project is a **Data Visualization Final Project** that provides comprehensive analysis of traffic accidents in Seoul from 2009 to 2024. The dashboard offers interactive visualizations including choropleth maps, time-series trends, weather condition analysis, vehicle type distribution, and heatmaps.

**Key Objectives:**
- Identify traffic accident hotspots across Seoul districts
- Analyze temporal trends and patterns
- Understand the impact of weather conditions on accidents
- Examine vehicle type distributions in accidents
- Provide actionable insights through data visualization

## ✨ Features

### 🎛️ Interactive Filters
- **Year Range Selector**: Analyze specific time periods using an intuitive slider
- **District Selection**: Focus on particular districts or view all 25 districts
- **Weather Conditions**: Filter by weather (Clear, Cloudy, Rain, Fog, Snow, Other)
- **Map Metrics**: Toggle between casualties, fatalities, and accident counts

### 📊 Visualizations

1. **Choropleth Map** 🗺️
   - Geographic distribution of accidents across Seoul districts
   - Color-coded intensity based on selected metric
   - Interactive hover information with detailed statistics

2. **TOP 10 Ranking** 🏆
   - Horizontal bar chart showing accident hotspots
   - Sorted by total casualties in selected period
   - Quick identification of high-risk areas

3. **Yearly Trend Analysis** 📈
   - Time-series line chart tracking accident patterns
   - Multi-line comparison for different metrics
   - Trend identification over 15+ years of data

4. **Weather Condition Analysis** 🌤️
   - Grouped bar chart comparing accidents by weather
   - Side-by-side comparison of fatalities vs injuries
   - Insights into weather-related risk factors

5. **Vehicle Type Distribution** 🚙
   - Interactive pie chart showing accident breakdown by vehicle purpose
   - Percentage-based visualization for easy comparison
   - Categories include passenger cars, commercial vehicles, motorcycles, etc.

6. **Heatmap Matrix** 🔥
   - 2D visualization of district × year accident density
   - Color gradient representing accident intensity
   - Pattern recognition across time and location

### 📈 Statistical Cards
- **Total Accidents**: Aggregate count of incidents
- **Total Fatalities**: Cumulative death toll
- **Total Injuries**: Total number of people injured
- **Analysis Period**: Date range of current view

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.8+ |
| **Framework** | Plotly Dash 2.14+ |
| **Data Processing** | Pandas 2.1+ |
| **Visualization** | Plotly Express 5.18+ |
| **UI Components** | Dash Bootstrap Components |
| **Styling** | CSS3, Custom Dark Theme |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

**Option 1: Automated Installation (Windows)**
```bash
# Double-click the batch file
install_and_run.bat
```

**Option 2: Manual Installation**

1. Clone the repository:
```bash
git clone https://github.com/CocoaSoymilk/Seoul-Traffic-Accident-Dashboard.git
cd Seoul-Traffic-Accident-Dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:8050
```

## 📦 Dependencies

```txt
pandas==2.1.3
plotly==5.18.0
dash==2.14.2
dash-bootstrap-components==1.5.0
numpy==1.26.2
requests==2.31.0
```

## 🚀 Usage

1. **Launch the Dashboard**
   - Run `python app.py` or use the batch file
   - Wait for the "Dash is running on http://127.0.0.1:8050/" message

2. **Interact with Filters**
   - Use the year range slider to focus on specific periods
   - Select districts from the dropdown menu
   - Choose weather conditions to filter data
   - Toggle map metrics to change the choropleth visualization

3. **Analyze Data**
   - Hover over charts for detailed information
   - Identify trends and patterns across different visualizations
   - Compare multiple districts or time periods

4. **Export Insights**
   - Take screenshots of visualizations
   - Use browser developer tools to export chart data

## 📁 Project Structure

```
Seoul-Traffic-Accident-Dashboard/
├── app.py                          # Main Dash application
├── charts.py                       # Chart generation functions
├── preprocessing.py                # Data loading and cleaning
├── requirements.txt                # Python dependencies
├── README_EN.md                    # English documentation
├── README.md                       # Korean documentation
├── DATA/                           # Data directory
│   ├── 교통사고+현황(구별)_*.csv        # District-level data
│   ├── 기상상태별+교통사고+현황_*.csv     # Weather condition data
│   └── 차량용도별+교통사고+현황_*.csv     # Vehicle type data
├── start_dashboard.bat             # Quick launch script
└── install_and_run.bat             # Installation & launch script
```

### Module Descriptions

**`app.py`**
- Initializes the Dash application
- Defines the dashboard layout with Bootstrap components
- Implements callback functions for interactivity
- Manages state and user inputs

**`charts.py`**
- `create_map_chart()`: Generates choropleth map of Seoul
- `create_trend_chart()`: Creates time-series line charts
- `create_weather_chart()`: Produces weather analysis bar charts
- `create_vehicle_chart()`: Builds vehicle type pie charts
- `create_heatmap_chart()`: Constructs district-year heatmaps
- `create_ranking_chart()`: Generates TOP 10 ranking charts

**`preprocessing.py`**
- `load_and_clean_data()`: Main data loading orchestrator
- `load_district_data()`: Processes district-level CSV files
- `load_weather_data()`: Handles weather condition data
- `load_vehicle_data()`: Manages vehicle type data
- Data cleaning, type conversion, and validation

## 📊 Data Source

- **Source**: Seoul Open Data Plaza (서울 열린데이터광장)
- **Period**: 2009 - 2024 (15+ years)
- **Coverage**: All 25 districts of Seoul
- **Metrics**: 
  - Accident counts
  - Fatalities
  - Injuries (minor and serious)
  - Weather conditions
  - Vehicle types
  - Temporal information (year, month)

**Districts Included:**
Gangnam, Gangdong, Gangbuk, Gangseo, Gwanak, Gwangjin, Guro, Geumcheon, Nowon, Dobong, Dongdaemun, Dongjak, Mapo, Seodaemun, Seocho, Seongdong, Seongbuk, Songpa, Yangcheon, Yeongdeungpo, Yongsan, Eunpyeong, Jongno, Jung, Jungnang

## 🎨 Design Features

### Responsive Layout
- Mobile-first design approach
- Breakpoint-based layout adjustments
- Optimized for desktop, tablet, and mobile devices

### User Experience
- Real-time chart updates based on filter selections
- Smooth transitions and animations
- Intuitive navigation and controls
- Accessible color schemes (WCAG AA compliant)

### Visual Design
- Modern dark theme (CYBORG Bootstrap theme)
- Consistent color palette
- Professional typography
- Font Awesome icons for visual clarity

## 📸 Screenshots

*Screenshots will be added upon project deployment*

### Dashboard Overview
![Full Dashboard](docs/screenshot_overview.png)

### Interactive Map View
![Map Visualization](docs/screenshot_map.png)

### Detailed Analytics
![Charts and Analysis](docs/screenshot_charts.png)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guidelines for Python code
- Add docstrings to new functions
- Update README if adding new features
- Test your changes locally before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**CocoaSoymilk**
- GitHub: [@CocoaSoymilk](https://github.com/CocoaSoymilk)
- Project: Data Visualization Final Project

## 🙏 Acknowledgments

- **Seoul Open Data Plaza** - For providing comprehensive traffic accident datasets
- **Plotly Community** - For excellent visualization tools and documentation
- **Dash Framework** - For the powerful web application framework
- **Bootstrap** - For responsive UI components

## 📞 Contact

For questions, suggestions, or feedback, please open an issue on GitHub.

## 🔗 Links

- [Seoul Open Data Plaza](https://data.seoul.go.kr/)
- [Plotly Documentation](https://plotly.com/python/)
- [Dash Documentation](https://dash.plotly.com/)

---

⭐ **If you find this project helpful, please consider giving it a star!**

---

**Project Type**: Academic - Data Visualization Final Project  
**Institution**: [Your University Name]  
**Course**: Data Visualization / Data Science  
**Year**: 2024-2025

