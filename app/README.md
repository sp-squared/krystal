# Krystal App

> Mobile interface for power structure analysis

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
