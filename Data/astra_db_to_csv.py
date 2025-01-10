import pandas as pd
from cassandra.cluster import Cluster

# Path to the secure connect bundle (downloaded from Astra DB dashboard)
SECURE_CONNECT_BUNDLE = 'path_to_secure_connect_bundle.zip'

# Keyspace and table name
ASTRA_DB_KEYSPACE = 'your_keyspace'  # Replace with your keyspace name
ASTRA_DB_TABLE = 'your_table_name'  # Replace with your table name

def connect_to_astra_db(bundle_path):
    """Connect to Astra DB using the secure connect bundle and return a session object."""
    cluster = Cluster(cloud={'secure_connect_bundle': bundle_path})
    session = cluster.connect()
    return session

def fetch_data_from_astra_db(session, keyspace, table_name):
    """Fetch data from Astra DB and return it as a Pandas DataFrame."""
    session.set_keyspace(keyspace)
    query = f"SELECT * FROM {table_name}"
    rows = session.execute(query)

    # Convert rows to a list of dictionaries
    data = [dict(row._asdict()) for row in rows]

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    # Connect to Astra DB
    session = connect_to_astra_db(SECURE_CONNECT_BUNDLE)
    print("Connected to Astra DB successfully!")

    # Fetch data and load it into a Pandas DataFrame
    df = fetch_data_from_astra_db(session, ASTRA_DB_KEYSPACE, ASTRA_DB_TABLE)

    # Display the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv("astra_db_data.csv", index=False)
    print("Data saved to astra_db_data.csv!")

if _name_ == "_main_":
    main()