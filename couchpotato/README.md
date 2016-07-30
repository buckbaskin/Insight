Current issue

```
def multiply(a, b):
  return a*b

lazy_multiply = lazify(multiply)

multiply(3, 4) == lazy_multiply(3, 4) returns False
```

type(multiply(3, 4)) -> int
type(lazy_multiply(3, 4)) -> couchpotato.decorator.Lazily
