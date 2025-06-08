# Margin Calculator

This project contains a simple margin calculator built with [Streamlit](https://streamlit.io/). It provides two tools:

1. **Margin / price drop** – calculates the sales volume increase needed to maintain profit when the margin or price is reduced.
2. **Quick margin calculator** – quickly derives margin, price or unit cost when any two of these values are provided.

The application supports both Polish and English languages and runs entirely in the browser using Streamlit.

## Setup

Install the package in editable mode and set up the pre-commit hooks before starting the application:

```bash
pip install -e .
pip install pre-commit
pre-commit install
streamlit run app.py
```

By default Streamlit launches at `http://localhost:8501`. Open this address in your browser to access the calculator.

## Running tests

To run the automated tests, install the project in editable mode and execute `pytest`:

```bash
pip install -e .
pytest
```

## Usage

Select the desired language from the sidebar, choose one of the tabs, fill in the required fields and press **Calculate**. The application will display the computed margin and related information.


## Command line interface

Basic calculations are also accessible from the command line. Run `python cli.py --help` to list the available commands.

Calculate margin:

```bash
python cli.py marza 50 100
```

Calculate sale price from a desired margin:

```bash
python cli.py cena 50 0.2
```

## Docker

The repository includes a `Dockerfile` so the application can be run in a
container without installing Python locally.

Build the image with:

```bash
docker build -t margin-calculator .
```

Then start the container:

```bash
docker run -p 8501:8501 margin-calculator
```

Once running, open `http://localhost:8501` in your browser to use the app.


## Streamlit Community Cloud

You can also deploy the calculator on [Streamlit Community Cloud](https://streamlit.io/cloud). Create a new app from this repository, and the service will automatically install the dependencies listed in `requirements.txt` and launch the application with:

```bash
streamlit run app.py
```

Make sure to push your code to a Git repository (for example on GitHub) so Streamlit Cloud can access it. If your application uses secrets or other configuration values, define them as environment variables in the app's settings.

