#!/usr/bin/env python3
"""
White-Box Tests for ICSC
Tests internal logic paths and code coverage for complex functions.

Functions selected for white-box testing:
1. calculate_cost() - Complex tiered pricing logic with multiple branches
2. parse_service_entry() - Complex parsing with multiple error conditions

These functions were chosen because they contain:
- Multiple conditional branches
- Loop constructs
- Error handling paths
- Edge cases in logic flow
"""

import sys

# Import modules to test
from cost_calculator import calculate_cost, find_tier_index
from service_loader import parse_service_entry


class WhiteBoxTestResults:
    """Class to track white-box test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, test_name, path_tested, passed, expected, actual):
        self.tests.append({
            'name': test_name,
            'path': path_tested,
            'passed': passed,
            'expected': expected,
            'actual': actual
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "="*70)
        print("WHITE-BOX TEST RESULTS")
        print("="*70)
        for test in self.tests:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"{status}: {test['name']}")
            print(f"  Path: {test['path']}")
            if not test['passed']:
                print(f"  Expected: {test['expected']}")
                print(f"  Got: {test['actual']}")
        print("="*70)
        print(f"Total: {self.passed + self.failed} tests")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print("="*70)


def run_wb_test(results, test_name, path_tested, actual, expected):
    """Helper function to run a single white-box test."""
    passed = actual == expected
    results.add_result(test_name, path_tested, passed, expected, actual)
    return passed


# ============================================================================
# WHITE-BOX TEST SECTION 1: calculate_cost() - Tiered Pricing Logic
# ============================================================================
# 
# Function: calculate_cost(amount, tiers, costs)
# 
# Code paths to test:
# PATH 1: amount < 0 → return 0.0
# PATH 2: amount == 0 → return 0.0
# PATH 3: amount > 0 → find_tier_index() → calculate with tier cost
#   - Subpath 3a: amount in first tier
#   - Subpath 3b: amount exactly at tier boundary
#   - Subpath 3c: amount between boundaries
#   - Subpath 3d: amount in last (open-ended) tier
#
# Loop coverage in find_tier_index():
# - Loop through tiers from highest to lowest
# - Test loop entry, body execution, and exit conditions
# ============================================================================

def test_calculate_cost_whitebox(results):
    """White-box tests for calculate_cost() covering all code paths."""
    print("\n--- WHITE-BOX TESTING: cost_calculator.calculate_cost() ---")
    print("Testing all conditional branches and tier-finding logic\n")
    
    tiers = [0, 50, 1000, 8000]
    costs = [0.62, 0.58, 0.55, 0.52]
    
    # PATH 1: Test negative amount branch (amount < 0)
    print("PATH 1: Testing negative amount condition (amount < 0)")
    result = calculate_cost(-100, tiers, costs)
    run_wb_test(results, "WB_CC_PATH1: Negative amount",
                "if amount < 0: return 0.0",
                result, 0.0)
    
    # PATH 2: Test zero amount branch (amount == 0)
    print("\nPATH 2: Testing zero amount condition (amount == 0)")
    result = calculate_cost(0, tiers, costs)
    run_wb_test(results, "WB_CC_PATH2: Zero amount",
                "if amount == 0: return 0.0",
                result, 0.0)
    
    # PATH 3a: Test first tier (0 <= amount < 50)
    print("\nPATH 3a: Testing first tier logic (0 <= amount < 50)")
    result = calculate_cost(25, tiers, costs)
    expected = 25 * 0.62  # First tier cost
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3a: Amount in first tier",
                "tier_index = 0, cost = amount * costs[0]",
                passed, True)
    
    # PATH 3b: Test exact tier boundary (amount == tier[i])
    print("\nPATH 3b: Testing exact tier boundary (amount == 50)")
    result = calculate_cost(50, tiers, costs)
    expected = 50 * 0.58  # Second tier cost
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3b: Amount at tier boundary",
                "amount >= tiers[i], tier_index = 1",
                passed, True)
    
    # PATH 3c: Test middle tier (50 < amount < 1000)
    print("\nPATH 3c: Testing middle tier (50 < amount < 1000)")
    result = calculate_cost(500, tiers, costs)
    expected = 500 * 0.58  # Second tier cost
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3c: Amount in middle tier",
                "tier_index = 1, cost = amount * costs[1]",
                passed, True)
    
    # PATH 3d: Test highest tier (amount >= 8000)
    print("\nPATH 3d: Testing highest (open-ended) tier (amount >= 8000)")
    result = calculate_cost(10000, tiers, costs)
    expected = 10000 * 0.52  # Highest tier cost
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3d: Amount in highest tier",
                "tier_index = 3, cost = amount * costs[3]",
                passed, True)
    
    # Test boundary just before tier change (49.99)
    print("\nPATH 3e: Testing boundary edge case (49.99)")
    result = calculate_cost(49.99, tiers, costs)
    expected = 49.99 * 0.62  # Should still be first tier
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3e: Just before tier boundary",
                "amount < 50, tier_index = 0",
                passed, True)
    
    # Test boundary just after tier change (50.01)
    print("\nPATH 3f: Testing boundary edge case (50.01)")
    result = calculate_cost(50.01, tiers, costs)
    expected = 50.01 * 0.58  # Should be second tier
    passed = abs(result - expected) < 0.01
    run_wb_test(results, "WB_CC_PATH3f: Just after tier boundary",
                "amount >= 50, tier_index = 1",
                passed, True)


def test_find_tier_index_loop_coverage(results):
    """White-box tests for find_tier_index() covering loop execution paths."""
    print("\n--- WHITE-BOX TESTING: cost_calculator.find_tier_index() ---")
    print("Testing loop iterations and boundary conditions\n")
    
    tiers = [0, 50, 1000, 8000]
    
    # LOOP PATH 1: Loop executes 1 iteration (amount >= last tier)
    print("LOOP PATH 1: Single iteration (amount >= highest tier)")
    result = find_tier_index(10000, tiers)
    run_wb_test(results, "WB_FTI_LOOP1: Immediate match on first iteration",
                "for i in [3]: if 10000 >= 8000: return 3",
                result, 3)
    
    # LOOP PATH 2: Loop executes 2 iterations
    print("\nLOOP PATH 2: Two iterations (amount in second-to-last tier)")
    result = find_tier_index(5000, tiers)
    run_wb_test(results, "WB_FTI_LOOP2: Match on second iteration",
                "for i in [3,2]: if 5000 >= 1000: return 2",
                result, 2)
    
    # LOOP PATH 3: Loop executes 3 iterations
    print("\nLOOP PATH 3: Three iterations (amount in second tier)")
    result = find_tier_index(100, tiers)
    run_wb_test(results, "WB_FTI_LOOP3: Match on third iteration",
                "for i in [3,2,1]: if 100 >= 50: return 1",
                result, 1)
    
    # LOOP PATH 4: Loop executes all iterations (amount in first tier)
    print("\nLOOP PATH 4: All iterations (amount in first tier)")
    result = find_tier_index(25, tiers)
    run_wb_test(results, "WB_FTI_LOOP4: Match on fourth iteration",
                "for i in [3,2,1,0]: if 25 >= 0: return 0",
                result, 0)
    
    # EDGE CASE: Test with single tier
    print("\nEDGE CASE: Single tier (loop executes once)")
    result = find_tier_index(100, [0])
    run_wb_test(results, "WB_FTI_EDGE1: Single tier",
                "for i in [0]: if 100 >= 0: return 0",
                result, 0)


# ============================================================================
# WHITE-BOX TEST SECTION 2: parse_service_entry() - Complex Parsing Logic
# ============================================================================
#
# Function: parse_service_entry(lines, index)
#
# Code paths to test:
# PATH 1: Happy path - all parsing succeeds
# PATH 2: Invalid name line (wrong format) → return None
# PATH 3: Invalid tier line (non-numeric) → ValueError → return None
# PATH 4: Invalid cost line (non-numeric) → ValueError → return None
# PATH 5: Mismatched tiers/costs count → return None
# PATH 6: Tiers not in ascending order → return None
# PATH 7: Index out of range → IndexError → return None
#
# Conditional branches:
# - if len(name_line) != 2
# - if len(tiers) != len(costs)
# - if tiers[i] >= tiers[i+1] (loop through tiers)
# - try-except blocks for ValueError and IndexError
# ============================================================================

def test_parse_service_entry_whitebox(results):
    """White-box tests for parse_service_entry() covering all code paths."""
    print("\n--- WHITE-BOX TESTING: service_loader.parse_service_entry() ---")
    print("Testing all parsing branches and error handling\n")
    
    # PATH 1: Happy path - valid parsing
    print("PATH 1: Valid service entry (happy path)")
    valid_lines = [
        "Compute,hour",
        "0,50,1000",
        "0.62,0.58,0.55"
    ]
    result = parse_service_entry(valid_lines, 0)
    passed = (result is not None and 
              result['name'] == 'Compute' and
              result['units'] == 'hour')
    run_wb_test(results, "WB_PSE_PATH1: Valid parsing",
                "All conditions pass, return service_data",
                passed, True)
    
    # PATH 2: Invalid name line format
    print("\nPATH 2: Invalid name line (wrong format)")
    invalid_lines = [
        "Compute",  # Missing units
        "0,50",
        "0.62,0.58"
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_wb_test(results, "WB_PSE_PATH2: Invalid name format",
                "if len(name_line) != 2: return None",
                result is None, True)
    
    # PATH 3: Non-numeric tier values
    print("\nPATH 3: Non-numeric tier values (ValueError)")
    invalid_lines = [
        "Storage,Gb",
        "0,abc,1000",  # 'abc' is not a number
        "0.12,0.10,0.09"
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_wb_test(results, "WB_PSE_PATH3: Non-numeric tiers",
                "float(t.strip()) raises ValueError → except → return None",
                result is None, True)
    
    # PATH 4: Non-numeric cost values
    print("\nPATH 4: Non-numeric cost values (ValueError)")
    invalid_lines = [
        "Storage,Gb",
        "0,100,500",
        "0.12,xyz,0.09"  # 'xyz' is not a number
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_wb_test(results, "WB_PSE_PATH4: Non-numeric costs",
                "float(c.strip()) raises ValueError → except → return None",
                result is None, True)
    
    # PATH 5: Mismatched tiers and costs count
    print("\nPATH 5: Mismatched tiers/costs count")
    invalid_lines = [
        "Database,Gb",
        "0,50,200",  # 3 tiers
        "0.25,0.22"  # 2 costs (mismatch!)
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_wb_test(results, "WB_PSE_PATH5: Mismatched counts",
                "if len(tiers) != len(costs): return None",
                result is None, True)
    
    # PATH 6: Tiers not in ascending order
    print("\nPATH 6: Tiers not in ascending order")
    invalid_lines = [
        "AI,hour",
        "0,500,100",  # Not ascending! 500 > 100
        "1.50,1.35,1.20"
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_wb_test(results, "WB_PSE_PATH6: Non-ascending tiers",
                "if tiers[i] >= tiers[i+1]: return None",
                result is None, True)
    
    # PATH 7: Index out of range
    print("\nPATH 7: Index out of range (IndexError)")
    short_lines = [
        "Compute,hour"
        # Missing lines 2 and 3
    ]
    result = parse_service_entry(short_lines, 0)
    run_wb_test(results, "WB_PSE_PATH7: Index out of range",
                "lines[index+1] raises IndexError → except → return None",
                result is None, True)
    
    # LOOP COVERAGE: Test tier validation loop with multiple tiers
    print("\nLOOP COVERAGE: Tier validation loop")
    valid_lines_4tiers = [
        "Networking,Gb",
        "0,100,500,2000",  # 4 tiers to iterate through
        "0.15,0.12,0.10,0.08"
    ]
    result = parse_service_entry(valid_lines_4tiers, 0)
    passed = result is not None and len(result['tiers']) == 4
    run_wb_test(results, "WB_PSE_LOOP: Validation loop 4 iterations",
                "for i in range(3): check tiers[i] < tiers[i+1]",
                passed, True)
    
    # EDGE CASE: Single tier (loop doesn't execute)
    print("\nEDGE CASE: Single tier (loop body skipped)")
    single_tier = [
        "Simple,unit",
        "0",
        "1.00"
    ]
    result = parse_service_entry(single_tier, 0)
    passed = result is not None and len(result['tiers']) == 1
    run_wb_test(results, "WB_PSE_EDGE: Single tier, no loop",
                "range(len(tiers)-1) = range(0), loop skipped",
                passed, True)
    
    # EDGE CASE: Tiers equal (boundary condition)
    print("\nEDGE CASE: Equal consecutive tiers")
    equal_tiers = [
        "Bad,Gb",
        "0,50,50",  # Second and third are equal
        "0.10,0.09,0.08"
    ]
    result = parse_service_entry(equal_tiers, 0)
    run_wb_test(results, "WB_PSE_EDGE2: Equal tiers rejected",
                "if tiers[1] >= tiers[2]: return None",
                result is None, True)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all white-box tests."""
    results = WhiteBoxTestResults()
    
    print("="*70)
    print("RUNNING WHITE-BOX TESTS")
    print("="*70)
    print("\nFOCUS: Testing internal logic paths and code coverage")
    print("Selected functions:")
    print("1. calculate_cost() - Complex conditional and tier logic")
    print("2. parse_service_entry() - Complex parsing with error handling")
    print("="*70)
    
    # Run all white-box test suites
    test_calculate_cost_whitebox(results)
    test_find_tier_index_loop_coverage(results)
    test_parse_service_entry_whitebox(results)
    
    # Print summary
    results.print_summary()
    
    # Return exit code based on results
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
