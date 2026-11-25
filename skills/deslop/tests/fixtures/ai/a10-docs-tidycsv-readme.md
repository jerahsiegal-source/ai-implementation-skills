# tidycsv

Clean messy CSV files in a few lines of Python. `tidycsv` handles the usual problems: inconsistent headers, stray whitespace, mixed-case column names, empty rows, duplicate rows, and mixed delimiters or encodings.

## Installation

```bash
pip install tidycsv
```

Requires Python 3.9 or newer.

## Quick start

```python
import tidycsv

clean = tidycsv.read("messy.csv")
clean.to_csv("tidy.csv")
```

## Usage

### Load and clean a file

```python
import tidycsv

df = tidycsv.read(
    "sales_raw.csv",
    strip_whitespace=True,      # trim leading/trailing spaces in every cell
    normalize_headers=True,     # "  Order ID " -> "order_id"
    drop_empty=True,            # remove blank rows and columns
    drop_duplicates=True,       # remove exact duplicate rows
)

print(df.head())
```

### Detect the delimiter and encoding automatically

```python
import tidycsv

df = tidycsv.read("export_from_excel.csv", delimiter="auto", encoding="auto")
```

### Clean in memory from a string

```python
import tidycsv

raw = """  Name ,Age,City
 Ada Lovelace , 36 ,London
,,
Ada Lovelace , 36 ,London
"""

df = tidycsv.read_string(raw)
print(df.to_records())
# [{'name': 'Ada Lovelace', 'age': '36', 'city': 'London'}]
```

### Apply your own column transforms

```python
import tidycsv

df = tidycsv.read("orders.csv")

df = df.transform_column("amount", lambda v: float(v.replace("$", "").replace(",", "")))
df = df.rename_columns({"cust_id": "customer_id"})
df = df.fill_missing("region", value="unknown")

df.to_csv("orders_clean.csv")
```

### Command line

```bash
tidycsv clean messy.csv -o tidy.csv
tidycsv clean messy.csv --delimiter auto --drop-duplicates
tidycsv inspect messy.csv        # report issues without writing anything
```

## Options

| Option | Default | Description |
|---|---|---|
| `delimiter` | `","` | Column separator, or `"auto"` to detect it |
| `encoding` | `"utf-8"` | File encoding, or `"auto"` to detect it |
| `strip_whitespace` | `True` | Trim whitespace from every cell |
| `normalize_headers` | `True` | Convert headers to lowercase `snake_case` |
| `drop_empty` | `True` | Remove fully blank rows and columns |
| `drop_duplicates` | `False` | Remove exact duplicate rows |

## Development

```bash
git clone https://github.com/your-org/tidycsv.git
cd tidycsv
pip install -e ".[dev]"
pytest
```

## License

MIT
