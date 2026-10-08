# 05_ch05_dates: code examples from the book
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


print(pd.to_datetime('04/05/2020'))


def shape(s):
    return (s.str.replace(r'\d', '9', regex=True)
             .str.replace(r'[A-Za-z]', 'A', regex=True))

print(shape(raw['join_date']).value_counts())


jd = raw['join_date']
formats = ['%d/%m/%Y', '%Y-%m-%d', '%d-%b-%y']
parsed = pd.Series(pd.NaT, index=jd.index,
                   dtype='datetime64[us]')
for fmt in formats:
    attempt = pd.to_datetime(jd, format=fmt,
                             errors='coerce')
    parsed = parsed.fillna(attempt)
print(parsed.isna().sum())
raw['join_date'] = parsed


guess = pd.to_datetime(jd, errors='coerce')
wrong = (guess != parsed) & guess.notna()
print('Dates pandas got wrong:', wrong.sum())
print(pd.DataFrame({'text': jd, 'guess': guess,
                    'correct': parsed})[wrong].head(3))


assert raw['join_date'].notna().all()
print(raw['join_date'].min().date(),
      raw['join_date'].max().date())


rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
opened = rep.loc[rep['Store'].notna()
                 & ~rep['Store'].str.contains('total'),
                 ['Store', 'Opened']]
print(opened)


op = opened['Opened']
is_num = op.map(lambda v: isinstance(v, (int, float)))
from_serial = pd.to_datetime(
    pd.to_numeric(op.where(is_num)),
    unit='D', origin='1899-12-30')
from_text = pd.to_datetime(op.where(~is_num),
                           format='%Y-%m-%d')
opened['Opened'] = from_serial.fillna(from_text)
print(opened)


assert opened['Opened'].between('2010-01-01',
                                '2026-12-31').all()


s = pd.Series(['04-Mar-25', '15-Jun-62', '01-Jan-69'])
print(pd.to_datetime(s, format='%d-%b-%y'))


today = pd.Timestamp('2026-10-08')
print((raw['join_date'] > today).sum())


births = pd.to_datetime(s, format='%d-%b-%y')
births = births.mask(births > today,
                     births - pd.DateOffset(years=100))
print(births)


assert (births <= today).all()


wo = pd.read_csv('data/raw/web_orders.csv',
                 dtype={'customer_id': str})
print(*wo['order_ts_utc'].head(3), sep='\n')


ts = pd.to_datetime(wo['order_ts_utc'], utc=True)
wo['order_local'] = ts.dt.tz_convert('Australia/Adelaide')
print(wo[['order_ts_utc', 'order_local']].head(3))


for t in ['2026-04-04 14:00', '2026-04-05 14:00']:
    utc = pd.Timestamp(t, tz='UTC')
    print(utc, '->',
          utc.tz_convert('Australia/Adelaide'))


utc_day = ts.dt.date
local_day = wo['order_local'].dt.date
moved = (utc_day != local_day).mean()
print(f'Orders on a different date: {moved:.1%}')
daily = pd.DataFrame({
    'utc': utc_day.value_counts(),
    'local': local_day.value_counts()}).fillna(0)
print(daily.astype(int).loc[pd.to_datetime(['2026-03-14']).date])


assert (wo['order_local'].iloc[0].strftime('%H:%M')
        == '10:46')


bd = pd.to_datetime(raw['birth_date'],
                    format='%d/%m/%Y', errors='coerce')
print(bd.min(), bd.max())
print(bd.value_counts().head(3))


lu = pd.to_datetime(raw['last_updated'])
print((lu < raw['join_date']).sum(),
      'records updated before they were created')


bd = bd.mask(bd == '1900-01-01')
age = (today - bd).dt.days / 365.25
print(age.describe().round(1))


assert bd.dropna().between('1910-01-01',
                           '2010-12-31').all()
assert (raw['join_date'] >= '2018-07-01').all()


parts = pd.DataFrame({'year': [2026, 2026],
                      'month': [3, 7],
                      'day': [15, 1]})
print(pd.to_datetime(parts))


d = pd.Series(pd.to_datetime(['2025-06-30',
                              '2025-07-01',
                              '2026-03-15']))
fq = d.dt.to_period('Q-JUN')
print(pd.DataFrame({'date': d, 'fy_quarter': fq,
                    'fy': fq.dt.qyear}))

