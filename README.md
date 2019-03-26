<!--[![Build Status](https://travis-ci.org/okfn/flexidate.svg?branch=master)](https://travis-ci.org/okfn/flexidate) [![codecov.io](http://codecov.io/github/okfn/flexidate/coverage.svg?branch=master)](http://codecov.io/github/okfn/flexidate?branch=master)-->


# About

The `flexidate` library supports date parsing and normalization using the `FlexiDate` class. It provides functionality to:

1. Cast dates according to the [Anno Domini](https://en.wikipedia.org/wiki/Anno_Domini) notation system (e.g., 399 BC, AD 417) as well as the [Common Era](https://en.wikipedia.org/wiki/Common_Era) notation system (e.g., 399 B.C.E, 417 CE)
1. Handle dates before  AD 1 or 1 CE
1. Cast imprecise dates (c.1860, 18??, fl. 1534, etc)
1. Normalize dates to machine-readable data types
1. Create sortable date objects

Flexidate builds on the excellent [dateutil](https://dateutil.readthedocs.org/en/latest/).

For more information see [this blog post](http://www.rufuspollock.org/2009/06/18/flexible-dates-in-python/).


# Examples

First load a string into the `parse` function, which returns a `FlexiDate` object:

``` python
>>> from flexidate import parse
>>> fd = parse('Jan 1890')
```

Once you have your date in a `FlexiDate` object, you can get access to attributes:

``` python
>>> fd.year # u'1890'
'1890'
>>> fd.month # u'01'
'01'
```

Note how all fields are retained as strings, which prevents the loss of original input data.

The `FlexiDate` object exports to other formats (e.g., `int` or `datetime`):

``` python
>>> fd.as_float()
1890.0833333333333
>>> fd.as_datetime()
datetime.datetime(1890, 1, 1, 0, 0)
```

<!--1. TODO: figure out how to do BC years and say this up top -->
To cast years before AD 1:

To case dates before Christ (i.e., Anno Domini or Common Era):

``` python
>>> fd = parse('399 BC')
>>> fd
<class 'flexidate.FlexiDate'> -0399
>>> fd.year
'-0399'
```

Or after:
``` python
>>> fd = parse('AD 417')
>>> fd
<class 'flexidate.FlexiDate'> 0417
```

Including with Common Era notation:
``` python
>>> fd_ce = parse('399 BCE')
>>> fd_ce
<class 'flexidate.FlexiDate'> -0399
>>> fd_ad = parse('399 BC')
>>> fd_ce.year == fd_ad.year
True
```

``` python
>>> fd_ce = parse('417 CE')
>>> fd_ce
<class 'flexidate.FlexiDate'> 0417
>>> fd_ad = parse('AD 417')
>>> fd_ce.year == fd_ad.year
True
```

`FlexiDate` supports hour, minute, second, and microsecond:

``` python
>>> fd = parse('417-06-01 10')
<class 'flexidate.FlexiDate'> 2016-01-06 10
>>> fd.hour
'10'
>>> fd.minute
''
```

`parse` can capture various fuzzy date attributes. In `FlexiDate` this becomes available as the attribute `qualifier`:

``` python
>>> fd = parse('417?')
>>> fd
<class 'flexidate.FlexiDate'>  [b'UNPARSED: 417?']
>>> fd.qualifier
b'UNPARSED: 417?'
```

``` python
>>> fd = parse('c. 417')
>>> fd
<class 'flexidate.FlexiDate'> 0417 [Note 'circa' : c. 417]
>>> fd.qualifier
"Note 'circa' : c. 417"
```

``` python
>>> fd = parse('177?')
>>> fd
<class 'flexidate.FlexiDate'>  [b'UNPARSED: 177?']
>>> fd.qualifier
b'UNPARSED: 177?'
```

Comparison of dates:

``` python
>>> fd1 = parse('399 BC')
>>> fd2 = parse('AD 200')
>>> fd1.year < fd2.year
True
>>> fd1.year > fd2.year
False
```


# Developers

To install required development dependencies: `pip install -r requirements.txt`.

Patches are welcome. Please include additional tests where relevant.

## Run Tests

Tests can be found in `flexidate/test_flexidate.py`. Run using `python flexidate/test_flexidate.py` or, for a full coverage report, `nosetests --no-skip --with-coverage`.

## Package

To build locally: `python setup install`.


## TODO

* ~~Cast dates written in the [Common Era](https://en.wikipedia.org/wiki/Common_Era) notation system (e.g., 399 BCE, 417 CE)~~


# License

MIT. See `LICENSE`.
