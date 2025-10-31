#!/usr/bin/env python3
"""
Black-Box Tests for ICSC
Tests functions based on their specifications without examining internal logic.

Test Coverage:
- service_loader functions
- cost_calculator functions
- subscription_manager functions
- ui_handler formatting functions
"""

import sys
import os

# Import modules to test
from service_loader import (
    load_services, parse_service_entry, validate_service_data, get_service_names
)
from cost_calculator import (
    calculate_cost, find_tier_index, get_cost_per_unit, format_currency,
    calculate_total_cost
)
from subscription_manager import (
    create_subscriptions, add_subscription, get_subscription_amount,
    get_all_subscriptions, has_subscriptions
)


class TestResults:
    """Simple class to track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, test_name, passed, expected, actual):
        self.tests.append({
            'name': test_name,
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
        print("BLACK-BOX TEST RESULTS")
        print("="*70)
        for test in self.tests:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"{status}: {test['name']}")
            if not test['passed']:
                print(f"  Expected: {test['expected']}")
                print(f"  Got: {test['actual']}")
        print("="*70)
        print(f"Total: {self.passed + self.failed} tests")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print("="*70)


def run_test(results, test_name, actual, expected):
    """Helper function to run a single test."""
    passed = actual == expected
    results.add_result(test_name, passed, expected, actual)
    return passed


# ============================================================================
# TEST SECTION 1: service_loader.py - CSV Parsing and Validation
# ============================================================================

def test_load_services(results):
    """Test loading services from CSV file."""
    print("\n--- Testing service_loader.load_services() ---")
    
    # Test 1: Valid file loading
    try:
        services = load_services('services.csv')
        run_test(results, "BB_SL_01: Load valid services.csv",
                 'Compute' in services, True)
        run_test(results, "BB_SL_02: Services contain units field",
                 'units' in services.get('Compute', {}), True)
    except Exception as e:
        run_test(results, "BB_SL_01: Load valid services.csv", str(e), "Success")
    
    # Test 2: Invalid file (should raise FileNotFoundError)
    try:
        load_services('nonexistent.csv')
        run_test(results, "BB_SL_03: Load nonexistent file raises error",
                 False, True)
    except FileNotFoundError:
        run_test(results, "BB_SL_03: Load nonexistent file raises error",
                 True, True)


def test_parse_service_entry(results):
    """Test parsing individual service entries."""
    print("\n--- Testing service_loader.parse_service_entry() ---")
    
    # Test 1: Valid service entry
    lines = [
        "Compute,hour",
        "0,50,1000",
        "0.62,0.58,0.55"
    ]
    result = parse_service_entry(lines, 0)
    run_test(results, "BB_PSE_01: Parse valid service entry",
             result is not None, True)
    run_test(results, "BB_PSE_02: Parsed service name is 'Compute'",
             result['name'] if result else None, 'Compute')
    
    # Test 2: Invalid entry (mismatched tiers/costs)
    invalid_lines = [
        "Storage,Gb",
        "0,100",
        "0.12,0.10,0.09"  # 3 costs but only 2 tiers
    ]
    result = parse_service_entry(invalid_lines, 0)
    run_test(results, "BB_PSE_03: Parse invalid entry returns None",
             result is None, True)


def test_validate_service_data(results):
    """Test service data validation."""
    print("\n--- Testing service_loader.validate_service_data() ---")
    
    # Test 1: Valid service data
    valid_service = {
        'units': 'hour',
        'tiers': [0, 50, 1000],
        'costs': [0.62, 0.58, 0.55]
    }
    run_test(results, "BB_VSD_01: Validate correct service data",
             validate_service_data(valid_service), True)
    
    # Test 2: Invalid - negative tier
    invalid_service = {
        'units': 'hour',
        'tiers': [-10, 50],
        'costs': [0.62, 0.58]
    }
    run_test(results, "BB_VSD_02: Reject negative tier",
             validate_service_data(invalid_service), False)
    
    # Test 3: Invalid - zero or negative cost
    invalid_service2 = {
        'units': 'hour',
        'tiers': [0, 50],
        'costs': [0.62, -0.10]
    }
    run_test(results, "BB_VSD_03: Reject negative cost",
             validate_service_data(invalid_service2), False)


# ============================================================================
# TEST SECTION 2: cost_calculator.py - Tiered Pricing Calculations
# ============================================================================

def test_calculate_cost(results):
    """Test cost calculation with tiered pricing."""
    print("\n--- Testing cost_calculator.calculate_cost() ---")
    
    tiers = [0, 50, 1000, 8000]
    costs = [0.62, 0.58, 0.55, 0.52]
    
    # Test 1: Amount in first tier (0-49.99)
    cost = calculate_cost(25, tiers, costs)
    expected = 25 * 0.62  # 15.50
    run_test(results, "BB_CC_01: Calculate cost in first tier",
             abs(cost - expected) < 0.01, True)
    
    # Test 2: Amount exactly at tier boundary (50)
    cost = calculate_cost(50, tiers, costs)
    expected = 50 * 0.58  # 29.00
    run_test(results, "BB_CC_02: Calculate cost at tier boundary",
             abs(cost - expected) < 0.01, True)
    
    # Test 3: Amount in middle tier (100)
    cost = calculate_cost(100, tiers, costs)
    expected = 100 * 0.58  # 58.00
    run_test(results, "BB_CC_03: Calculate cost in middle tier",
             abs(cost - expected) < 0.01, True)
    
    # Test 4: Amount in highest tier (10000)
    cost = calculate_cost(10000, tiers, costs)
    expected = 10000 * 0.52  # 5200.00
    run_test(results, "BB_CC_04: Calculate cost in highest tier",
             abs(cost - expected) < 0.01, True)
    
    # Test 5: Zero amount
    cost = calculate_cost(0, tiers, costs)
    run_test(results, "BB_CC_05: Calculate cost for zero amount",
             cost, 0.0)
    
    # Test 6: Negative amount (boundary test)
    cost = calculate_cost(-10, tiers, costs)
    run_test(results, "BB_CC_06: Calculate cost for negative amount",
             cost, 0.0)


def test_find_tier_index(results):
    """Test finding the correct tier index."""
    print("\n--- Testing cost_calculator.find_tier_index() ---")
    
    tiers = [0, 50, 1000, 8000]
    
    # Test 1: Amount in first tier
    run_test(results, "BB_FTI_01: Find tier for amount 25",
             find_tier_index(25, tiers), 0)
    
    # Test 2: Amount exactly at tier boundary
    run_test(results, "BB_FTI_02: Find tier for amount 50",
             find_tier_index(50, tiers), 1)
    
    # Test 3: Amount in middle tier
    run_test(results, "BB_FTI_03: Find tier for amount 500",
             find_tier_index(500, tiers), 1)
    
    # Test 4: Amount in last tier
    run_test(results, "BB_FTI_04: Find tier for amount 10000",
             find_tier_index(10000, tiers), 3)


def test_format_currency(results):
    """Test currency formatting."""
    print("\n--- Testing cost_calculator.format_currency() ---")
    
    # Test 1: Whole number
    run_test(results, "BB_FC_01: Format whole number",
             format_currency(100), "$100.00")
    
    # Test 2: Decimal number
    run_test(results, "BB_FC_02: Format decimal",
             format_currency(58.99), "$58.99")
    
    # Test 3: Zero
    run_test(results, "BB_FC_03: Format zero",
             format_currency(0), "$0.00")
    
    # Test 4: Large number
    run_test(results, "BB_FC_04: Format large number",
             format_currency(5200.50), "$5200.50")


# ============================================================================
# TEST SECTION 3: subscription_manager.py - Subscription Management
# ============================================================================

def test_subscription_operations(results):
    """Test subscription management operations."""
    print("\n--- Testing subscription_manager functions ---")
    
    # Test 1: Create empty subscriptions
    subs = create_subscriptions()
    run_test(results, "BB_SM_01: Create empty subscriptions",
             isinstance(subs, dict) and len(subs) == 0, True)
    
    # Test 2: Add valid subscription
    success = add_subscription(subs, "Compute", 100)
    run_test(results, "BB_SM_02: Add valid subscription",
             success, True)
    run_test(results, "BB_SM_03: Subscription amount stored correctly",
             subs.get("Compute"), 100)
    
    # Test 3: Update existing subscription
    add_subscription(subs, "Compute", 200)
    run_test(results, "BB_SM_04: Update subscription",
             subs.get("Compute"), 200)
    
    # Test 4: Add negative amount (should fail)
    success = add_subscription(subs, "Storage", -50)
    run_test(results, "BB_SM_05: Reject negative subscription",
             success, False)
    
    # Test 5: Get subscription amount
    amount = get_subscription_amount(subs, "Compute")
    run_test(results, "BB_SM_06: Get existing subscription amount",
             amount, 200)
    
    # Test 6: Get non-existent subscription (should return 0)
    amount = get_subscription_amount(subs, "NonExistent")
    run_test(results, "BB_SM_07: Get non-existent subscription returns 0",
             amount, 0.0)
    
    # Test 7: Has subscriptions (should be True)
    add_subscription(subs, "Storage", 50)
    run_test(results, "BB_SM_08: Has subscriptions returns True",
             has_subscriptions(subs), True)
    
    # Test 8: Get all subscriptions (active only)
    active = get_all_subscriptions(subs)
    run_test(results, "BB_SM_09: Get all active subscriptions",
             len(active) >= 2, True)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all black-box tests."""
    results = TestResults()
    
    print("="*70)
    print("RUNNING BLACK-BOX TESTS")
    print("="*70)
    
    # Run all test suites
    test_load_services(results)
    test_parse_service_entry(results)
    test_validate_service_data(results)
    test_calculate_cost(results)
    test_find_tier_index(results)
    test_format_currency(results)
    test_subscription_operations(results)
    
    # Print summary
    results.print_summary()
    
    # Return exit code based on results
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
