# CultureVista Explorer 🏛️

A data-driven web application dedicated to promoting India's rich cultural heritage by showcasing traditional art forms, unexplored cultural experiences, and regional diversity.

## 🌟 Overview

CultureVista is an innovative platform that leverages open government datasets and tourism trends to identify hidden cultural gems, endangered art forms, and seasonality patterns across Indian states. Our mission is to educate travelers, support local artisans, and drive cultural preservation through data-driven insights.

## ✨ Features

- **Interactive Visualizations**: Explore cultural data through dynamic charts and maps
- **Cultural Storytelling**: Discover rich narratives behind traditional art forms and practices
- **Hidden Gems Discovery**: Uncover unexplored cultural experiences across regions
- **Endangered Arts Tracking**: Identify and highlight art forms that need preservation
- **Seasonality Insights**: Understand the best times to experience different cultural events
- **Responsible Tourism Tips**: Promote sustainable and respectful cultural tourism
- **Regional Diversity Showcase**: Celebrate the unique cultural identity of each state

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Database**: Snowflake
- **Data Sources**: Open Government Datasets, Tourism Analytics
- **Visualization**: Interactive charts and mapping tools
- **Deployment**: https://culturevista-hsbdtsspw9nhsl53cbajza.streamlit.app/


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Snowflake account and credentials
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/cultural-heritage-explorer.git
cd cultural-heritage-explorer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your Snowflake credentials
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

4. Run the application:
```bash
streamlit run Gateway.py
```

5. Open your browser and navigate to `http://localhost:8501`

## 📊 Data Sources

Our platform integrates multiple data sources to provide comprehensive cultural insights:

- Government tourism datasets
- Cultural ministry databases
- Regional art form documentation
- Tourism trend analytics
- Seasonal event calendars

## 🎯 Impact & Goals

### Cultural Preservation
- Highlight endangered art forms requiring immediate attention
- Document traditional practices for future generations
- Support local artisan communities

### Sustainable Tourism
- Promote balanced tourism distribution across regions
- Encourage responsible cultural engagement
- Reduce over-tourism in popular destinations

### Education & Awareness
- Increase cultural literacy among travelers
- Foster appreciation for regional diversity
- Bridge cultural gaps through storytelling

## 🤝 Team Contributions

Our team worked collaboratively to bring this cultural heritage platform to life. Here are the specific contributions from each member:

### 👩‍💻 Anshi Gupta
- **Core Application Development**:
  - Living_Heritage.py - Complete development and UI design
  - Kreative_Traditions.py - Complete development and UI design
  - Gateway.py - Complete development and UI design
- **Data Contribution**:
  - indian_festivals.csv - Festival data compilation
  - dataset_temples - Contributed 150 out of 230 temple records
- **Project Management**:
  - README.md creation and documentation
  - License setup and requirements.txt
  - Page organization and custom display ordering
  - Application deployment and finishing touches

### 👨‍💻 Kapil Pradhan
- **Data Collection & Curation**: 
  - Dataset_Forts - Comprehensive fort data across India
  - Dataset_Museum - Museum information and details
  - Dataset_Temples - Contributed 80 out of 230 temple records
  - Responsible_tourism_Tips.csv - Curated responsible tourism guidelines
- **Feature Development**:
  - Preserve_tourism.py - Complete development and UI design
  - iQuick_guide.py - Complete development and UI design

### 👩‍💻 Vanshika Bhardwaj
- **Analytics & Visualization**:
  - Insights_Dashboard.py - Main dashboard development
  - Journey_trends.py - Tourism analysis and trends
- **Data Analysis**:
  - Footfall tourism data - All India statewise and monthwise analysis
  - Cultural richness score - Developed scoring methodology and implementation

### 👨‍💻 Dinesh Kumar
- **Data Architecture & Government Insights**:
  - tourism_trends_country.csv - National tourism trend data
  - heritage_sites.csv - Comprehensive heritage site information
  - footfall_tourism.csv - Tourism footfall statistics
  - tourism_trends_statewise.csv - State-wise tourism analysis
  - endangered_art_forms.csv - Documentation of at-risk cultural practices
  - art_culture_budget.csv - Cultural funding and budget data
  - employment_tourism.csv - Tourism sector employment statistics
- **Government Initiatives Module**:
  - Ministry_Programs.py - Complete development showcasing policy impacts and governmental support for cultural preservation
``

## 🔮 Future Enhancements

- Mobile application development
- AI-powered cultural recommendations
- Virtual reality cultural experiences
- Community-contributed content platform
- Multi-language support
- Integration with booking platforms

## 📱 Screenshots

[Add screenshots of your application here]

## 🤝 Contributing

We welcome contributions to help preserve and promote India's cultural heritage! Please read our contributing guidelines and submit pull requests for any improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- Government of India for providing open datasets
- Local cultural organizations and artisans
- Tourism boards across Indian states
- Open source community for amazing tools and libraries

---

**"Preserving culture through data, one story at a time."** 🇮🇳
