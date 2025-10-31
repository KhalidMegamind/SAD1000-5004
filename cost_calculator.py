"""
Cost Calculator Module
Handles calculation of costs based on tiered pricing structure.

Functions:
- calculate_cost(amount, tiers, costs): Calculate cost for given amount
- find_tier_index(amount, tiers): Find which tier an amount falls into
- format_currency(amount): Format amount as currency string
"""


def calculate_cost(amount, tiers, costs):
    """
    Calculate the total cost for a given amount based on tiered pricing.
    
    The tiered pricing works where higher amounts get lower per-unit rates.
    For example, with tiers [0, 50, 1000] and costs [0.62, 0.58, 0.55]:
    - 0-49.99 units: $0.62 per unit
    - 50-999.99 units: $0.58 per unit
    - 1000+ units: $0.55 per unit
    
    Parameters:
        amount (float): Amount of service to calculate cost for
        tiers (list): List of tier boundaries
        costs (list): List of costs per tier
    
    Returns:
        float: Total cost for the amount
    """
    if amount < 0:
        return 0.0
    
    if amount == 0:
        return 0.0
    
    # Find which tier this amount falls into
    tier_index = find_tier_index(amount, tiers)
    
    # All units are charged at the rate for that tier
    total_cost = amount * costs[tier_index]
    
    return total_cost


def find_tier_index(amount, tiers):
    """
    Find which tier index an amount falls into.
    
    Tier boundaries define the start of each tier:
    - Tier 0: [tiers[0], tiers[1])
    - Tier 1: [tiers[1], tiers[2])
    - ...
    - Last tier: [tiers[-1], infinity)
    
    Parameters:
        amount (float): Amount to find tier for
        tiers (list): List of tier boundaries
    
    Returns:
        int: Index of the tier (0 to len(tiers)-1)
    """
    # Start from the highest tier and work backwards
    for i in range(len(tiers) - 1, -1, -1):
        if amount >= tiers[i]:
            return i
    
    # Should never reach here if amount >= 0, but default to first tier
    return 0


def get_cost_per_unit(amount, tiers, costs):
    """
    Get the per-unit cost rate for a given amount.
    
    Parameters:
        amount (float): Amount to check
        tiers (list): List of tier boundaries
        costs (list): List of costs per tier
    
    Returns:
        float: Cost per unit for this amount
    """
    if amount < 0:
        return 0.0
    
    tier_index = find_tier_index(amount, tiers)
    return costs[tier_index]


def format_currency(amount):
    """
    Format a numeric amount as currency string.
    
    Parameters:
        amount (float): Amount to format
    
    Returns:
        str: Formatted currency string (e.g., "$58.00")
    """
    return f"${amount:.2f}"


def calculate_total_cost(subscriptions, services):
    """
    Calculate total cost across all subscriptions.
    
    Parameters:
        subscriptions (dict): Dictionary of service_name: amount pairs
        services (dict): Dictionary of service data
    
    Returns:
        float: Total cost across all subscriptions
    """
    total = 0.0
    
    for service_name, amount in subscriptions.items():
        if service_name in services and amount > 0:
            service = services[service_name]
            cost = calculate_cost(amount, service['tiers'], service['costs'])
            total += cost
    
    return total
