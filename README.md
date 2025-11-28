# Krystal

> Mobile interface for power structure analysis

Krystal is a mobile application that overlays power structure mapping onto news content using the Google News API and LittleSis API. The app reveals connections between corporations, government officials, and other powerful entities mentioned in news stories.

Krystal is the mobile frontend that brings power structure mapping to your smartphone. Built with Kivy and Python, it provides an intuitive interface for analyzing power relationships in news media using the Krystal Core engine.

## 🎯 Mission

To make power structure analysis accessible on mobile devices, enabling users to understand the connections between powerful entities while reading news anywhere, anytime.

## 📱 Features

- **Mobile-Optimized Interface**: Touch-friendly design for smartphones and tablets
- **Real-time Power Mapping**: Instant visualization of entity relationships
- **News Integration**: Direct analysis of articles from various sources
- **Offline Capability**: Basic functionality without constant internet connection
- **Privacy-Focused**: No user tracking or data collection

## 🛠 Technology Stack

- **Frontend**: Kivy 2.0+ (MIT) + KivyMD (MIT)
- **Language**: Python 3.8+
- **Core Engine**: Krystal Core (LGPL v3)
- **Data Visualization**: Custom Kivy widgets + Matplotlib
- **APIs**: Google News, LittleSis, OpenSecrets
- **Packaging**: Buildozer for Android/iOS deployment
- **License**: GNU GPL v3

## 📄 License

This project is licensed under the **GNU Lesser General Public License v3.0**.

**Why LGPL v3?**

- Ensures the core framework remains free and open
- Allows linking with proprietary components (useful for some API integrations)
- Maintains software freedom while enabling practical distribution
- Aligns with our mission of transparency and accessibility

See the [LICENSE](LICENSE) file for the complete license text.

## 🚀 Getting Started

[Development setup instructions to be added]

## 🤝 Contributing

We welcome contributions from developers who share our commitment to transparency and open knowledge. Please read our contributing guidelines before submitting pull requests.

## 🔗 Data Sources

- [LittleSis](https://littlesis.org/) - Public database of power relationships
- [Google News API](https://newsapi.org/) - News aggregation
- [OpenSecrets](https://www.opensecrets.org/) - Political funding data

## 📸 Screenshots

*Application screenshots will be added during development*

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Krystal Core package installed
- Android SDK (for mobile builds)
- Xcode (for iOS builds, macOS only)

### Installation

```bash
# Install the core package first (from project root)
pip install -e ../core

# Install the app package
pip install -e .

# Or install both at once
pip install -e ../core -e .
