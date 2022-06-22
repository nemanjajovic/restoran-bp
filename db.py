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
        cond = f"WHERE {condition}" if condition else ""
        command = f"""SELECT {columns} FROM {table} {cond};"""
        return self.cursor.execute(command)

    def insert(self, table, columns, values):
        command = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self.cursor.execute(command)

    def update(self, table, column, new_val, id_column, id_val):
        command = f"UPDATE {table} SET {column} = '{new_val}' WHERE {id_column} = {id_val}"
        return self.cursor.execute(command)

# context manager
class Connection:
    def __init__(self):
        pass

    def __enter__(self):
        self.handler = DbHandler()
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handler:
            self.handler.conn.commit()
            self.handler.conn.close()

# context manager test
with Connection() as handler:
    table = "Radnici"
    #handler.insert("Radnici", "radnik_naziv, radnik_tip", "'DUDU DADA', 'servis'")
    handler.update(table, "radnik_naziv", 'Hahuu g', "radnik_id", "7")
    for row in handler.select("*", table,""):
        print(row)