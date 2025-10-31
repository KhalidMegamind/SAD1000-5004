"""
UI Handler Module
Handles user interface, menu display, and user input.

Functions:
- display_main_menu(services): Display the main menu
- display_service_costs(service_name, service): Display cost structure for a service
- display_subscriptions(subscriptions, services): Display all active subscriptions
- display_cost_breakdown(subscriptions, services): Display detailed cost breakdown
- get_user_choice(): Get menu choice from user
- get_amount_input(prompt): Get numeric amount from user
"""

from cost_calculator import calculate_cost, get_cost_per_unit, format_currency


def display_main_menu(services):
    """
    Display the main menu with all available services.
    
    Parameters:
        services (dict): Dictionary of available services
    """
    print("\n" + "="*50)
    print("Welcome to ICSC – ISE Cloud Services Calculator")
    print("="*50)
    print("\nAdd subscription for:")
    
    service_names = sorted(services.keys())
    for i, service_name in enumerate(service_names, 1):
        print(f"{i}) {service_name}")
    
    print("s) List subscriptions and totals")
    print("$) Display cost breakdown")
    print("q) Quit")


def display_service_costs(service_name, service):
    """
    Display the cost structure for a specific service.
    
    Parameters:
        service_name (str): Name of the service
        service (dict): Service data including tiers and costs
    """
    print(f"\nYou chose {service_name}, which has the following cost structure:")
    
    tiers = service['tiers']
    costs = service['costs']
    units = service['units']
    
    for i in range(len(tiers)):
        if i < len(tiers) - 1:
            # Not the last tier
            print(f"{tiers[i]}-{tiers[i+1]}: {format_currency(costs[i])} per {units}")
        else:
            # Last tier (open-ended)
            print(f"{tiers[i]}+: {format_currency(costs[i])} per {units}")


def display_subscriptions(subscriptions, services):
    """
    Display all active subscriptions.
    
    Parameters:
        subscriptions (dict): Current subscriptions
        services (dict): Dictionary of service data
    """
    active_subs = {name: amount for name, amount in subscriptions.items() if amount > 0}
    
    if not active_subs:
        print("\nYou have no subscriptions yet.")
        return
    
    print("\nYou have subscriptions for:")
    for service_name, amount in sorted(active_subs.items()):
        if service_name in services:
            units = services[service_name]['units']
            # Handle singular/plural
            unit_text = units if amount != 1 else units.rstrip('s')
            print(f"{service_name}: {amount} {unit_text}(s)")


def display_cost_breakdown(subscriptions, services):
    """
    Display detailed cost breakdown for all subscriptions.
    
    Parameters:
        subscriptions (dict): Current subscriptions
        services (dict): Dictionary of service data
    """
    active_subs = {name: amount for name, amount in subscriptions.items() if amount > 0}
    
    if not active_subs:
        print("\nYou have no subscriptions yet.")
        return
    
    print("\nYour current cost breakdown is:")
    total = 0.0
    
    for service_name, amount in sorted(active_subs.items()):
        if service_name in services:
            service = services[service_name]
            cost = calculate_cost(amount, service['tiers'], service['costs'])
            per_unit_cost = get_cost_per_unit(amount, service['tiers'], service['costs'])
            
            print(f"{service_name}: {amount} @ {format_currency(per_unit_cost)} = {format_currency(cost)}")
            total += cost
    
    print(f"TOTAL: {format_currency(total)}")


def get_user_choice():
    """
    Get menu choice from user.
    
    Returns:
        str: User's choice (lowercase, stripped)
    """
    try:
        choice = input("\n> ").strip().lower()
        return choice
    except EOFError:
        return 'q'
    except KeyboardInterrupt:
        return 'q'


def get_amount_input(prompt, current_amount=0.0, units="unit"):
    """
    Get numeric amount input from user.
    
    Parameters:
        prompt (str): Prompt to display to user
        current_amount (float): Current amount (for display)
        units (str): Unit name for display
    
    Returns:
        float or None: Amount entered by user, or None if invalid/cancelled
    """
    print(f"\nCurrent {units} amount: {current_amount}")
    print(prompt)
    
    try:
        user_input = input("> ").strip()
        
        if user_input == "":
            return None
        
        amount = float(user_input)
        
        if amount < 0:
            print("Error: Amount cannot be negative.")
            return None
        
        return amount
    
    except ValueError:
        print("Error: Please enter a valid number.")
        return None
    except EOFError:
        return None
    except KeyboardInterrupt:
        return None


def display_error(message):
    """
    Display an error message to the user.
    
    Parameters:
        message (str): Error message to display
    """
    print(f"\nError: {message}")


def display_success(message):
    """
    Display a success message to the user.
    
    Parameters:
        message (str): Success message to display
    """
    print(f"\n{message}")


def confirm_quit():
    """
    Ask user to confirm they want to quit.
    
    Returns:
        bool: True if user confirms, False otherwise
    """
    print("\nThank you for using ICSC!")
    return True
