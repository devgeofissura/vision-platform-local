---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: applied-mathematics
description: Practical algebra, calculus and statistics with worked numerical examples
category: science
version: 0.1.0
author: devtiagoabreu
tags: [mathematics, algebra, calculus, statistics, examples]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic arithmetic and algebra from high school
  - A scientific calculator or spreadsheet for practice
provides:
  - Linear equations and functions with applications
  - Derivative and integral examples with interpretations
  - Descriptive statistics and probability calculations
---

# Applied Mathematics

## Overview

This skill presents the mathematics most used in engineering, data, and
business with worked numerical examples: linear functions and equations,
differential and integral calculus, and descriptive statistics with basic
probability. Every topic includes the formula, the reasoning, and a concrete
application so the method is clear, not just the symbol manipulation.

The emphasis is on interpretation: a derivative is a rate of change, an
integral is an accumulation, a standard deviation is a spread. Once those ideas
are clear, the formulas become tools.

## Prerequisites

- Comfort with basic arithmetic and fractions
- Familiarity with function notation and the concept of a variable
- A calculator or spreadsheet to reproduce the examples

## Usage Instructions

### 1. Linear Functions and Equations

Linear models describe constant-rate situations: distance at constant speed,
cost with fixed and variable parts, or simple growth. The form is
y = ax + b, where a is the slope (rate) and b is the intercept (initial value).

```text
Cost model:  C(x) = 250x + 1,200
  250 = variable cost per unit (slope)
  1,200 = fixed cost (intercept)

Break-even: revenue R(x) = 400x
  400x = 250x + 1,200  ->  150x = 1,200  ->  x = 8 units
  At 8 units cost equals revenue; below that, loss.

Two-point line through (0, 10) and (4, 30):
  slope a = (30 - 10) / (4 - 0) = 20 / 4 = 5
  y = 5x + 10

Applications:
  - Distance: d = v t  ->  v = slope of d vs t
  - Depreciation: value V(t) = 20000 - 3500t
    book value after 3 years = 20000 - 10500 = R$ 9,500
  - Currency: USD to BRL at rate 5.20, fixed fee 2.00
    BRL = 5.20 x USD + 2.00
```

### 2. Derivatives and Integrals

The derivative f'(x) measures the instantaneous rate of change; the definite
integral accumulates the area under a curve. Both appear constantly in
optimization and in computing totals from rates.

```text
Derivative examples:
  f(x) = 3x²        -> f'(x) = 6x
  f(x) = 5x + 2     -> f'(x) = 5
  f(x) = 1/x        -> f'(x) = -1/x²

Interpretation: if f is revenue in R$/week and x is weeks,
  f'(x) is the marginal revenue (extra R$ per week).

Marginal cost example:
  C(x) = 1000 + 40x + 0.5x²
  C'(x) = 40 + x  -> marginal cost at x = 60 units
  C'(60) = 40 + 60 = R$ 100 per extra unit

Definite integral examples:
  Rate r(t) = 5t (items per hour), from t=1 to t=4:
  integral(5t) dt = (5/2)t²
  from 1 to 4 = (5/2)(16 - 1) = (5/2)(15) = 37.5 items
  -> total production over 3 hours.

Area under y = x² from 0 to 3:
  integral(x²) = x³/3 -> (27/3) - 0 = 9
```

### 3. Descriptive Statistics and Probability

Statistics summarizes data with central tendency (mean, median) and spread
(variance, standard deviation). Probability gives the chance of events, with
the multiplication rule for independent events.

```text
Dataset: [4, 8, 6, 5, 9, 7]
  Mean mu = (4+8+6+5+9+7) / 6 = 39 / 6 = 6.5
  Median: sorted [4,5,6,7,8,9] -> (6+7)/2 = 6.5
  Variance = sum((xi - mu)²) / n
    = (6.25 + 2.25 + 0.25 + 2.25 + 6.25 + 0.25) / 6
    = 17.5 / 6 = 2.917
  Standard deviation sigma = sqrt(2.917) = 1.708

Coefficient of variation = sigma / mu = 1.708 / 6.5 = 0.263 (26.3%)

Probability examples:
  - Die: P(6) = 1/6
  - Independent events (A and B):
    P(two sixes) = 1/6 x 1/6 = 1/36 ≈ 2.78%
  - At least one success in n tries:
    P = 1 - (1 - p)^n ; p = 0.1, n = 10
    P = 1 - 0.9^10 = 1 - 0.3487 = 0.6513 (65.1%)
```

## Examples

### Example 1: Optimization with Derivatives

```text
Maximize profit:  Profit P(x) = -2x² + 120x - 800
Set derivative to zero:
  P'(x) = -4x + 120 = 0  ->  x = 30 units
Second derivative P''(x) = -4 < 0 -> maximum

  P(30) = -2(900) + 3600 - 800 = -1800 + 2800 = R$ 1,000
Answer: produce 30 units for maximum profit of R$ 1,000.
```

### Example 2: Compound Growth and Logarithm

```text
Investment grows continuously: A = P e^(r t)
  P = R$ 10,000, r = 8%/yr, t = 5 years
  A = 10000 x e^(0.40) = 10000 x 1.49182 = R$ 14,918.25

Doubling time: t = ln(2) / r = 0.6931 / 0.08 = 8.66 years
Rule of 72 check: 72 / 8 = 9 years (approximation)

Geometric series (total = n x annuity factor):
  Monthly payment R$ 500 for 12 months at 1% per month:
  Future value = 500 x ((1.01^12 - 1) / 0.01)
  = 500 x (1.126825 - 1) / 0.01 = 500 x 12.6825 = R$ 6,341.27
```

## Best Practices

- Write the units on every step; they catch most mistakes
- Check extreme cases: x = 0 and a large value validate the model
- Verify the sign of a derivative before declaring a max or min
- Use median instead of mean with outliers in the data
- Report the standard deviation together with the mean
- State assumptions (linearity, independence) before applying formulas

## Pitfalls / Common Mistakes

- Confusing the slope with the intercept in word problems
- Using the arithmetic mean when the growth is geometric
- Forgetting that P'(x) = 0 can also find a minimum or a saddle point
- Treating dependent events as independent in probability
- Computing variance with the population formula on a sample
- Misreading the base of a logarithm (ln vs log)

## References

- [Khan Academy - Algebra and Functions](https://www.khanacademy.org/math/algebra)
- [Paul's Online Math Notes - Calculus](https://tutorial.math.lamar.edu/classes/calci/calci.aspx)
- [MIT OpenCourseWare - Single Variable Calculus](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)
- [Khan Academy - Statistics and Probability](https://www.khanacademy.org/math/statistics-probability)
- [Wolfram Alpha (formula verification)](https://www.wolframalpha.com/)

## Notes

- Always validate hand calculations with a spreadsheet or CAS
- Numerical accuracy matters; keep 3 significant figures in engineering work
- Applied math is a toolbox: match the tool to the problem type
