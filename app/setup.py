from setuptools import setup, find_packages

setup(
    name="krystal-app",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "krystal-core>=0.1.0",  # Our core package
        "kivy>=2.0.0",
        "kivymd>=1.1.1",
        "Pillow>=9.0.0",        # For image support in Kivy
    ],
    python_requires=">=3.8",
    author="Krystal Team",
    author_email="your-email@example.com",
    description="Mobile app for mapping power structures in news media",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/krystal",
    license= "GPL-3.0-or-later",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Sociology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
         "GPL-3.0-or-later",
    ],
    keywords="power mapping, network analysis, transparency, news analysis, mobile app",
    project_urls={
        "Documentation": "https://github.com/your-username/krystal/docs",
        "Source": "https://github.com/your-username/krystal",
        "Tracker": "https://github.com/your-username/krystal/issues",
    },
    entry_points={
        "console_scripts": [
            "krystal-app=krystal_app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "krystal_app": [
            "*.kv",           # Kivy language files
            "assets/*.png",   # App icons and images
            "assets/*.jpg",
            "assets/*.ttf",   # Font files
        ],
    },
    options={
        "build_exe": {
            "includes": ["kivy", "kivymd"],
        },
    },
)