# Linq for Python

## What's that

### _Simple `Language integrated query` for Python_

This package helps you write queries on Iterable objects in python

It makes it easy to deal with iterators.

## Why should i use this?

Well you should not! i mean you don't need such thing at all. python has already fully implemented methods for iterables, but if you used to `Linq` in `C#` ( like me ), you are probably want to use such package.

## How to?

### Well it's super easy

Let's take a look at the examples

```py
from ipyquery import Linq

my_list = Linq([5, 1, 7, 2, 3, 10, 1, 4, 5])

powered_cleaned = my_list.distinct().where(
    lambda x: x <= 5).orderby().select(lambda x: x**2).tolist()

print(powered_cleaned)

# [1, 4, 9, 16, 25]
```

You can use methods to do whatever you want with your list just that easy!

## More Examples?

Take a look at [tests](tests/test_linq.py) folder ( There are a lot to explore )

## Currently available methods

> Below you can see all currently available methods, all of these can be used on `Linq` object ( which contains your list )

- `select`
- `select_many`
- `enum_select`
- `tolist`
- `todict`
- `groupby`
- `where`
- `first`
- `first_or_default`
- `any`
- `all`
- `orderby`
- `orderby_desc`
- `max`
- `min`
- `sum`
- `average`
- `distinct`
- `single`
- `single_or_default`
- `add`
- `reverse`
- `remove`
- `remove_all`

_Don't worry will add more methods._
