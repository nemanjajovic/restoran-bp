import pyodbc

class Connection:
    """Context manager for database connections."""
    def __init__(self):
        pass

    def __enter__(self):
        self.handler = DbHandler()
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handler:
            self.handler.conn.commit()
            self.handler.conn.close()

class DbHandler:
    """ Database handler class with basic database 
        interdace methods."""
    def __init__(self):
        self.conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-29O4L02;" # DESKTOP-29O4L02 lap: DESKTOP-1P60H2U
            "Database=BetaTest;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def select(self, columns, table, condition):
        cond = f"WHERE {condition}" if condition else ""
        command = f"""SELECT {columns} FROM {table} {cond};"""
        rows = self.get_row_list(command)
        return command, rows
    
    def order_by(self, table, column, cond):
        cond = f"WHERE {cond}" if cond else ""
        command = f"""SELECT * FROM {table} {cond} ORDER BY {column};"""
        rows = self.get_row_list(command)
        return command, rows

    def insert(self, table, columns, values):
        command = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return command, self.cursor.execute(command)

    def update(self, table, setValue, whereValue):
        command = f"UPDATE {table} SET {setValue} WHERE {whereValue}"
        self.cursor.execute(command)
        return command

    def delete(self, table, condition):
        command = f"DELETE FROM {table} WHERE {condition}"
        return self.cursor.execute(command)

    def get_column_names(self, table):
        """ Returns a list and comma separated string of column 
            names from the given table. The list is for setting table 
            column headers, and the string for a database query."""

        column_list, columns = [], "" 
        rows = self.cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")
        for row in rows:
            columns += row[3] + ',' # third elem is name
            column_list.append(row[3])
        return column_list, columns[:-1] 

    def get_row_list(self, cmd):
        rows = []
        for row in self.cursor.execute(cmd):
            temp = []
            for cell in row:
                temp.append(cell)
            rows.append(temp)
        return rows