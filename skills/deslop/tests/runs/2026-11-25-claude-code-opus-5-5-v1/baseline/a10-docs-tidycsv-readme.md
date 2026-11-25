# tidycsv

`tidycsv` cleans up messy CSV files with a few lines of Python. It fixes inconsistent headers, stray whitespace, mixed-case column names, empty rows, duplicate rows, and files with mixed delimiters or encodings.

## Install

```bash
pip install tidycsv
```

You'll need Python 3.9+.

## Quick start

```python
import tidycsv

clean = tidycsv.read("messy.csv")
clean.to_csv("tidy.csv")
```

## Usage

### Reading and cleaning a file

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

### Auto-detecting delimiter and encoding

Pass `"auto"` if you don't know what the file uses. This is common with Excel exports.

```python
import tidycsv

df = tidycsv.read("export_from_excel.csv", delimiter="auto", encoding="auto")
```

### Cleaning a string in memory

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

### Custom column transforms

```python
import tidycsv

df = tidycsv.read("orders.csv")

df = df.transform_column("amount", lambda v: float(v.replace("$", "").replace(",", "")))
df = df.rename_columns({"cust_id": "customer_id"})
df = df.fill_missing("region", value="unknown")

df.to_csv("orders_clean.csv")
```

### CLI

```bash
tidycsv clean messy.csv -o tidy.csv
tidycsv clean messy.csv --delimiter auto --drop-duplicates
tidycsv inspect messy.csv        # report issues without writing anything
```

## Options

| Option | Default | What it does |
|---|---|---|
| `delimiter` | `","` | Column separator. Use `"auto"` to detect it |
| `encoding` | `"utf-8"` | File encoding. Use `"auto"` to detect it |
| `strip_whitespace` | `True` | Trims whitespace from every cell |
| `normalize_headers` | `True` | Converts headers to lowercase `snake_case` |
| `drop_empty` | `True` | Drops rows and columns that are completely blank |
| `drop_duplicates` | `False` | Drops exact duplicate rows |

## Development

```bash
git clone https://github.com/your-org/tidycsv.git
cd tidycsv
pip install -e ".[dev]"
pytest
```

## License

MIT
