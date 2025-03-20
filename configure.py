import json
import subprocess
import sys

CONFIG_FILE = "config.json"

def load_config(file_path):
    """Load configuration from JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        sys.exit(1)

def apply_config(data):
    """Apply configuration using confd_cli."""
    try:
        for component in data.get("components", []):
            name = component.get("name")
            config = component.get("config", {})
            state = component.get("state", {})

            print(f"\nConfiguring component: {name}")

            # Configure the component
            subprocess.run(f'confd_cli -C "config; set openconfig-platform:components/component {name}"',
                           shell=True, check=True)

            # Apply config settings
            for key, value in config.items():
                cmd = f'confd_cli -C "config; set openconfig-platform:components/component {name}/config/{key} {value}"'
                subprocess.run(cmd, shell=True, check=True)

            # Apply state settings
            for key, value in state.items():
                cmd = f'confd_cli -C "config; set openconfig-platform:components/component {name}/state/{key} {value}"'
                subprocess.run(cmd, shell=True, check=True)

        # Commit changes
        subprocess.run('confd_cli -C "commit"', shell=True, check=True)
        print("\nConfiguration applied successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error applying configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    config_data = load_config(CONFIG_FILE)
    apply_config(config_data)
