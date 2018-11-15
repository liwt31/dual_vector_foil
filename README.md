# dual_vector_foil
[![Build Status](https://travis-ci.org/liwt31/dual_vector_foil.svg?branch=master)](https://travis-ci.org/liwt31/dual_vector_foil)
[![PyPI version](https://badge.fury.io/py/dvf.svg)](https://badge.fury.io/py/dvf)

A dual vector foil（[二向箔](https://zh.wikipedia.org/wiki/%E4%B8%89%E4%BD%93%E7%94%A8%E8%AF%AD%E5%88%97%E8%A1%A8#%E4%BA%8C%E5%90%91%E7%AE%94)） that squashes any Python objects into your console

## Introduction

Simply speaking, `dvf` (dual vector foil) is a recursive pretty printer for any objects in Python. It allows you to inspect Python object in a simple and comprehensive way. Checkout the following example:

![simple2](https://user-images.githubusercontent.com/22628546/48036479-9295a680-e1a3-11e8-9847-449d3e5310ae.gif)

## Example on Flask app

`Flask` app is very complex Python object, and `dvf` can use paging (`less`) to wrap the output. If the GIF doesn't show immediately, be patient, it's about 10 MB large (click to zoom in):

![complex4](https://user-images.githubusercontent.com/22628546/47995242-9851a480-e12f-11e8-9e2d-499756b3fdb4.gif)

If your eyes are sharp enough, you'll find a warning at the end of the gif. That's because `dvf` tries to access some attributes of `Flask` that are only valid in a request context. The warning is quite common for complex objects.

## Installation 

```
pip install dvf
```

The project is still under development, so any report on bugs is highly appreciated. 
The development is under Python 3.7 and Python 3.6 is also tested. The package provides **no Python <= 3.5 support**.

## Philosophy

#### Why not `dir` or `__dict__`

There is already an amazing inspection package [`pdir`](https://github.com/laike9m/pdir2), which emphasize on the **usage** of modules and objects, while `dvf` is aiming at **data and internal structure** of objects. 
As a result, `dvf` will by default omit any object attributes that have type of function, module or class, and will try its best to expand any iterable to see what really lies in .

#### Safety concern
As you might have gaused, it's not wise to use `dvf` on untrusted object because `dvf` will have to evoke some methods of the object to evaluate attributes. Is this a foundamental flaw of `dvf`? I think not.
Because if an object is really malicious, it can delete your system when it's imported, why wait untill `dvf` to check it?

#### Deal with loops
The biggest problem of `dvf` is loops in objects. The following class has a pointer points to himself. A simple recursion implementation of `dvf` will result in an infinite loop.
```python
class Foo:

    def __init__(self):
        self.another_me = self
```
To solve this economically, `dvf` records every object it has visited and omit them next time it meet the object. That's why sometimes a complete view of certain objects is not possible.

Another troublesome case is object creation during attribute access. A typical example is `NumPy` array, which has an attribute of `T` that returns the transpose of the array, 
which has another `T` that returns another new array. So there is also an infinite loop. To solve this `dvf` should be very cautious toward data descriptors. Some result gained from descriptors will not be expanded.

## Todo list
- [ ] User-custom searching and filtering
- [ ] Docs on output format
- [x] Tests
- [ ] Use `prompt_toolkit` to build an application that can handle wide output (horizontally scollable)
