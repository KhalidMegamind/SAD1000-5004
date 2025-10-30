"""
Subscription Manager Module
Manages user subscriptions to services.

Functions:
- create_subscriptions(): Initialize empty subscriptions dictionary
- add_subscription(subscriptions, service_name, amount): Add/update subscription
- get_subscription_amount(subscriptions, service_name): Get current amount
- get_all_subscriptions(subscriptions): Get all active subscriptions
- has_subscriptions(subscriptions): Check if any subscriptions exist
"""


def create_subscriptions():
    """
    Create an empty subscriptions dictionary.
    
    Returns:
        dict: Empty subscriptions dictionary
    """
    return {}


def add_subscription(subscriptions, service_name, amount):
    """
    Add or update a subscription for a service.
    
    Parameters:
        subscriptions (dict): Current subscriptions
        service_name (str): Name of the service
        amount (float): Amount of service to subscribe to
    
    Returns:
        bool: True if successful, False otherwise
    """
    if amount < 0:
        return False
    
    # If amount is 0, we still allow it but it means no subscription
    subscriptions[service_name] = amount
    return True


def get_subscription_amount(subscriptions, service_name):
    """
    Get the current subscription amount for a service.
    
    Parameters:
        subscriptions (dict): Current subscriptions
        service_name (str): Name of the service
    
    Returns:
        float: Current amount (0 if not subscribed)
    """
    return subscriptions.get(service_name, 0.0)


def get_all_subscriptions(subscriptions):
    """
    Get all active subscriptions (amount > 0).
    
    Parameters:
        subscriptions (dict): Current subscriptions
    
    Returns:
        dict: Dictionary of active subscriptions only
    """
    return {name: amount for name, amount in subscriptions.items() if amount > 0}


def has_subscriptions(subscriptions):
    """
    Check if there are any active subscriptions.
    
    Parameters:
        subscriptions (dict): Current subscriptions
    
    Returns:
        bool: True if there are active subscriptions, False otherwise
    """
    return any(amount > 0 for amount in subscriptions.values())


def remove_subscription(subscriptions, service_name):
    """
    Remove a subscription (set amount to 0).
    
    Parameters:
        subscriptions (dict): Current subscriptions
        service_name (str): Name of the service
    
    Returns:
        bool: True if service existed, False otherwise
    """
    if service_name in subscriptions:
        subscriptions[service_name] = 0.0
        return True
    return False


def clear_all_subscriptions(subscriptions):
    """
    Clear all subscriptions.
    
    Parameters:
        subscriptions (dict): Current subscriptions
    """
    subscriptions.clear()
