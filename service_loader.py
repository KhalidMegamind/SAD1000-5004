"""
Service Loader Module
Handles loading and parsing service data from CSV file.

Functions:
- load_services(filename): Load all services from CSV file
- parse_service_entry(lines, index): Parse a single service entry
- validate_service_data(service): Validate service data structure
"""


def load_services(filename):
    """
    Load services from CSV file and return as dictionary.
    
    Parameters:
        filename (str): Path to the services CSV file
    
    Returns:
        dict: Dictionary of services with structure:
              {service_name: {'units': str, 'tiers': list, 'costs': list}}
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If file format is invalid
    """
    services = {}
    
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Services file '{filename}' not found")
    
    i = 0
    while i < len(lines):
        if i + 2 >= len(lines):
            break
            
        # Parse service entry (3 lines: name/units, tiers, costs)
        service_data = parse_service_entry(lines, i)
        
        if service_data:
            services[service_data['name']] = {
                'units': service_data['units'],
                'tiers': service_data['tiers'],
                'costs': service_data['costs']
            }
        
        i += 3
    
    if not services:
        raise ValueError("No valid services found in file")
    
    return services


def parse_service_entry(lines, index):
    """
    Parse a single service entry from three consecutive lines.
    
    Parameters:
        lines (list): All lines from the CSV file
        index (int): Starting index of the service entry
    
    Returns:
        dict: Parsed service data or None if invalid
    """
    try:
        # Line 1: Service name and units
        name_line = lines[index].split(',')
        if len(name_line) != 2:
            return None
        
        service_name = name_line[0].strip()
        units = name_line[1].strip()
        
        # Line 2: Tier boundaries
        tier_line = lines[index + 1].split(',')
        tiers = [float(t.strip()) for t in tier_line]
        
        # Line 3: Costs per tier
        cost_line = lines[index + 2].split(',')
        costs = [float(c.strip()) for c in cost_line]
        
        # Validate that tiers and costs match
        if len(tiers) != len(costs):
            return None
        
        # Validate tiers are in ascending order
        for i in range(len(tiers) - 1):
            if tiers[i] >= tiers[i + 1]:
                return None
        
        return {
            'name': service_name,
            'units': units,
            'tiers': tiers,
            'costs': costs
        }
    
    except (ValueError, IndexError):
        return None


def validate_service_data(service):
    """
    Validate that service data structure is correct.
    
    Parameters:
        service (dict): Service data to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(service, dict):
        return False
    
    required_keys = ['units', 'tiers', 'costs']
    if not all(key in service for key in required_keys):
        return False
    
    if len(service['tiers']) != len(service['costs']):
        return False
    
    if len(service['tiers']) == 0:
        return False
    
    # Check all tiers are non-negative
    if any(tier < 0 for tier in service['tiers']):
        return False
    
    # Check all costs are positive
    if any(cost <= 0 for cost in service['costs']):
        return False
    
    return True


def get_service_names(services):
    """
    Get list of all service names.
    
    Parameters:
        services (dict): Dictionary of services
    
    Returns:
        list: Sorted list of service names
    """
    return sorted(services.keys())
