import pyodbc
import typer

# Define the connection string
conn_str = r'DRIVER={MDBTools};DBQ=/home/user/Downloads/mydb.accdb;'

# Establish the connection
conn = pyodbc.connect(conn_str)

# Create a cursor
cursor = conn.cursor()

# Execute a query
# cursor.execute('SELECT * FROM your_table_name')
table_names = cursor.tables()
print(table_names)

for table in table_names:
    print(table)

cursor.execute("SELECT * FROM MSysNavPaneGroups")

rows = cursor.fetchall()
for row in rows:
    print(row)

# Fetch all results
# rows = cursor.fetchall()

# Iterate over the rows
# for row in rows:
#     print(row)

# Close the connection
conn.close()
