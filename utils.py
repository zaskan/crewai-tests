import yaml

def parse_yaml(file_path):
    """Reads and parses YAML files."""
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except yaml.YAMLError:
        return "Error: Invalid YAML format."