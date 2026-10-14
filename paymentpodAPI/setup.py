"""
Setup script for Vulnerability Orchestrator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# packages = find_packages(include=["orchestrator", "orchestrator.*", "skills", "skills.*"])
# Metadata
setup(
    name="vulnerability-orchestrator",
    version="1.0.0",
    author="Security Team",
    description="Automated vulnerability detection and fixing for Payment Pod API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),   #find all directories and subdirectories
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#dependency management

    python_requires=">=3.8",
    install_requires=[
        "PyGithub==2.1.1",
        "jira==3.10.5",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "coverage==7.16.2",
        "pytest==9.1.1",
        "pytest-cov==7.1.0",
    ],
    entry_points={
        "console_scripts": [
            "vulnerability-orchestrator=main:main",
        ],
    },
)
