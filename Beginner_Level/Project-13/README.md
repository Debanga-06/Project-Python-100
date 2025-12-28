# Fibonacci Sequence Generator 

Generate and analyze Fibonacci sequences with multiple algorithms, golden ratio convergence, and mathematical insights.

## Features

- **Multiple Generation Methods**: Iterative, recursive, memoized
- **Golden Ratio Analysis**: Shows convergence to φ (phi)
- **Sequence Display**: Formatted table with indices
- **Mathematical Properties**: Educational information
- **Specific Term Calculation**: Calculate any Fibonacci number
- **File Export**: Save sequences to text files
- **Performance Optimized**: Handles large sequences efficiently

## Requirements

- Python 3.x

## Installation

```bash
python fibonacci_generator.py
```

## Quick Start

```
Options:
  1. Generate sequence
  2. View Fibonacci properties
  3. Calculate specific term
  q. Quit

Your choice: 1

How many terms to generate? (1-100): 10

Fibonacci Sequence:
----------------------------------------------------------------------
     F0     F1     F2     F3     F4
      0      1      1      2      3

     F5     F6     F7     F8     F9
      5      8     13     21     34

======================================================================
SEQUENCE ANALYSIS
======================================================================

Terms Generated:    10
First Term:         0
Last Term:          34
Sum of Sequence:    88

Golden Ratio (φ):   1.618033988749895
Last Ratio F9/F8:   1.619047619047619
Difference:         1.014e-03
======================================================================
```

## The Fibonacci Sequence

### Definition
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2) for n ≥ 2

### First 20 Terms
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181

## Algorithms

### 1. Iterative (Recommended)
```python
Time: O(n) | Space: O(n)
Best for generating sequences
```

### 2. Recursive
```python
Time: O(2^n) | Space: O(n)
Educational but inefficient
```

### 3. Memoized Recursive
```python
Time: O(n) | Space: O(n)
Optimized recursive approach
```

## Mathematical Properties

1. **Recurrence Relation**: F(n) = F(n-1) + F(n-2)
2. **Golden Ratio**: lim(F(n+1)/F(n)) = φ ≈ 1.618
3. **Binet's Formula**: F(n) = (φ^n - ψ^n) / √5
4. **Divisibility**: Every kth Fibonacci is divisible by F(k)
5. **Sum Formula**: Σ F(i) from i=0 to n = F(n+2) - 1

## Applications in Nature

- **Flower Petals**: Often Fibonacci numbers (3, 5, 8, 13, 21)
- **Pine Cones**: Spirals follow Fibonacci sequence
- **Shells**: Nautilus shell follows golden spiral
- **Tree Branches**: Branching patterns
- **Galaxies**: Spiral arm patterns
- **DNA**: Double helix measurements

## Use Cases

- Algorithm study and optimization
- Golden ratio demonstrations
- Nature pattern analysis
- Mathematical education
- Sequence generation practice
- Recursion vs iteration comparison

## License

Free to use for educational purposes.