# nada-data
Python library to enable tabular data operations with `nada_dsl`.

## Purpose

The library can be imported in the usual way:
```python
import nada_data
from nada_data import *
```

The library provides two basic types: `NadaArray` and `NadaTable`. The `NadaArray` type is analogous
to Python's builtin `list` type, and can be created as follows:
```python
from nada_dsl import SecretInteger, Input, Party
from nada_data import NadaArray

party = Party(name="me")

# can be instantiated as comma-separated list of values
arr = NadaArray(
    SecretInteger(Input(name="int1", party=party)),
    SecretInteger(Input(name="int2", party=party))
)

# OR from list
values = [SecretInteger(Input(name="int1", party=party)), SecretInteger(Input(name="int2", party=party))]
arr = NadaArray(values)

# OR as list comp from list
arr = NadaArray(v for v in values)

>>> arr
NadaArray | len=2 | parties=['me']
```

This library provides utility functions that are normally available to the `list` type:
```python
from nada_data import sum_nada_array, filter_nada_array, nada_gt

s = sum_nada_array(arr) # outputs single SecretInteger

new_party = Party(name="new_party")
f = filter_nada_array(arr, nada_gt, SecretInteger(Input(name="int3", party=new_party)))

>>> f
NadaArray | len=2 | parties=['me', 'new_party']
```

The `NadaTable` type is a tabular data structure that enables relational workflows over arrays of `SecretInteger`
instances. Accordingly, it is instantiated from an array of `NadaArray` objects and a comma-separated list of
column names:
```python
from nada_data import NadaTable

rows = [
    NadaArray(SecretInteger(Input(name="int1", party=party)), SecretInteger(Input(name="int2", party=party))),
    NadaArray(SecretInteger(Input(name="int3", party=new_party)), SecretInteger(Input(name="int4", party=new_party)))
]

tbl = NadaTable(
    "a", "b", rows=rows
)
>>> tbl
NadaTable | cols=['a','b'] | rows=2 | parties=['me','new_party']
```

The `NadaTable` type provides relational-style functions that one would expect from something like a SQl table:
```python

col = tbl.select("a")
>>> col
NadaTable | cols=['a'] | rows=2 | parties=['me', 'new_party']

tbl.aggregate_sum(key_col="a", agg_col="b")
>>> tbl
NadaTable | cols=['a','b'] | rows=2 | parties=['me','new_party']
```

## Development

All installation and development dependencies are fully specified in pyproject.toml. The project.optional-dependencies
object is used to specify optional requirements for various development tasks. This makes it possible to specify 
additional options (such as docs, lint, and so on) when performing installation using pip:
```shell
python -m pip install .[docs,lint]
```

### Testing and Conventions 

All unit tests are executed using a combination of `doctest` and `unittest`. Both can be run as follows:
```shell
python -m unittest discover -s tests
```

Coverage can be measured as the tests are run using `coverage`:
```shell
python -m pip install .[test]
coverage run -m unittest discover -s tests
coverage report
```