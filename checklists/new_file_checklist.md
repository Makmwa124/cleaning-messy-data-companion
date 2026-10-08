# New-file checklist

From *Cleaning Messy Data* by Mathew Kariuki. Problem numbers refer to the book.

Run through this list the first time you receive any file. It takes ten to twenty minutes and finds most problems before they reach a report. 

**Before you open it**

- [ ] Save the file, untouched, in a raw folder. Note who sent it, when, and what system it came from.
- [ ] Ask what one row represents, and which column (if any) should be unique.

**Reading it**

- [ ] Read everything as text (`dtype=str, keep_default_na=False`).
- [ ] Encoding errors or odd characters? Try `utf-8`, then `cp1252`. (Problem 1)
- [ ] Header on the first row? Any notes or totals at the bottom? (Problems 2 and 30)
- [ ] Right number of columns? Check the separator and decimal mark. (Problem 3)

**Profiling it**

- [ ] Rows and columns as expected? Compare with what the sender says.
- [ ] Filled, blank and unique counts for every column. (Chapter 1)
- [ ] `value_counts()` for every column with few distinct values. (Problems 6, 7, 12)
- [ ] One random row on its side, three or four times.
- [ ] Exact duplicates, and repeats in the column that should be unique. (Problems 21, 23)

**Checking each kind of column**

- [ ] Identifiers and codes: fixed length? Leading zeros? (Problem 5)
- [ ] Text: spaces, case, spellings against a reference list. (Problems 6 to 8)
- [ ] Numbers: which values fail to convert? Units? Sentinels? Extremes? (Problems 4, 25 to 27)
- [ ] Dates: shapes, ranges, placeholders, time zone. (Problems 15 to 19)
- [ ] Missing values: disguised? Patterned by group? What does blank mean? (Problems 12, 13)
- [ ] Layout: lists in cells, wide columns, label gaps, totals. (Problems 9, 14, 29, 30)

**Before you deliver**

- [ ] Every fix is in a script, in a sensible order. (Chapter 1, Habit 4)
- [ ] Every assumption is an `assert`. (Chapter 9)
- [ ] Row counts and key totals reconciled with the source.
- [ ] Cleaning log written, and the issue list sent to whoever owns the source.

