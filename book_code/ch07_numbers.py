# 07_ch07_numbers: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

wo = (pd.read_csv('data/raw/web_orders.csv',
                  dtype={'customer_id': str})
      .drop_duplicates().reset_index(drop=True))
products = (pd.read_csv('data/raw/products.csv')
            .sort_values('price')
            .drop_duplicates('product_code', keep='last'))
print(len(wo), 'orders')


print(wo['weight_unit'].value_counts())
print(wo.groupby('weight_unit')['ship_weight']
        .median())


wo = wo.merge(products[['product_code', 'price']],
              on='product_code', validate='many_to_one')
ratio = (wo['unit_price'] / wo['price']).round(2)
print(ratio.value_counts().head())


in_g = wo['weight_unit'] == 'g'
wo.loc[in_g, 'ship_weight'] /= 1000
wo['weight_unit'] = 'kg'

in_cents = ratio >= 50
wo.loc[in_cents, 'unit_price'] /= 100
wo['price_was_cents'] = in_cents
print(in_g.sum(), 'weights and', in_cents.sum(),
      'prices converted')


r = wo['unit_price'] / wo['price']
assert r.between(0.9, 1.1).all()


print(wo['qty'].value_counts().sort_index())


wo = wo.merge(products[['product_code', 'weight_kg']],
              on='product_code')
implied = wo['weight_kg'] * wo['qty']
odd = wo['qty'].isin([999, -1])
print(wo.loc[odd, ['qty', 'ship_weight']]
        .assign(implied=implied[odd]).head(4))


wo['qty_sentinel'] = wo['qty'].isin([999, -1])
wo['qty'] = wo['qty'].mask(wo['qty_sentinel'])
print(wo['qty'].describe().round(2))


assert wo['qty'].dropna().between(1, 500).all()


q1, q3 = wo['qty'].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
print(f'Q1={q1} Q3={q3} IQR={iqr} upper={upper}')
print((wo['qty'] > upper).sum(), 'flagged')


med = wo['qty'].median()
mad = (wo['qty'] - med).abs().median()
robust_z = (wo['qty'] - med) / (1.4826 * mad)
print(wo.loc[robust_z.abs() > 5,
             ['order_id', 'product_code', 'qty']])


big = robust_z.abs() > 5
print(wo.loc[big, ['qty', 'ship_weight']]
        .assign(implied=implied[big]))


print(round(wo['qty'].mean(), 2),
      round(wo.loc[~big, 'qty'].mean(), 2),
      wo['qty'].median())


print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)


lines = wo['qty'].fillna(0) * wo['unit_price']
ex_line = (lines / 1.1).round(2).sum()
ex_total = round(lines.sum() / 1.1, 2)
print(f'{ex_line:,.2f}  {ex_total:,.2f}  '
      f'diff {ex_line - ex_total:.2f}')


print(round(0.125, 2), round(0.375, 2))
print(round(2.675, 2))


a, b = 0.1 + 0.2, 0.3
print(abs(a - b) < 0.005, np.isclose(a, b))


from decimal import Decimal, ROUND_HALF_UP
x = Decimal('2.675')
print(x.quantize(Decimal('0.01'),
                 rounding=ROUND_HALF_UP))


diff = abs(ex_line - ex_total)
assert diff < 0.01 * len(wo), 'More than rounding'
print(f'Rounding difference: ${diff:.2f}')

