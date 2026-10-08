"""Clean the Mallee Hardware customer export (Chapter 9 of Cleaning Messy Data).

Run from the companion folder:  python scripts/clean_mallee.py
Reads  data/raw/mallee_customers.csv and data/reference/*.csv
Writes output/mallee_customers_clean.csv, output/mallee_interests.csv,
       output/mallee_merge_map.csv and output/cleaning_log.csv
"""
from pathlib import Path
Path('output').mkdir(exist_ok=True)

import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

import re
from difflib import get_close_matches

LOG = []

def log(rule, changed, reason):
    LOG.append({'step': len(LOG) + 1, 'rule': rule,
                'rows_changed': int(changed),
                'reason': reason})

def changed(before, after):
    """Rows where any value differs."""
    b = before.astype('string').fillna('<NA>')
    a = after.astype('string').fillna('<NA>')
    return (b != a).any(axis=1).sum() if b.ndim > 1 \
        else (b != a).sum()


RAW = 'data/raw/mallee_customers.csv'
df = pd.read_csv(RAW, encoding='cp1252', dtype=str,
                 keep_default_na=False)
log('Read file as Windows-1252, all text', 0,
    f'{len(df)} rows, {df.shape[1]} columns')

def tidy(s):
    return (s.str.replace('\xa0', ' ')
             .str.replace(r'\s+', ' ', regex=True)
             .str.strip())

before = df.copy()
df = df.apply(tidy)
log('Trim spaces, remove non-breaking spaces',
    changed(before, df), 'Problem 6')

n = len(df)
df = df.drop_duplicates().reset_index(drop=True)
log('Drop exact duplicate rows', n - len(df),
    'Export pages overlapped (Problem 21)')


smap = pd.read_csv('data/reference/state_map.csv')
lookup = dict(zip(smap['raw_value'].str.upper()
                  .str.replace('.', ''), smap['state']))
key = df['state'].str.upper().str.replace('.', '')
new = key.map(lookup)
log('Map state spellings to SA/NT',
    changed(df['state'], new), 'Problem 7')
df['state'] = new

new = df['postcode'].str.zfill(4)
log('Pad postcodes to 4 digits',
    changed(df['postcode'], new), 'Excel dropped zeros')
df['postcode'] = new

fixes = pd.read_csv('data/reference/suburb_fixes.csv')
new = (df['suburb'].str.title()
       .str.replace(r'^Mt\b', 'Mount', regex=True)
       .str.replace(r'^Pt\b', 'Port', regex=True)
       .replace(dict(zip(fixes['found'],
                         fixes['correct']))))
log('Standardise suburb names',
    changed(df['suburb'], new), 'Reviewed fixes table')
df['suburb'] = new


pat = (r'^(?P<last>[^,]+),\s*(?P<first>.+)$'
       r'|^(?P<first2>\S+)\s+(?P<last2>.+)$')
parts = df['full_name'].str.extract(pat)

def name_case(s):
    s = s.str.title()
    return s.str.replace(r'\bMc(\w)',
                         lambda m: 'Mc' + m[1].upper(),
                         regex=True)

df['first_name'] = name_case(
    parts['first'].fillna(parts['first2']))
df['last_name'] = name_case(
    parts['last'].fillna(parts['last2']))
log('Split full_name into first and last',
    len(df), 'Surname-first and lower-case layouts')

def clean_phone(s):
    d = s.str.replace(r'\D', '', regex=True)
    d = d.str.replace(r'^61(?=\d{9}$)', '0', regex=True)
    d = d.where(d.str.len() != 9, '0' + d)
    return d.where(d.str.fullmatch(r'0[2-478]\d{8}'))

new = clean_phone(df['phone'])
log('Standardise phone to 10 digits',
    changed(df['phone'].mask(df['phone'] == ''), new),
    'Problem 11; blanks left out of the count')
df['phone'] = new

em = df['email'].str.lower()
placeholder = em.isin(['', 'n/a', 'none', '-'])
valid = em.str.fullmatch(r'[^@\s]+@[^@\s]+\.[a-z]{2,}')
df['email_check'] = ~valid & ~placeholder
new = em.where(valid)
log('Lower-case emails; blank placeholders',
    changed(df['email'], new),
    f"{df['email_check'].sum()} flagged for checking")
df['email'] = new


jd = df['join_date']
parsed = pd.Series(pd.NaT, index=df.index,
                   dtype='datetime64[us]')
for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%b-%y']:
    parsed = parsed.fillna(pd.to_datetime(
        jd, format=fmt, errors='coerce'))
df['join_date'] = parsed
log('Parse join_date (3 formats, day first)',
    len(df), 'Problem 15')

