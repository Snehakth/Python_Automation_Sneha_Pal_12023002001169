# Selenium E-Commerce Purchase Automation

This capstone automates a customer purchase on the public Tutorialsninja OpenCart demo. It registers a unique demo account for each run, logs in through the site's login form, searches for a product, adds it to the cart, updates the quantity, and verifies the cart row.

### Project demonstration video:-
<a>https://drive.google.com/file/d/1GF4AU413_59F7djUJngHtA5CzkL5HjqE/view?usp=sharing</a>

## Setup

Requires Python 3.10+ and Google Chrome. Selenium Manager locates/downloads the matching driver when needed. Install dependencies into your system Python:

```powershell
py -m pip install -r requirements.txt
```

## Run

The default scenario comes from `test_data/purchase.json`:

```powershell
py -m pytest
```

To run headlessly, set `HEADLESS=1`. To use Excel instead of JSON, first generate the sample workbook and select it:

```powershell
py -m test_data.create_sample_excel
$env:TEST_DATA_FILE = "test_data/purchase.xlsx"
py -m pytest
```

The loader also accepts an existing `.xlsx` or `.xlsm` workbook whose active sheet has `base_url`, `product_name`, and `quantity` columns in its first row, followed by one scenario row. `TEST_DATA_FILE` may be an absolute path or a path relative to the project root.

## Artifacts

- HTML execution report: `artifacts/execution-report.html`
- Screenshots: `artifacts/screenshots/` (after product add, after cart update, and automatically on test failure)

The demo site is shared and can be rate-limited or unavailable. Each successful run creates a fresh account on that site.


