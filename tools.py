import yaml

def read_playbook(playbook_path):
    with open(playbook_path, 'r') as f:
        return yaml.safe_load(f)
