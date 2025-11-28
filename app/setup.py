from setuptools import setup, find_packages

setup(
    name="krystal-app",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "krystal-core>=0.1.0",  # This will look for the local version first
        "kivy>=2.0.0",
        "kivymd>=1.1.1",
        "Pillow>=9.0.0",  # For image support in Kivy
    ],
    python_requires=">=3.8",
    author="Krystal Team",
    description="Mobile app for mapping power structures in news media",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
)