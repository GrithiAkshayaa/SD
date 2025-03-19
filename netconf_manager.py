from ncclient import manager

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
