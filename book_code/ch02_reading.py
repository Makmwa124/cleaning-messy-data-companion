# 02_ch02_reading: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

try:
    pd.read_csv('data/raw/mallee_customers.csv')
except UnicodeDecodeError as e:
    print(f'{e.encoding} cannot read byte '
          f'{e.object[e.start]:#x} at position {e.start}')


import re
data = open('data/raw/mallee_customers.csv', 'rb').read()
odd = sorted(set(re.findall(rb'[\x80-\xff]', data)))
print(odd)


raw = pd.read_csv('data/raw/mallee_customers.csv',
                  encoding='cp1252', dtype=str,
                  keep_default_na=False)
names = raw['full_name']
print(names[names.str.contains('’|ë|é')].head(4))


bad = pd.Series(['ZoÃ«', 'CafÃ© Banksia',
                 'Oâ€™Brien', 'Smith'])

def unmangle(s):
    try:
        return s.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s

print(bad.map(unmangle))


with open('data/raw/supplier_prices.txt',
          encoding='utf-8') as f:
    print(repr(f.readline()[:16]))


checks = {'Ã': 'Ã', 'â€': 'â€', '\ufffd': 'U+FFFD'}
for char, label in checks.items():
    print(label, raw['full_name'].str.contains(char).sum())


rep = pd.read_excel('data/raw/sales_report.xlsx')
print(rep.columns[:4].tolist())


peek = pd.read_excel('data/raw/sales_report.xlsx',
                     header=None)
print(peek.iloc[:6, :3])
print(peek.iloc[-1, 0])


rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
rep = rep[rep['Store'].notna()]
print(rep.iloc[:, :4])


assert rep.columns[:3].tolist() == ['Region', 'Store',
                                    'Opened']
print(len(rep), 'rows')


from pandas.errors import ParserError
try:
    pd.read_csv('data/raw/supplier_prices.txt',
                encoding='utf-8-sig')
except ParserError as e:
    print(str(e).replace('. C error', '.\nC error'))


with open('data/raw/supplier_prices.txt',
          encoding='utf-8-sig') as f:
    for _ in range(3):
        print(f.readline().rstrip())


sup = pd.read_csv('data/raw/supplier_prices.txt',
                  encoding='utf-8-sig', sep=';',
                  decimal=',', thousands='.')
print(sup[['sku', 'unit_price_eur']])
print(sup['unit_price_eur'].dtype)


assert sup.shape[1] == 4
assert sup['unit_price_eur'].dtype == 'float64'


pts = raw['loyalty_points']
print(pts.head(6).tolist())
print(pts.dtype)


as_num = pd.to_numeric(pts, errors='coerce')
failed = pts[as_num.isna() & (pts != '')]
print(failed.value_counts().head(8))


cleaned = pts.str.replace(r'[$,\s]', '', regex=True)
points = pd.to_numeric(cleaned, errors='coerce')
still_bad = pts[points.isna() & (pts != '')]
print(still_bad.value_counts())
print(points.describe().round(1))


money = pd.Series(['$1,204.50', '(45.00)', ' 310 ',
                   '$-12.00'])
fixed = (money.str.strip()
              .str.replace(r'^\((.*)\)$', r'-\1', regex=True)
              .str.replace(r'[$,]', '', regex=True))
print(pd.to_numeric(fixed).tolist())


n_blank = (pts == '').sum()
n_na = (pts == 'N/A').sum()
assert points.isna().sum() == n_blank + n_na


guessed = pd.read_csv('data/raw/mallee_customers.csv',
                      encoding='cp1252')
print(guessed['cust_no'].head(3).tolist())
print(guessed['postcode'].dtype)


print(raw['postcode'].str.len().value_counts())
print(raw.loc[raw['postcode'].str.len() < 4,
              ['suburb', 'postcode']].drop_duplicates())


raw['postcode'] = raw['postcode'].str.zfill(4)
print(raw['postcode'].str.len().value_counts())


assert raw['postcode'].str.fullmatch(r'\d{4}').all()
ref = pd.read_csv('data/reference/localities.csv',
                  dtype=str)
print(raw['postcode'].isin(ref['postcode']).mean())

