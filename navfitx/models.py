import pandas as pd
import pyodbc
from sqlmodel import Field, Session, SQLModel, create_engine


# --- 1. Define your SQLModel table ---
class Customer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str | None = None


# --- 2. Connect to your Access database ---
access_db_path = r"./export_folder.accdb"
conn_str = (
    r"Driver={MDBTools};"
    rf"DBQ={access_db_path};"
)
access_conn = pyodbc.connect(conn_str)

# --- 3. Read table data into a pandas DataFrame ---
table_name = "Folders"
df = pd.read_sql(f"SELECT * FROM {table_name}", access_conn)

# --- 4. Create your SQLModel database ---
engine = create_engine("sqlite:///customers.db")
SQLModel.metadata.create_all(engine)

# --- 5. Insert data into SQLModel ---
with Session(engine) as session:
    for _, row in df.iterrows():
        customer = Customer(id=row["ID"], name=row["Name"], email=row.get("Email"))
        session.add(customer)
    session.commit()
