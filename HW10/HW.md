# Implementing Price Class

> _Remember we had a class `Price`, where we've been doing math operations with `Price` classes?_

You Must:

- Implement a `Price` class:
  - two `Price` instances (with the same currency) must support ADDITION and SUBTRACTION
  - IF currencies are DIFFERENT, apply MIDDLE CONVERSION logic (through "CHF")
    - `self.currency` -> CONVERT to CHF
    - `other.currency` -> CONVERT to CHF
    - make the OPERATION (sum/subtract)
    - CONVERT result to `self.currency` (original currency of LEFT OPERAND)
- Alphavantage API is used
  - link: https://www.alphavantage.co
  - you have to INVESTIGATE API docs and use RATES FROM THIS API's (alphavantage) response to perform currency exchange in your application

> _P.S. your reference is what we had been doing on this lesson_

code example

```python
a = Price(100, "USD")
b = Price(150, "UAH")

c = a + b
```
