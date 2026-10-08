# 12_appD_answers: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

wo = pd.read_csv('data/raw/web_orders.csv', dtype=str,
                 keep_default_na=False)
prof = pd.DataFrame({'blank': (wo == '').sum(),
                     'unique': wo.nunique()})
print(prof)


print(wo.duplicated().sum(),
      wo['order_id'].duplicated().sum())


import csv
for enc in ['utf-8', 'utf-8-sig']:
    with open('data/raw/supplier_prices.txt',
              encoding=enc, newline='') as f:
        print(enc, next(csv.reader(f, delimiter=';')))


rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
row = rep[rep['Store'] == 'Glenelg'].iloc[0]
print(row[row.map(lambda v: isinstance(v, str))])


raw = pd.read_csv('data/raw/mallee_customers.csv',
                  encoding='cp1252', dtype=str,
                  keep_default_na=False)
nm = (raw['full_name'].str.replace('\xa0', ' ')
      .str.replace(r'\s+', ' ', regex=True).str.strip())
parts = nm.str.extract(
    r'^(?P<l>[^,]+),\s*(?P<f>.+)$|^(?P<f2>\S+)\s+.+$')
first = parts['f'].fillna(parts['f2']).str.title()
print((first == 'Zoë').sum())


from difflib import get_close_matches
ref = pd.read_csv('data/reference/localities.csv')
known = list(ref['suburb'])
for v in ['Victor Hbr', 'Mount Baker', 'Loxtn']:
    print(v, get_close_matches(v, known, n=2,
                               cutoff=0.6))


d = raw['phone'].str.replace(r'\D', '', regex=True)
d = d.str.replace(r'^61(?=\d{9}$)', '0', regex=True)
d = d.where(d.str.len() != 9, '0' + d)
mobile = d.str.fullmatch(r'04\d{8}')
print(mobile.sum(), 'mobiles;',
      d.str.fullmatch(r'08\d{8}').sum(), 'landlines')


dflt = pd.read_csv('data/raw/mallee_customers.csv',
                   encoding='cp1252', dtype=str)
print(dflt.isna().sum()[lambda s: s > 0])


print(raw.assign(no_phone=raw['phone'] == '')
         .groupby('signup_channel')['no_phone']
         .mean().round(3))


def shape(s):
    return (s.str.replace(r'\d', '9', regex=True)
             .str.replace(r'[A-Za-z]', 'A', regex=True))

print(shape(raw['phone']).value_counts())


wo = pd.read_csv('data/raw/web_orders.csv')
ts = pd.to_datetime(wo['order_ts_utc'], utc=True)
local = ts.dt.tz_convert('Australia/Adelaide')
print(local.dt.hour.value_counts().head(3))


upd = raw.groupby('cust_no')['last_updated'].nunique()
print(upd.max(), upd.idxmax(), (upd > 1).sum())


nm = (raw['full_name'].str.replace('\xa0', ' ')
      .str.replace(r'\s+', ' ', regex=True).str.strip()
      .str.lower())
key = nm + '|' + raw['suburb'].str.strip().str.lower()
k = raw.drop_duplicates().assign(key=key)
low = k.groupby('key')['cust_no'].transform('min')
found = set(zip(k['cust_no'], low)) - set(
    zip(low, low))
mm = pd.read_csv('output/mallee_merge_map.csv',
                 dtype=str)
real = set(zip(mm['old'], mm['new']))
print(len(found & real), 'real,',
      len(found - real), 'false matches')


wo = pd.read_csv('data/raw/web_orders.csv',
                 dtype={'customer_id': str})
wo = wo.drop_duplicates()
pr = pd.read_csv('data/raw/products.csv')
wo['unit_price'] = wo['unit_price'].where(
    wo['unit_price'] < 1000, wo['unit_price'] / 100)
wo['qty'] = wo['qty'].where(wo['qty'].between(1, 500))
j = wo.merge(pr, on='product_code')
rev = lambda d: (d['qty'] * d['unit_price']).sum()
print(len(j) - len(wo), 'extra rows;',
      f'${rev(j) - rev(wo):,.0f} extra revenue')


wo = (pd.read_csv('data/raw/web_orders.csv',
                  dtype={'customer_id': str})
      .drop_duplicates())
pr = (pd.read_csv('data/raw/products.csv')
      .drop_duplicates('product_code'))
w = wo.merge(pr[['product_code', 'weight_kg']],
             on='product_code')
kg = w['ship_weight'].where(w['weight_unit'] == 'kg',
                            w['ship_weight'] / 1000)
s = w[w['qty'].isin([999, -1])]
est = (kg[s.index] / s['weight_kg']).round()
print(est.value_counts())


w = wo.merge(pr[['product_code', 'price']],
             on='product_code')
up = w['unit_price'].where(w['unit_price'] < 1000,
                           w['unit_price'] / 100)
qty = w['qty'].where(~w['qty'].isin([999, -1]), 0)
w['line'] = qty * up
per_line = (w['line'] / 1.1).round(2).groupby(
    w['product_code']).sum()
per_prod = (w.groupby('product_code')['line'].sum()
            / 1.1).round(2)
print((per_line - per_prod).abs().idxmax(),
      round((per_line - per_prod).abs().max(), 2))


rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
rep = rep[rep['Store'].notna()].copy()
rep['Region'] = rep['Region'].ffill()
rep = rep[~rep['Store'].str.contains('total')]
long = rep.melt(['Region', 'Store', 'Opened'],
                var_name='month', value_name='sales')
long['sales'] = pd.to_numeric(long['sales'].astype(str)
                .str.replace(r'[$,]', '', regex=True))
t = long.groupby(['Region', 'Store'])['sales'].sum()
print((t / t.groupby(level=0).transform('sum'))
      .round(3))


long['month'] = pd.to_datetime(long['month'],
                               format='%b-%y')
tab = long.pivot_table(index='Store', columns='month',
                       values='sales', aggfunc='sum',
                       margins=True, margins_name='Total')
print(tab.shape)

