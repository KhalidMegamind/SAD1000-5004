#!/usr/bin/env python3
"""
ISE Cloud Services Calculator (ICSC)
Main program for calculating cloud service subscription costs.

This program allows users to:
- View available cloud services with tiered pricing
- Add/modify subscriptions to services
- View current subscriptions
- Calculate and display cost breakdowns
"""

import sys
from service_loader import load_services, get_service_names
from subscription_manager import (
    create_subscriptions,
    add_subscription,
    get_subscription_amount
)
from ui_handler import (
    display_main_menu,
    display_service_costs,
    display_subscriptions,
    display_cost_breakdown,
    get_user_choice,
    get_amount_input,
    display_error,
    confirm_quit
)


def process_service_selection(choice, services, subscriptions):
    """
    Process user's selection of a service to subscribe to.
    
    Parameters:
        choice (str): User's menu choice (number)
        services (dict): Dictionary of available services
        subscriptions (dict): Current subscriptions
    
    Returns:
        bool: True if processed successfully, False otherwise
    """
    try:
        service_index = int(choice) - 1
        service_names = sorted(services.keys())
        
        if 0 <= service_index < len(service_names):
            service_name = service_names[service_index]
            service = services[service_name]
            
            # Display cost structure
            display_service_costs(service_name, service)
            
            # Get current amount
            current_amount = get_subscription_amount(subscriptions, service_name)
            
            # Get new amount from user
            units = service['units']
            amount = get_amount_input(
                f"Enter new {units} amount:",
                current_amount,
                units
            )
            
            if amount is not None:
                add_subscription(subscriptions, service_name, amount)
                print(f"\nSubscription updated: {service_name} = {amount} {units}(s)")
                return True
        else:
            display_error("Invalid service number.")
            return False
    
    except ValueError:
        return False


def main():
    """
    Main program function.
    Loads services, manages subscriptions, and handles user interaction.
    """
    # Try to load services from file
    try:
        services = load_services('services.csv')
    except FileNotFoundError:
        print("Error: services.csv file not found!")
        print("Please ensure the services.csv file exists in the current directory.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error loading services: {e}")
        sys.exit(1)
    
    # Initialize subscriptions
    subscriptions = create_subscriptions()
    
    # Main program loop
    running = True
    while running:
        display_main_menu(services)
        choice = get_user_choice()
        
        if choice == 'q':
            # Quit
            confirm_quit()
            running = False
        
        elif choice == 's':
            # List subscriptions
            display_subscriptions(subscriptions, services)
        
        elif choice == '$':
            # Display cost breakdown
            display_cost_breakdown(subscriptions, services)
        
        elif choice.isdigit():
            # User selected a service number
            process_service_selection(choice, services, subscriptions)
        
        else:
            display_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
