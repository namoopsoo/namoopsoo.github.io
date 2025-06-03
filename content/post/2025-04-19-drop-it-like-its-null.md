---
title: Drop it Like It's null
date: 2025-04-19
---

Arghh ha ha I have been messing around with trying to understand why the transactions I see on my Tiller from my credit card, are not as many as what I see when I pull the csv of transactions straight from my credit card website.

Dohh.

During my data wrangling,  I had to manually copy and paste transactions out of my Google Sheets, because Google Sheets oddly enough does not have the capability of "exporting as csv" what has undergone a data filter. So you are awkwardly forced to manually copy and paste it out.

But then because after pasting into a file locally, lots of rows ended up as empties, and when I was 

```python
tillerdf = pl.read_csv("from_tiller.csv")
```
I just decided to 

```python
tillerdf = pl.read_csv("from_tiller.csv").drop_nulls()
```
probably out of sheer laziness haha. 

But a day later I am scratching my head why the amounts did not match,

```python
tillerdf = pl.read_csv("from_tiller.csv").drop_nulls()
rawdf = pl.read_csv("from_credit_card_website.csv")
```
the tillerdf fell short by a hunk of what was in the rawdf.

### Why
Because the `drop_nulls()` was not just dropping the fully null rows but also rows that have even just one null and in my case here , it was that some number of rows on Tiller, I had not categorized ! 🤦‍♂️ and so they were dropped.

However in the process of debugging, I also found a cool concept in polars I had not known about 

### In polars, how to filter for what would have been dropped
per this neat toy example, from the "Polars Docs AI" engine, from an answer to a question I asked on this topic.
```python
# Example DataFrame
df = pl.DataFrame({
    "foo": [1, 2, 3, None, 4],
    "bar": [6, None, 8, None, 9],
    "ham": ["a", "b", None, "d", "e"]
})

# This shows rows that WOULD be dropped by drop_nulls()
dropped_rows = df.filter(pl.any_horizontal(pl.all().is_null()))
print(dropped_rows)
print(toydf)
```
```
shape: (3, 3)
┌──────┬──────┬──────┐
│ foo  ┆ bar  ┆ ham  │
│ ---  ┆ ---  ┆ ---  │
│ i64  ┆ i64  ┆ str  │
╞══════╪══════╪══════╡
│ 2    ┆ null ┆ b    │
│ 3    ┆ 8    ┆ null │
│ null ┆ null ┆ d    │
└──────┴──────┴──────┘
shape: (5, 3)
┌──────┬──────┬──────┐
│ foo  ┆ bar  ┆ ham  │
│ ---  ┆ ---  ┆ ---  │
│ i64  ┆ i64  ┆ str  │
╞══════╪══════╪══════╡
│ 1    ┆ 6    ┆ a    │
│ 2    ┆ null ┆ b    │
│ 3    ┆ 8    ┆ null │
│ null ┆ null ┆ d    │
│ 4    ┆ 9    ┆ e    │
└──────┴──────┴──────┘
```

### dropping only if all columns are null
per the documentation this appears to be a bit verbose 

```python
result = df.filter(~pl.all_horizontal(pl.all().is_null()))
```
