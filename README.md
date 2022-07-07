# restoran-bp
A GUI for a Databases class term paper (Restaurant)

Requirements:</br>
- MS SQL Server</br>
- python, modules:</br>
  - pyside6</br>
  - pyodbc</br>
  
Install steps:</br>
- Install MS SQL Server and restore from backup 
  the database located under assets/db/ 
- Install python and required modules
- Change the server name in the db.py file in the DbHandler 
  class self.conn object to your device or server name
- Start the program with 'python main.py' while in the
  repository root

Assignment:</br>
    In your term paper present a database project that shows the record</br>
keeping and usage od restaurant data. Implement record keeping of 
products, tables, seats, workers, guest traffic and other things,
as needed.</br>
    Show database capabilities with apropriate queries that illustrate
functionality according to diverse criteria.</br>
-   Model an SQL database on the given topic - show ER diagram
-   Show the usage of following data types:
    -   Date (3 entities minimum)
    -   AlphaNumeric
    -   Numeric (integer and floating point)
    -   and other
-   Implement integrities (entity, domain and referential level)
-   Provide needed data to illustrate data access techniques
-   
-   Show usage of functions (date, string, aggregate, numeric, general)
-   
-   
-   Show queries on multiple tables (all variations of JOIN)
-   If possible, use one of the CASE tools for database modeling
