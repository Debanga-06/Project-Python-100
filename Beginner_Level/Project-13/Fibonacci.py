"""
Fibonacci Sequence Generator 
Generate Fibonacci numbers with multiple display options and analysis.
"""


def generate_fibonacci_iterative(n):
    """
    Generate first n Fibonacci numbers using iterative approach.
    Most efficient for generating sequences.
    
    Args:
        n (int): Number of terms to generate
    
    Returns:
        list: List of Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib


def fibonacci_recursive(n):
    """
    Calculate nth Fibonacci number recursively.
    Educational but inefficient for large n.
    
    Args:
        n (int): Position in sequence (0-indexed)
    
    Returns:
        int: Fibonacci number at position n
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_with_memoization(n, memo=None):
    """
    Calculate nth Fibonacci number with memoization.
    Optimized recursive approach.
    
    Args:
        n (int): Position in sequence
        memo (dict): Memoization cache
    
    Returns:
        int: Fibonacci number at position n
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_with_memoization(n - 1, memo) + fibonacci_with_memoization(n - 2, memo)
    return memo[n]


def golden_ratio_approximation(fib_sequence):
    """
    Calculate golden ratio approximations from Fibonacci sequence.
    
    Args:
        fib_sequence (list): Fibonacci sequence
    
    Returns:
        list: List of ratios between consecutive terms
    """
    if len(fib_sequence) < 2:
        return []
    
    ratios = []
    for i in range(1, len(fib_sequence)):
        if fib_sequence[i-1] != 0:
            ratio = fib_sequence[i] / fib_sequence[i-1]
            ratios.append(ratio)
    
    return ratios


def display_sequence(fib_sequence, show_indices=True):
    """Display Fibonacci sequence in formatted rows."""
    print("\nFibonacci Sequence:")
    print("-" * 70)
    
    for i in range(0, len(fib_sequence), 5):
        row = fib_sequence[i:i+5]
        if show_indices:
            indices = [f"F{j}" for j in range(i, min(i+5, len(fib_sequence)))]
            print("  " + "  ".join(f"{idx:>6}" for idx in indices))
        
        print("  " + "  ".join(f"{num:>6}" for num in row))
        print()


def display_analysis(fib_sequence):
    """Display mathematical analysis of the sequence."""
    print("\n" + "=" * 70)
    print("SEQUENCE ANALYSIS")
    print("=" * 70)
    
    n = len(fib_sequence)
    print(f"\nTerms Generated:    {n}")
    print(f"First Term:         {fib_sequence[0]}")
    print(f"Last Term:          {fib_sequence[-1]:,}")
    
    if n >= 2:
        print(f"Sum of Sequence:    {sum(fib_sequence):,}")
    
    # Golden ratio convergence
    if n >= 10:
        ratios = golden_ratio_approximation(fib_sequence)
        golden_ratio = 1.618033988749895  # φ (phi)
        
        print(f"\nGolden Ratio (φ):   {golden_ratio:.15f}")
        print(f"Last Ratio F{n-1}/F{n-2}:  {ratios[-1]:.15f}")
        print(f"Difference:         {abs(ratios[-1] - golden_ratio):.15e}")
        
        # Show convergence for last 5 ratios
        print("\nRatio Convergence (last 5):")
        for i in range(max(0, len(ratios) - 5), len(ratios)):
            idx = i + 1
            print(f"  F{idx}/F{idx-1} = {ratios[i]:.10f}")
    
    print("=" * 70)


def display_properties():
    """Display interesting Fibonacci properties."""
    print("\n" + "=" * 70)
    print("FIBONACCI SEQUENCE PROPERTIES")
    print("=" * 70)
    
    properties = [
        "1. Each term is the sum of the two preceding terms",
        "2. Ratio of consecutive terms approaches Golden Ratio (φ ≈ 1.618)",
        "3. Every 3rd number is divisible by 2",
        "4. Every 4th number is divisible by 3",
        "5. Every 5th number is divisible by 5",
        "6. F(n)^2 + F(n+1)^2 = F(2n+1)",
        "7. Sum of first n terms = F(n+2) - 1",
        "8. Appears in nature: flowers, shells, galaxies",
    ]
    
    for prop in properties:
        print(f"  {prop}")
    
    print("=" * 70)


def export_to_file(fib_sequence, filename="fibonacci.txt"):
    """Export sequence to a text file."""
    try:
        with open(filename, 'w') as f:
            f.write("Fibonacci Sequence\n")
            f.write("=" * 50 + "\n\n")
            
            for i, num in enumerate(fib_sequence):
                f.write(f"F({i}) = {num}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"Total terms: {len(fib_sequence)}\n")
            f.write(f"Sum: {sum(fib_sequence)}\n")
        
        print(f"\n✓ Sequence exported to '{filename}'")
        return True
    except Exception as e:
        print(f"\n❌ Error exporting file: {str(e)}")
        return False


def main():
    """Main program execution."""
    print("=" * 70)
    print("              FIBONACCI SEQUENCE GENERATOR")
    print("=" * 70)
    print("\nThe Fibonacci Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...")
    print("Each number is the sum of the two preceding numbers.")
    
    while True:
        print("\n" + "-" * 70)
        print("Options:")
        print("  1. Generate sequence")
        print("  2. View Fibonacci properties")
        print("  3. Calculate specific term")
        print("  q. Quit")
        print("-" * 70)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("\nThank you for exploring Fibonacci numbers!")
            break
        
        try:
            if choice == '1':
                # Generate sequence
                n = int(input("\nHow many terms to generate? (1-100): "))
                
                if n < 1:
                    print("\n❌ Please enter a positive number.")
                    continue
                
                if n > 100:
                    print("\n⚠️  Large sequences may display slowly.")
                    confirm = input("    Continue? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                
                print(f"\nGenerating first {n} Fibonacci numbers...")
                fib_sequence = generate_fibonacci_iterative(n)
                
                display_sequence(fib_sequence)
                display_analysis(fib_sequence)
                
                # Export option
                export = input("\nExport to file? (y/n): ")
                if export.lower() == 'y':
                    filename = input("Filename (default: fibonacci.txt): ").strip()
                    if not filename:
                        filename = "fibonacci.txt"
                    export_to_file(fib_sequence, filename)
            
            elif choice == '2':
                # Display properties
                display_properties()
            
            elif choice == '3':
                # Calculate specific term
                n = int(input("\nEnter term position (0-indexed): "))
                
                if n < 0:
                    print("\n❌ Please enter a non-negative number.")
                    continue
                
                if n > 1000:
                    print("\n⚠️  Large terms may take time to compute.")
                    confirm = input("    Continue? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                
                print("\nCalculating...")
                result = fibonacci_with_memoization(n)
                
                print("\n" + "=" * 70)
                print(f"F({n}) = {result:,}")
                print("=" * 70)
                
                # Show context
                if n >= 2:
                    prev1 = fibonacci_with_memoization(n - 1)
                    prev2 = fibonacci_with_memoization(n - 2)
                    print(f"\nCalculation: F({n}) = F({n-1}) + F({n-2})")
                    print(f"            {result:,} = {prev1:,} + {prev2:,}")
            
            else:
                print("\n❌ Invalid choice. Please enter 1, 2, 3, or q.")
        
        except ValueError:
            print("\n❌ Error: Please enter valid integer values.")
        except RecursionError:
            print("\n❌ Error: Number too large for recursive calculation.")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()