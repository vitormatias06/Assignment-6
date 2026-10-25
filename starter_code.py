
"""
Dynamic Programming Assignment - Longest Common Subsequence
Implement three versions: naive recursive, memoization, and tabulation.
"""

import json
import time


# ============================================================================
# PART 1: NAIVE RECURSIVE SOLUTION
# ============================================================================

def lcs_recursive(seq1, seq2):
    """
    Find the length of longest common subsequence using pure recursion.
    """

    if len(seq1) == 0 or len(seq2) == 0:
        return 0

    if seq1[-1] == seq2[-1]:
        return 1 + lcs_recursive(seq1[:-1], seq2[:-1])

    return max(
        lcs_recursive(seq1[:-1], seq2),
        lcs_recursive(seq1, seq2[:-1])
    )


# ============================================================================
# PART 2: MEMOIZATION (TOP-DOWN WITH CACHING)
# ============================================================================

def lcs_memoization(seq1, seq2):
    """
    Find the length of longest common subsequence using memoization.
    """

    cache = {}

    def solve(i, j):
        if i == 0 or j == 0:
            return 0

        if (i, j) in cache:
            return cache[(i, j)]

        if seq1[i - 1] == seq2[j - 1]:
            result = 1 + solve(i - 1, j - 1)
        else:
            result = max(
                solve(i - 1, j),
                solve(i, j - 1)
            )

        cache[(i, j)] = result
        return result

    return solve(len(seq1), len(seq2))


# ============================================================================
# PART 3: TABULATION (BOTTOM-UP WITH TABLE)
# ============================================================================

def lcs_tabulation(seq1, seq2):
    """
    Find the length of longest common subsequence using tabulation.
    """

    m = len(seq1)
    n = len(seq2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    return dp[m][n]


# ============================================================================
# TESTING & TIMING
# ============================================================================

def load_sequence(filename):
    """Load DNA sequence from JSON file."""
    with open(f"sequences/{filename}", "r") as f:
        return json.load(f)


def test_small_cases():
    """Test all implementations on small known cases."""
    print("=" * 70)
    print("TESTING ON SMALL CASES")
    print("=" * 70 + "\n")

    test_cases = [
        ("AGGTAB", "GXTXAYB", 4),
        ("ABCDGH", "AEDFHR", 3),
        ("ABC", "AC", 2),
        ("", "ABC", 0),
    ]

    for seq1, seq2, expected in test_cases:
        print(f"Test: '{seq1}' vs '{seq2}'")
        print(f"  Expected LCS length: {expected}")

        try:
            result = lcs_recursive(seq1, seq2)
            status = "PASS" if result == expected else "FAIL"
            print(f"  Recursive: {result} {status}")
        except Exception as e:
            print(f"  Recursive: ERROR - {str(e)}")

        try:
            result = lcs_memoization(seq1, seq2)
            status = "PASS" if result == expected else "FAIL"
            print(f"  Memoization: {result} {status}")
        except Exception as e:
            print(f"  Memoization: ERROR - {str(e)}")

        try:
            result = lcs_tabulation(seq1, seq2)
            status = "PASS" if result == expected else "FAIL"
            print(f"  Tabulation: {result} {status}")
        except Exception as e:
            print(f"  Tabulation: ERROR - {str(e)}")

        print()


def time_recursive():
    """Time the recursive solution on progressively larger inputs."""
    print("\n" + "=" * 70)
    print("TIMING RECURSIVE SOLUTION")
    print("=" * 70 + "\n")
    print("WARNING: Recursive solution will become very slow!\n")

    sizes = [10, 20, 50]

    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]

        print(f"Sequence length: {size}")

        start = time.perf_counter()
        result = lcs_recursive(seq1, seq2)
        elapsed = time.perf_counter() - start

        print(f"  LCS length: {result}")
        print(f"  Time: {elapsed:.4f} seconds\n")

        if elapsed > 5.0:
            print("  Stopping - recursive is too slow for larger inputs!\n")
            break


def compare_all_approaches():
    """Compare all three approaches on sequences of increasing size."""
    print("\n" + "=" * 70)
    print("COMPARING ALL APPROACHES")
    print("=" * 70 + "\n")

    sizes = [10, 20, 50, 100, 200, 500, 1000]

    print(f"{'Size':<10} {'Recursive':<15} {'Memoization':<15} {'Tabulation':<15}")
    print("-" * 70)

    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]

        times = {"size": size}

        if size <= 20:
            try:
                start = time.perf_counter()
                lcs_recursive(seq1, seq2)
                times["recursive"] = time.perf_counter() - start
            except Exception:
                times["recursive"] = None
        else:
            times["recursive"] = None

        try:
            start = time.perf_counter()
            lcs_memoization(seq1, seq2)
            times["memoization"] = time.perf_counter() - start
        except Exception:
            times["memoization"] = None

        try:
            start = time.perf_counter()
            lcs_tabulation(seq1, seq2)
            times["tabulation"] = time.perf_counter() - start
        except Exception:
            times["tabulation"] = None

        rec = times["recursive"]
        mem = times["memoization"]
        tab = times["tabulation"]

        rec_str = f"{rec:.4f}s" if rec is not None else "Too slow"
        mem_str = f"{mem:.4f}s" if mem is not None else "ERROR"
        tab_str = f"{tab:.4f}s" if tab is not None else "ERROR"

        print(f"{size:<10} {rec_str:<15} {mem_str:<15} {tab_str:<15}")


if __name__ == "__main__":
    print("DYNAMIC PROGRAMMING ASSIGNMENT")
    print("Testing the three LCS implementations.\n")

    test_small_cases()

    # Uncomment these when you are ready to benchmark:
    # time_recursive()
    compare_all_approaches()
