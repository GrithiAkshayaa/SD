from ncclient import manager
import xml.etree.ElementTree as ET

# Function to connect to the NETCONF server
def open_netconf_connection(host, port, username, password):
    try:
        connection = manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False
        )
        print("✅ Connection Established")
        return connection
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return None

# Function to close the NETCONF connection
def close_netconf_connection(session):
    session.close_session()
    print("✅ NETCONF Connection Closed")

# Function to parse XML and extract configurations
def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

# Function to generate NETCONF XML for creating configurations
def generate_create_rpc(component):
    name = component.find("name").text
    config = component.find("config")

    rpc = f"""
    <config>
        <components xmlns="http://openconfig.net/yang/platform">
            <component>
                <name>{name}</name>
                <config>
                    <description>{config.find("description").text}</description>
                    <type>{config.find("type").text}</type>
                </config>
            </component>
        </components>
    </config>
    """
    return rpc

# Function to generate NETCONF XML for deleting configurations
def generate_delete_rpc(name):
    rpc = f"""
    <config>
        <components xmlns="http://openconfig.net/yang/platform">
            <component operation="delete">
                <name>{name}</name>
            </component>
        </components>
    </config>
    """
    return rpc

# Function to apply configurations (Create/Delete/Update)
def apply_configuration(xml_file, operation):
    components = parse_xml(xml_file)

    # Open connection to NETCONF
    netconf_session = open_netconf_connection("127.0.0.1", 830, "admin", "admin")
    
    if not netconf_session:
        return  # Exit if connection fails

    for component in components.findall("component"):
        name = component.find("name").text
        
        if operation == "create":
            rpc = generate_create_rpc(component)
        elif operation == "delete":
            rpc = generate_delete_rpc(name)
        else:
            print(f"Invalid operation: {operation}")
            return
        
        response = netconf_session.edit_config(target="running", config=rpc)
        print(response)

    # Close connection after operation
    close_netconf_connection(netconf_session)

# Run the script
if __name__ == "__main__":
    apply_configuration("config.xml", "create")  # Change to "delete" for deletion
