# setup.py
from setuptools import setup, find_packages

setup(
    name="langchain-asi",
    version="0.1.0",
    description="LangChain integration for ASI1 API",
    author="Rajashekar Vennavelli",
    author_email="rajashekarvennavelli@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.0.267",
        "requests>=2.28.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)