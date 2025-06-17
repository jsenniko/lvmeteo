from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lvmeteo",
    version="0.1.0",
    author="LVMeteo Team",
    author_email="",
    description="A Python library for accessing Latvian meteorological data from data.gov.lv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lvmeteo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    keywords="meteorology, weather, latvia, data, api",
)