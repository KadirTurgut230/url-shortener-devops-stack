from user_agents import parse
import random

def parse_device_type(user_agent_string: str) -> str:
    if not user_agent_string or user_agent_string == "Unknown":
        return "Unknown"
        
    ua = parse(user_agent_string)
    
    if ua.is_mobile:
        return "Mobile"
    elif ua.is_tablet:
        return "Tablet"
    elif ua.is_pc:
        return "Desktop"
    else:
        return "Other"

def resolve_country_from_ip(ip_address: str) -> str:
    mock_countries = ["Turkey", "Germany", "USA", "UK", "France", "Japan"]
    try:
        last_digit = int(ip_address.split('.')[-1])
        return mock_countries[last_digit % len(mock_countries)]
    except:
        return random.choice(mock_countries)