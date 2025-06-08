# Margin Calculator

This project contains a simple margin calculator built with [Streamlit](https://streamlit.io/). It provides two tools:

1. **Margin / price drop** – calculates the sales volume increase needed to maintain profit when the margin or price is reduced.
2. **Quick margin calculator** – quickly derives margin, price or unit cost when any two of these values are provided.

The application supports both Polish and English languages and runs entirely in the browser using Streamlit.

## Setup

Install the required packages and start the application:

```bash
pip install -r requirements.txt
streamlit run app.py
```

By default Streamlit launches at `http://localhost:8501`. Open this address in your browser to access the calculator.

## Running tests

To run the automated tests, install the project dependencies and execute `pytest`:

```bash
pip install -r requirements.txt
pytest
```

## Usage

Select the desired language from the sidebar, choose one of the tabs, fill in the required fields and press **Calculate**. The application will display the computed margin and related information.

