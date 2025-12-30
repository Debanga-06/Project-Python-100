# 🌤️ Weather Application

A modern, user-friendly desktop weather application built with Python that provides real-time weather information for any city worldwide.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Information](#api-information)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Weather Data**: Fetches current weather information using OpenWeatherMap API
- **Intuitive GUI**: Clean and modern interface built with Tkinter
- **Comprehensive Weather Details**:
  - Current temperature (°C)
  - Weather description
  - Humidity percentage
  - Wind speed
  - Atmospheric pressure
  - "Feels like" temperature
- **JSON Data Handling**: Parse API responses and save weather data locally
- **Search Functionality**: Search weather by city name
- **Export Capability**: Save weather data as JSON files for later reference
- **Error Handling**: Robust error management for network issues and invalid inputs
- **Responsive Design**: User-friendly interface with visual feedback

## 📸 Screenshots

```
┌─────────────────────────────────┐
│      🌤️ Weather App            │
│                                 │
│  Enter City: [London    ] 🔍   │
│                                 │
│  ┌──────────────────────────┐  │
│  │  London, GB              │  │
│  │                          │  │
│  │      15.3°C              │  │
│  │                          │  │
│  │   Partly Cloudy          │  │
│  │                          │  │
│  │  💧 Humidity: 72%        │  │
│  │  💨 Wind: 4.5 m/s        │  │
│  │  🎚️ Pressure: 1013 hPa   │  │
│  │  🌡️ Feels Like: 14.1°C   │  │
│  │                          │  │
│  │  Updated: 2024-12-30...  │  │
│  └──────────────────────────┘  │
│                                 │
│    [Save Weather Data]          │
└─────────────────────────────────┘
```

## 🔧 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.7 or higher**
- **pip** (Python package manager)
- **Internet connection** (for API requests)

## 📦 Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

Or download the ZIP file and extract it.

### Step 2: Install Required Dependencies

```bash
pip install requests
```

**Note**: `tkinter` is included with most Python installations. If it's not available, install it:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Included with Python
- **Windows**: Included with Python

### Step 3: Verify Installation

```bash
python --version
pip list | grep requests
```

## ⚙️ Configuration

### Getting Your API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Click on "Sign Up" and create a free account
3. Navigate to your account dashboard
4. Go to "API Keys" section
5. Copy your API key

### Adding Your API Key

Open `weather_app.py` and replace the placeholder with your actual API key:

```python
self.api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
```

Example:
```python
self.api_key = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

**Important**: Keep your API key private and never commit it to public repositories.

## 🚀 Usage

### Running the Application

```bash
python weather_app.py
```

### Using the Application

1. **Search for Weather**:
   - Enter a city name in the search box
   - Click the "Search" button or press Enter
   - View the weather information displayed

2. **Save Weather Data**:
   - After searching for a city, click "Save Weather Data"
   - A JSON file will be created with the format: `weather_CityName_YYYYMMDD_HHMMSS.json`
   - The file will be saved in the same directory as the application

### Example Cities to Try

- London
- New York
- Tokyo
- Paris
- Sydney
- Mumbai
- Berlin
- Toronto

## 🌐 API Information

### OpenWeatherMap API

This application uses the OpenWeatherMap Current Weather Data API.

- **Endpoint**: `http://api.openweathermap.org/data/2.5/weather`
- **Free Tier Limits**: 
  - 1,000 API calls per day
  - 60 calls per minute
- **Data Format**: JSON
- **Temperature Units**: Metric (Celsius)

### API Response Structure

```json
{
  "name": "London",
  "sys": {"country": "GB"},
  "main": {
    "temp": 15.3,
    "feels_like": 14.1,
    "humidity": 72,
    "pressure": 1013
  },
  "wind": {"speed": 4.5},
  "weather": [{"description": "partly cloudy"}]
}
```

## 📁 Project Structure

```
weather-app/
│
├── weather_app.py          # Main application file
├── README.md               # This file
├── requirements.txt        # Python dependencies (optional)
├── .gitignore             # Git ignore file (optional)
│
└── weather_*.json         # Saved weather data files (created by app)
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**Issue**: "Invalid API key" error
- **Solution**: Ensure you've replaced `YOUR_API_KEY_HERE` with your actual API key
- Verify your API key is active on OpenWeatherMap dashboard

**Issue**: "City not found" error
- **Solution**: Check the spelling of the city name
- Try using larger cities or include country code (e.g., "London,UK")

**Issue**: "Connection Error"
- **Solution**: Check your internet connection
- Verify you can access https://openweathermap.org in your browser

**Issue**: tkinter not found
- **Solution**: Install tkinter for your operating system (see Installation section)

**Issue**: "Request timed out"
- **Solution**: Check your internet speed
- Try again after a few moments

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

### Ideas for Contributions

- Add 5-day forecast functionality
- Implement temperature unit conversion (Celsius/Fahrenheit)
- Add weather icons
- Create a favorites/recent cities list
- Add support for other weather APIs
- Implement dark/light theme toggle
- Add weather alerts and notifications

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check the [Troubleshooting](#troubleshooting) section
- Review OpenWeatherMap's [API documentation](https://openweathermap.org/api)

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- Python Tkinter for the GUI framework
- The Python community for excellent documentation

## 📊 Version History

- **v1.0.0** (2024-12-30)
  - Initial release
  - Basic weather search functionality
  - JSON data export feature
  - Modern GUI interface

---

**Made with ❤️ using Python**

*Last Updated: December 30, 2025*
