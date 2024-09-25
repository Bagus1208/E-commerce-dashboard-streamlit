# Python Project Setup Guide

Welcome! This guide will help you set up the development environment for this Python project. You have two options for managing your environment: using **Anaconda** or **Python's virtual environment (venv)**. Follow the instructions below based on your preference.

## Prerequisites

Ensure that you have the following installed:
- Python 3.x
- [Anaconda](https://www.anaconda.com/products/individual#download-section) (if using Anaconda)
- Command line terminal (e.g., bash, zsh, or Command Prompt)

---

## Option 1: Setting up with Anaconda

If you prefer to use Anaconda, follow these steps:

### 1. Create a new environment
In your terminal, run the following command to create a new environment. Replace `3.x` with your preferred Python version (e.g., `3.8`).

```bash
conda create --name submission python=3.x
```
### 2. Activate the environment
Activate the environment by running the command:
```
conda activate submission
```
### 3. Install dependencies
Once the environment is activated, install the required dependencies:
```
pip install -r requirements.txt
```
### 4. Deactivate the environment
To deactivate the environment when you are done:
```
conda deactivate
```

---

## Option 2: Setting up with Virtual Environment (venv)
If you prefer using Python's built-in venv, follow these steps:
### 1. Create a virtual environment
In your project directory, run the following command. Replace `env` with the name you want for the virtual environment directory:
```
python3 -m venv env
```
### 2. Activate the virtual environment
For **Linux/Mac** users:
```
source env/bin/activate
```
For **Windows** users:
```
.\env\Scripts\activate
```
### 3. Install dependencies
With the virtual environment **activated**, install the required dependencies:
```
pip install -r requirements.txt
```
### 4. Deactivate the virtual environment
To deactivate the environment when finished, run:
```
deactivate
```

---

## Running the Project
Once the environment is set up and dependencies are installed, you can run the project by using:
```
streamlit run dashboard/dashboard.py
```

---

## Additional Information
You can see how the dashboard looks when run by clicking the link below.

 [Dashboard view](https://e-commerce-dashboard-app-2tzk79wum2ariruwxfgch6.streamlit.app/)