# 06_ch06_duplicates: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

raw = pd.read_csv('data/raw/mallee_customers.csv',
                  encoding='cp1252', dtype=str,
                  keep_default_na=False)

def tidy(s):
    return (s.str.replace('\xa0', ' ')
             .str.replace(r'\s+', ' ', regex=True)
             .str.strip())

raw = raw.apply(tidy)
print(len(raw))


dups = raw[raw.duplicated(keep=False)]
print(len(dups), 'rows involved,',
      raw.duplicated().sum(), 'extra copies')
print(dups.sort_values('cust_no')
      [['cust_no', 'full_name', 'suburb']].head(4))


before = len(raw)
raw = raw.drop_duplicates()
print(before - len(raw), 'removed;', len(raw), 'left')


wo = pd.read_csv('data/raw/web_orders.csv',
                 dtype={'customer_id': str})
print('Repeated rows:', wo.duplicated().sum())
print('Repeated order_id:',
      wo['order_id'].duplicated().sum())


assert not raw.duplicated().any()
assert len(raw) == before - 40


raw['email_key'] = (raw['email'].str.lower()
                    .where(raw['email'].str.contains('@')))
digits = raw['phone'].str.replace(r'\D', '', regex=True)
raw['phone_key'] = digits.str[-9:].where(
    digits.str.len() >= 9)


def pairs_on(key):
    d = raw.dropna(subset=[key])
    low = d.groupby(key)['cust_no'].transform('min')
    return (pd.DataFrame({'old': d['cust_no'],
                          'new': low})
            .query('old != new').drop_duplicates())

by_email = pairs_on('email_key')
by_phone = pairs_on('phone_key')
both = by_email.merge(by_phone)
print('Email:', len(by_email), ' Phone:', len(by_phone),
      ' Both:', len(both))


one_key = (pd.concat([by_email, by_phone])
           .drop_duplicates()
           .merge(both, how='left', indicator=True)
           .query('_merge == "left_only"'))
cols = ['cust_no', 'email', 'phone', 'suburb']
for _, p in one_key.iterrows():
    print(raw.loc[raw['cust_no'].isin([p['old'], p['new']]),
                  cols].to_string(header=False,
                                  index=False))
    print()


merge_map = (pd.concat([by_email, by_phone])
             .drop_duplicates())
assert merge_map['old'].is_unique
print(len(merge_map), 'customer numbers merged')
raw = raw[~raw['cust_no'].isin(merge_map['old'])]


for key in ['email_key', 'phone_key']:
    n = raw.dropna(subset=[key]).groupby(key)[
        'cust_no'].nunique()
    assert n.max() == 1, key
print(len(raw), 'rows')


rep = raw[raw['cust_no'].duplicated(keep=False)]
print(rep['cust_no'].nunique())
print(rep.sort_values(['cust_no', 'last_updated'])
      [['cust_no', 'suburb', 'postcode',
        'last_updated']].head(4))


print(raw['cust_no'].duplicated().sum())


latest = (raw.sort_values('last_updated')
             .drop_duplicates('cust_no', keep='last'))


ref = pd.read_csv('data/reference/localities.csv',
                  dtype=str)
pc_ref = dict(zip(ref['suburb'], ref['postcode']))

def agrees(df):
    return (df['postcode'].str.zfill(4)
            == df['suburb'].map(pc_ref))

won = latest[latest['cust_no'].isin(rep['cust_no'])]
print('Latest rows that agree:', agrees(won).sum(),
      'of', len(won))


raw['consistent'] = agrees(raw)
best = (raw.sort_values(['consistent', 'last_updated'])
           .drop_duplicates('cust_no', keep='last'))
fixed = best[best['cust_no'].isin(rep['cust_no'])]
print('Rows left:', len(best))
print('Winners that agree:', fixed['consistent'].sum(),
      'of', len(fixed))
raw = best.drop(columns='consistent')


assert raw['cust_no'].is_unique
print(len(raw), 'customers')


products = pd.read_csv('data/raw/products.csv')
wo = wo.drop_duplicates()
joined = wo.merge(products, on='product_code',
                  how='left')
print(len(wo), '->', len(joined))


print(products[products['product_code']
               .duplicated(keep=False)])


from pandas.errors import MergeError
try:
    wo.merge(products, on='product_code',
             validate='many_to_one')
except MergeError as e:
    print(str(e).split(';')[0])


current = (products.sort_values('price')
           .drop_duplicates('product_code', keep='last'))
joined = wo.merge(current, on='product_code',
                  how='left', validate='many_to_one')
print(len(wo), '->', len(joined))


wo['customer_id'] = wo['customer_id'].replace(
    dict(zip(merge_map['old'], merge_map['new'])))


cust_ids = raw[['cust_no']].rename(
    columns={'cust_no': 'customer_id'})
check = wo.merge(cust_ids, on='customer_id',
                 how='left', indicator=True)
print(check['_merge'].value_counts())
print(sorted(check.loc[check['_merge'] == 'left_only',
                       'customer_id'].unique()))


rev = lambda d: (d['qty'] * d['unit_price']).sum()
assert len(joined) == len(wo)
assert rev(joined) == rev(wo)

