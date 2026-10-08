# 08_ch08_structure: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
rep = rep[rep['Store'].notna()].copy()
rep['Region'] = rep['Region'].ffill()
print(rep.shape)


print(rep.iloc[:3, [1, 3, 4, 5, 14]])


long = rep.melt(id_vars=['Region', 'Store', 'Opened'],
                var_name='month', value_name='sales')
print(len(rep), 'rows x 12 months =', len(long))
print(long.head(3))


long['month'] = pd.to_datetime(long['month'],
                               format='%b-%y')
print(long['month'].min().date(),
      long['month'].max().date())


is_text = long['sales'].map(lambda v: isinstance(v, str))
print(long.loc[is_text, ['Store', 'month', 'sales']])
long['sales'] = pd.to_numeric(
    long['sales'].astype(str)
                 .str.replace(r'[$,]', '', regex=True))
print(long['sales'].dtype)


stores = long[~long['Store'].str.contains('total')]
best = stores.loc[stores.groupby('Store')['sales']
                        .idxmax(), ['Store', 'month']]
print(best.assign(month=best['month'].dt.strftime('%b')))


wide = stores.pivot(index='Store', columns='month',
                    values='sales')
print(wide.shape)


month_cols = rep.columns[3:]
wide_total = (rep[month_cols].astype(str)
              .replace(r'[$,]', '', regex=True)
              .astype(float).sum().sum())
assert np.isclose(wide_total, long['sales'].sum())
print(f'{wide_total:,.0f}')


is_total = long['Store'].str.contains('total',
                                      case=False)
print(list(long.loc[is_total, 'Store'].unique()))


stores = long[~is_total]
check = (stores.groupby(['Region', 'month'])['sales']
         .sum().rename('stores').reset_index())
subs = long[long['Store'].str.endswith('subtotal')]
check = check.merge(
    subs[['Region', 'month', 'sales']], on=['Region',
                                            'month'])
check['diff'] = check['stores'] - check['sales']
print(check['diff'].abs().max())


grand = long[long['Store'] == 'Grand total']
by_month = stores.groupby('month')['sales'].sum()
gap = (by_month - grand.set_index('month')['sales'])
print(gap.abs().max())


sales = stores.reset_index(drop=True)
print(len(sales), 'rows;',
      f"total ${sales['sales'].sum():,.0f}")


assert not sales['Store'].str.contains('total',
                                       case=False).any()
assert not sales.duplicated(['Store', 'month']).any()
assert len(sales) == 7 * 12

