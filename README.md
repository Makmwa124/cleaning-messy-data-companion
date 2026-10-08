# Cleaning Messy Data: companion files

Free practice files for the book **Cleaning Messy Data: A Field Guide to 30 Real-World Data Problems and How to Fix Each One in Python, SQL and Excel** by Mathew Kariuki.

Every example in the book follows Priya, an analyst at Banksia Home Supply, as she cleans the customer export from Mallee Hardware & Garden, a business Banksia has just bought. Both companies are fictional. This repository holds the messy files exactly as Priya received them, the reference tables used to fix them, a SQLite copy for the SQL examples, and every code example from the book, so you can follow along.

## Download

Click the green **Code** button above, then **Download ZIP**. Unzip it somewhere sensible, such as your Documents folder.

## What's here

| Path | What it is |
| --- | --- |
| `data/raw/mallee_customers.csv` | The messy customer export (Windows-1252 encoded; Chapters 1 to 6 and 9) |
| `data/raw/web_orders.csv` | Two months of web orders with UTC times, mixed units and sentinels (Chapters 5 to 7) |
| `data/raw/products.csv` | Product list with two repeated codes (Problem 24) |
| `data/raw/supplier_prices.txt` | European price list: semicolons, decimal commas, a byte order mark (Problems 1 and 3) |
| `data/raw/sales_report.xlsx` | A report-style workbook: title rows, merged labels, subtotals, months as columns (Chapters 2, 4 and 8) |
| `data/raw/banksia_customers.csv` | Banksia's clean customer list, for matching in Chapter 9 |
| `data/reference/` | Lookup tables: towns and postcodes, state spellings, reviewed suburb fixes |
| `data/banksia.db` | SQLite database with the same tables, for the SQL examples |
| `book_code/` | Every Python and SQL example, chapter by chapter, plus the Try it answers |
| `scripts/clean_mallee.py` | The finished cleaning script from Chapter 9 |
| `scripts/make_data.py` | Rebuilds every practice file from scratch |
| `checklists/` | The new-file checklist (Appendix B) and a cleaning log template |

## Quick start

1. Install Python, then run:

   ```
   pip install pandas openpyxl
   ```

2. In VS Code, choose **File > Open Folder** and open this folder.
3. Run the finished cleaning script from a terminal in this folder:

   ```
   python scripts/clean_mallee.py
   ```

   It writes the clean customer file, the merge map and the cleaning log to an `output` folder.
4. Or create a notebook here and start exploring:

   ```python
   import pandas as pd
   raw = pd.read_csv('data/raw/mallee_customers.csv',
                     encoding='cp1252', dtype=str,
                     keep_default_na=False)
   raw.head()
   ```

Paths such as `data/raw/web_orders.csv` assume this folder is your working directory. For the SQL examples, open `data/banksia.db` in any SQLite tool, such as DB Browser for SQLite.

Tested with Python 3.13 and pandas 3.0.

## Get the book

Paperback and Kindle editions are on Amazon. The PDF bundle with a printable cheat sheet is on Gumroad at [mathewkariuki.gumroad.com](https://mathewkariuki.gumroad.com).

## About

Banksia Home Supply, Mallee Hardware & Garden and every person, email address and phone number in their data are fictional. Town names and postcodes are real. The data and code are free to use for learning. The book itself is © 2026 Mathew Kariuki.

Spotted a problem with an example or the data? Please open an issue.
