# SAD1000-5004


# ISE Cloud Services Calculator (ICSC)

## Project Overview
This is a Python implementation of the ISE Cloud Services Calculator for the ISAD1000/5004 Assignment. The system calculates cloud service subscription costs using tiered pricing structures.

## Author
Student Name: KHALID MOHAMMAD GALIB
Student Number: 23391745

## Project Structure
```
ICSC_Project/
├── icsc.py                 # Main program
├── service_loader.py       # CSV parsing and service data loading
├── cost_calculator.py      # Tiered cost calculations
├── subscription_manager.py # Subscription management
├── ui_handler.py          # User interface functions
├── services.csv           # Service definitions with tiered pricing
├── test_blackbox.py       # Black-box test suite
├── test_whitebox.py       # White-box test suite
└── README.txt             # This file
```

## Requirements
- Python 3.6 or higher
- Linux environment (tested on Ubuntu)
- No external dependencies required

## How to Run the Program

### Main Application
```bash
python3 icsc.py
```

The program will:
1. Load services from services.csv
2. Display a menu with available services
3. Allow you to add/modify subscriptions
4. Calculate and display costs

### Menu Options
- **1-6**: Select a service to add/modify subscription
- **s**: List all current subscriptions
- **$**: Display detailed cost breakdown
- **q**: Quit the program

### Example Usage
```
> 1                          # Select Compute service
Enter new hour amount: 100   # Add 100 hours
> s                          # List subscriptions
> $                          # Show cost breakdown
> q                          # Quit
```

## How to Run Tests

### Black-Box Tests
Tests all functions based on their specifications:
```bash
python3 test_blackbox.py
```

### White-Box Tests
Tests internal logic paths and code coverage:
```bash
python3 test_whitebox.py
```

### Both Test Suites
```bash
python3 test_blackbox.py && python3 test_whitebox.py
```

## Modular Design

### Module: service_loader.py
**Purpose**: Load and parse service data from CSV files
**Functions**:
- `load_services(filename)`: Load all services from CSV
- `parse_service_entry(lines, index)`: Parse individual service
- `validate_service_data(service)`: Validate service structure
- `get_service_names(services)`: Get list of service names

### Module: cost_calculator.py
**Purpose**: Calculate costs based on tiered pricing
**Functions**:
- `calculate_cost(amount, tiers, costs)`: Calculate total cost
- `find_tier_index(amount, tiers)`: Find appropriate tier
- `get_cost_per_unit(amount, tiers, costs)`: Get per-unit cost
- `format_currency(amount)`: Format as currency string
- `calculate_total_cost(subscriptions, services)`: Calculate total

### Module: subscription_manager.py
**Purpose**: Manage user subscriptions
**Functions**:
- `create_subscriptions()`: Initialize empty subscriptions
- `add_subscription(subscriptions, name, amount)`: Add/update subscription
- `get_subscription_amount(subscriptions, name)`: Get amount
- `get_all_subscriptions(subscriptions)`: Get active subscriptions
- `has_subscriptions(subscriptions)`: Check if any exist

### Module: ui_handler.py
**Purpose**: Handle user interface and interaction
**Functions**:
- `display_main_menu(services)`: Show main menu
- `display_service_costs(name, service)`: Show cost structure
- `display_subscriptions(subscriptions, services)`: List subscriptions
- `display_cost_breakdown(subscriptions, services)`: Show breakdown
- `get_user_choice()`: Get menu input
- `get_amount_input(prompt, current, units)`: Get numeric input

### Main Program: icsc.py
**Purpose**: Main program loop and coordination
**Functions**:
- `process_service_selection(choice, services, subscriptions)`: Handle selection
- `main()`: Main program entry point

## Services File Format (services.csv)

Each service requires 3 lines:
1. Service name and units (comma-separated)
2. Tier boundaries (comma-separated)
3. Costs per tier (comma-separated)

Example:
```
Compute,hour
0,50,1000,8000
0.62,0.58,0.55,0.52
```

This defines:
- Service: Compute (measured in hours)
- Tier 0: 0-49.99 hours @ $0.62/hour
- Tier 1: 50-999.99 hours @ $0.58/hour
- Tier 2: 1000-7999.99 hours @ $0.55/hour
- Tier 3: 8000+ hours @ $0.52/hour

## Testing Strategy

### Black-Box Testing
Tests each function's external behavior:
- Input validation (boundary values, error cases)
- Output correctness
- File I/O operations
- Data structure management

Coverage: 32 tests covering all modules

### White-Box Testing
Tests internal logic paths for complex functions:

**Function 1: calculate_cost()**
- All conditional branches
- Tier boundary conditions
- Edge cases (negative, zero, large values)

**Function 2: parse_service_entry()**
- All parsing paths
- Error handling (ValueError, IndexError)
- Loop coverage (tier validation)
- Edge cases (single tier, equal tiers)

Coverage: 23 tests covering all code paths



```

## Known Issues
None at this time.

## Future Improvements
- Add ability to remove subscriptions
- Support for saving/loading subscription profiles
- More detailed cost history
- Support for promotional discounts
- Unit test framework integration (pytest/unittest)


