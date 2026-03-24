# RZD Product Catalog Parameterization

Solution for the Digital Breakthrough 2024 case by [RZD](https://hacks-ai.ru/events/1077380).

## Overview

The goal is to transform raw product catalog records into a structured, parameterized dataset.

We enrich product rows with additional attributes extracted from external product pages, then use those attributes for downstream grouping and analytics.

## Problem Statement

Given a product database, identify potential product categories and extract useful features from text descriptions, then convert the original dataset into a parameter-based format.

## Data Sources

- Product reference tables:
  - `ED_IZM` (auxiliary dataset)
  - `GOST` (auxiliary dataset)
  - `MTR` (**main dataset to transform**)
  - `OKPD_2` (auxiliary dataset)
- Web sources used for product feature extraction

## Approach

1. Filter and group products by `OKPD_2`.
2. Build a search query from product name/model metadata.
3. Find matching (or closest) products on [Yandex Market](https://market.yandex.ru).
4. Extract available product characteristics.
5. Optionally use LLM-based post-processing for attribute normalization.
6. Cluster products based on extracted parameters.

## Why Yandex Market

- Thousands of categories and a very large product base
- Practical and scalable source for broad catalog enrichment
- Easy to validate quickly for prototype-level pipelines

## Sample Target Output

![Initial target result mockup](images/first_target.png)

## Tech Stack

- `Selenium` for web parsing
- `GigaChat` and `ChatGPT` for LLM-assisted processing
- `pandas`, `numpy`, `matplotlib` for analytics

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python parser.py
```

The script reads `itog_data_from_pars.csv`, extracts parameters for each product, and saves the result to `new.csv`.

## Code Quality

```bash
uvx ruff check .
uvx ruff format parser.py
uvx pyrefly check parser.py --ignore missing-source-for-stubs --ignore missing-import
```

## Project Files

| File | Description |
| --- | --- |
| `LLM_checked_df.csv` | LLM-labeled dataset |
| `itog_data_from_pars.csv` | Parsed intermediate dataset |
| `parser.py` | Main parser script |
| `final_notebook.ipynb` | Notebook with labeling and analysis |
| `train_dataset_rzd_catalog.zip` | Archive with initial source data |
| `user-agents.txt` | User-Agent pool for requests |
| `requirements.txt` | Python dependencies |
