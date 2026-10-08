# 03_ch03_text: code examples from the book
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


text_cols = ['full_name', 'email', 'suburb', 'state']
for col in text_cols:
    s = raw[col]
    print(f'{col:10}',
          'edge:', (s != s.str.strip()).sum(),
          'double:', s.str.contains('  ').sum(),
          'nbsp:', s.str.contains('\xa0').sum())


def tidy(s):
    return (s.str.replace('\xa0', ' ')
             .str.replace(r'\s+', ' ', regex=True)
             .str.strip())

for col in text_cols:
    raw[col] = tidy(raw[col])
print(raw['state'].nunique())


for col in text_cols:
    s = raw[col]
    assert (s == s.str.strip()).all()
    assert not s.str.contains('  |\xa0').any()


print(raw['state'].value_counts())


key = raw['state'].str.upper().str.replace('.', '')
print(key.value_counts())


smap = pd.read_csv('data/reference/state_map.csv')
smap['key'] = (smap['raw_value'].str.upper()
               .str.replace('.', ''))
lookup = dict(zip(smap['key'], smap['state']))
raw['state'] = key.map(lookup)
print(raw['state'].value_counts(dropna=False))


assert raw['state'].isin(['SA', 'NT']).all()


ref = pd.read_csv('data/reference/localities.csv',
                  dtype=str)
known = set(ref['suburb'])
unknown = raw.loc[~raw['suburb'].isin(known), 'suburb']
print(unknown.value_counts())


sub = raw['suburb'].str.title()
sub = sub.str.replace(r'^Mt\b', 'Mount', regex=True)
sub = sub.str.replace(r'^Pt\b', 'Port', regex=True)
left = sorted(set(sub) - known)
print(*left, sep='\n')


from difflib import get_close_matches

suggest = {v: get_close_matches(v, known, n=1,
                                cutoff=0.8)
           for v in left}
for v, m in suggest.items():
    print(f'{v:16} -> {m[0] if m else "?"}')


fixes = pd.DataFrame(
    [(k, v[0]) for k, v in suggest.items() if v],
    columns=['found', 'correct'])
fixes.loc[len(fixes)] = ['Victor Hbr', 'Victor Harbor']
fixes.to_csv('output/suburb_fixes.csv', index=False)
sub = sub.replace(dict(zip(fixes['found'],
                           fixes['correct'])))
raw['suburb'] = sub
print(raw['suburb'].isin(known).all())


pc_ref = dict(zip(ref['suburb'], ref['postcode']))
pc = raw['postcode'].str.zfill(4)
mismatch = pc != raw['suburb'].map(pc_ref)
print('Rows that disagree:', mismatch.sum())
repeated = raw['cust_no'].duplicated(keep=False)
print('All repeated cust_no:',
      repeated[mismatch].all())


print(*raw['interests'].sample(6, random_state=4),
      sep='\n')


print(raw['interests'].str.contains('[;,]').sum())


ints = (raw[['cust_no', 'interests']]
        .assign(interest=raw['interests']
                .str.split(r'\s*[;,]\s*'))
        .explode('interest'))
ints['interest'] = ints['interest'].str.strip().str.title()
ints = ints[ints['interest'] != '']
ints = (ints.drop_duplicates(['cust_no', 'interest'])
            .reset_index(drop=True))
print(ints[['cust_no', 'interest']].head(4))
print(ints['interest'].value_counts())


flags = pd.crosstab(ints['cust_no'], ints['interest'])
print(flags.head(3))


allowed = {'Garden', 'Kitchen', 'Outdoor', 'Tools',
           'Lighting', 'Pets'}
assert set(ints['interest']) <= allowed
assert not ints.duplicated(['cust_no',
                            'interest']).any()


print(*raw['full_name'].sample(6, random_state=2),
      sep='\n')


nm = raw['full_name']
print('Surname first:', nm.str.contains(',').sum())
print('All lower:', (nm == nm.str.lower()).sum())
print('All upper:', (nm == nm.str.upper()).sum())


pat = (r'^(?P<last>[^,]+),\s*(?P<first>.+)$'
       r'|^(?P<first2>\S+)\s+(?P<last2>.+)$')
parts = nm.str.extract(pat)
first = parts['first'].fillna(parts['first2'])
last = parts['last'].fillna(parts['last2'])
print(first.isna().sum(), last.isna().sum())


def name_case(s):
    s = s.str.title()
    return s.str.replace(r'\bMc(\w)',
                         lambda m: 'Mc' + m[1].upper(),
                         regex=True)

raw['first_name'] = name_case(first)
raw['last_name'] = name_case(last)
check = raw['last_name'].str.contains("Mc|’")
print(raw.loc[check, 'last_name'].value_counts())


for col in ['first_name', 'last_name']:
    s = raw[col]
    assert s.notna().all()
    assert not (s == s.str.upper()).any()
    assert not (s == s.str.lower()).any()


print(*raw['phone'].sample(6, random_state=9), sep='\n')


def clean_phone(s):
    d = s.str.replace(r'\D', '', regex=True)
    d = d.str.replace(r'^61(?=\d{9}$)', '0', regex=True)
    d = d.where(d.str.len() != 9, '0' + d)
    ok = d.str.fullmatch(r'0[2-478]\d{8}')
    return d.where(ok)

raw['phone_clean'] = clean_phone(raw['phone'])
print(raw[['phone', 'phone_clean']].head(5))


blank = raw['phone'] == ''
failed = raw['phone_clean'].isna() & ~blank
print('Blank:', blank.sum(), ' Failed:', failed.sum())


em = raw['email'].str.strip().str.lower()
valid = em.str.fullmatch(r'[^@\s]+@[^@\s]+\.[a-z]{2,}')
print(em[~valid].value_counts().head(6))
raw['email_clean'] = em.where(valid)


p = raw['phone_clean'].dropna()
assert p.str.fullmatch(r'0\d{9}').all()
e = raw['email_clean'].dropna()
assert (e == e.str.strip().str.lower()).all()
print(raw['email_clean'].notna().mean().round(3))