bd = pd.to_datetime(df['birth_date'], format='%d/%m/%Y',
                    errors='coerce')
placeholder = bd == '1900-01-01'
df['birth_date'] = bd.mask(placeholder)
log('Blank 01/01/1900 birth dates',
    placeholder.sum(), 'System placeholder (Problem 19)')

df['last_updated'] = pd.to_datetime(df['last_updated'])

pts = df['loyalty_points']
df['is_member'] = pts != ''
num = pd.to_numeric(pts.str.replace(',', ''),
                    errors='coerce')
df['points_check'] = num.eq(-1)
df['loyalty_points'] = num.mask(num < 0).astype('Int64')
log('Loyalty points to numbers',
    (pts.isin(['N/A', '-1'])).sum(),
    'N/A and -1 blanked; blank = not a member')


ints = (df[['cust_no']]
        .assign(interest=df['interests']
                .str.split(r'\s*[;,]\s*'))
        .explode('interest'))
ints['interest'] = ints['interest'].str.title()
ints = ints[ints['interest'].fillna('') != '']
ints = ints.drop_duplicates()
log('Interests to a long table', len(ints),
    'One row per customer per interest')


digits = df['phone'].str[-9:]

def pairs_on(key):
    d = df.assign(k=key).dropna(subset=['k'])
    low = d.groupby('k')['cust_no'].transform('min')
    return (pd.DataFrame({'old': d['cust_no'],
                          'new': low})
            .query('old != new').drop_duplicates())

merge_map = (pd.concat([pairs_on(df['email']),
                        pairs_on(digits)])
             .drop_duplicates())
assert merge_map['old'].is_unique
df = df[~df['cust_no'].isin(merge_map['old'])]
ints = ints[~ints['cust_no'].isin(merge_map['old'])]
log('Merge same customer under 2 numbers',
    len(merge_map), 'Matched on email or phone')

ref = pd.read_csv('data/reference/localities.csv',
                  dtype=str)
pc_ref = dict(zip(ref['suburb'], ref['postcode']))
df['ok'] = df['postcode'] == df['suburb'].map(pc_ref)
n = len(df)
df = (df.sort_values(['ok', 'last_updated'])
        .drop_duplicates('cust_no', keep='last')
        .drop(columns='ok')
        .sort_values('cust_no').reset_index(drop=True))
log('Resolve repeated cust_no', n - len(df),
    'Prefer suburb matching postcode, then latest')


assert df['cust_no'].is_unique
assert df['cust_no'].str.fullmatch(r'\d{6}').all()
assert df['state'].isin(['SA', 'NT']).all()
assert df['postcode'].str.fullmatch(r'\d{4}').all()
assert df['suburb'].isin(set(ref['suburb'])).all()
assert (df['postcode']
        == df['suburb'].map(pc_ref)).all()
assert df['first_name'].notna().all()
p = df['phone'].dropna()
assert p.str.fullmatch(r'0[2-478]\d{8}').all()
assert df['join_date'].between('2018-07-01',
                               '2026-10-08').all()
assert df['birth_date'].dropna().between(
    '1910-01-01', '2010-12-31').all()
assert (df['loyalty_points'].dropna() >= 0).all()
for k in [df['email'], df['phone']]:
    assert not k.dropna().duplicated().any()
print('All checks passed')


cols = ['cust_no', 'first_name', 'last_name', 'email',
        'email_check', 'phone', 'suburb', 'postcode',
        'state', 'signup_channel', 'join_date',
        'birth_date', 'is_member', 'loyalty_points',
        'points_check', 'last_updated']
clean = df[cols]
clean.to_csv('output/mallee_customers_clean.csv',
             index=False)
ints.to_csv('output/mallee_interests.csv', index=False)
merge_map.to_csv('output/mallee_merge_map.csv',
                 index=False)
log_df = pd.DataFrame(LOG)
log_df.to_csv('output/cleaning_log.csv', index=False)
print(len(clean), 'customers written')


print(log_df[['step', 'rule', 'rows_changed']]
      .to_string(index=False))


bk = pd.read_csv('data/raw/banksia_customers.csv',
                 dtype=str)
known = clean['email'].isin(bk['email'].str.lower())
print(known.sum(), 'Mallee customers already at Banksia')


offer = clean[~known & clean['email'].notna()]
print(len(offer), 'customers get the welcome email')
print(offer.groupby('state').size())


summary = pd.Series({
    'Rows received': 1259,
    'Customers after cleaning': len(clean),
    'Valid email': clean['email'].notna().sum(),
    'Valid phone': clean['phone'].notna().sum(),
    'Already Banksia customers': known.sum(),
    'Emails to confirm': clean['email_check'].sum(),
})
print(summary.to_string())

