from setuptools import setup, find_packages

setup(
    name="krystal-core",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.25.0",
        "networkx>=2.5",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "newsapi-python>=0.2.6",
    ],
    python_requires=">=3.8",
    author="Krystal Team",
    description="Core power mapping algorithms for transparency applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown", 
    license="LGPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
)