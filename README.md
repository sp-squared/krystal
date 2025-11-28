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

## 📄 Licensing

This project uses a strategic dual-licensing approach to balance software freedom with practical adoption:

### Core Engine: GNU Lesser General Public License v3.0 (LGPL v3)

**Why LGPL v3 for the core algorithms?**

- **Maximum Adoption**: Allows proprietary applications to use our power mapping engine while ensuring improvements to the core are shared back
- **Research Friendly**: Enables academic researchers and journalists to integrate our algorithms into their proprietary tools and workflows
- **Enterprise Compatibility**: Corporations can build internal tools using our engine without contaminating their IP
- **Freedom Preservation**: Modifications to the core engine itself must remain open source, protecting the foundational technology
- **Practical Impact**: Balances ideological purity with real-world influence by allowing our transparency technology to reach wider audiences

**LGPL v3 Requirements:**

- Users can dynamically link to our core library in proprietary software
- Modifications to the core library source must be released under LGPL v3
- Users must provide a way to relink with modified versions of the core

### Mobile Application: GNU General Public License v3.0 (GPL v3)

**Why GPL v3 for the mobile app?**

- **Complete Transparency**: Ensures the user-facing application and all derivatives remain fully open source
- **Mission Alignment**: Prevents proprietary forks that could hide or obscure power structures—the very problem we're fighting
- **User Freedom Guarantee**: Protects end users' rights to study, modify, and share the application
- **Strong Copyleft**: Creates a protective barrier around the complete user experience
- **Community Building**: Encourages collaborative improvement of the interface and user workflows

**GPL v3 Requirements:**

- Any derivative work based on the app must be licensed under GPL v3
- Complete source code must be available to all users
- All modifications must be clearly documented and shared

### Strategic Rationale

This dual-license structure creates a "protected commons" model:

- **Core (LGPL v3)**: Our power mapping technology can spread widely, becoming a standard for transparency analysis
- **App (GPL v3)**: The user experience remains completely transparent, preventing enclosure of the interface to power structure data

This approach ensures that while the underlying technology can achieve broad adoption, the primary user interface remains a protected public good that cannot be privatized or used to obscure the very power structures we aim to reveal.

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
