import pyodbc

class DbHandler:
    def __init__(self):
        self.conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-1P60H2U;"
            "Database=Test;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def select(self, columns, table, condition):
        extend = f"WHERE {condition}" if condition else ""
        rows = self.cursor.execute(f"""SELECT {columns} FROM {table} {extend};""")
        for row in rows:
            print("ID=%d, Name=%s Position=%s" % (row[0], row[1], row[2]))

# context manager
class Connection:
    def __init__(self):
        pass

    def __enter__(self):
        self.handler = DbHandler()
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handler:
            self.handler.conn.close()

# context manager test
with Connection() as handler:
    handler.select("*", "Radnici","")