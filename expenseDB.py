import sqlite3

# -- Database Connection Set-Up

# -- Establishes a connection to the SQLite database expenses.db and creates a cursor object
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# ---- Creating the Database ----

# -- Create expenses table to store individual expense entries if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS Expenses(
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          description TEXT,                      
          category TEXT,                        
          date TEXT,                             
          amount REAL                           
    )
""")

# -- Create categories table to store unique expense categories if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS Categories(
          id INTEGER PRIMARY KEY,                
          name TEXT UNIQUE                       
    )
""")

# -- Define default categories for the categories table
defaultCategories = [
    'Food',
    'Shopping',
    'Utilities',
    'Gas',
    'Fun'
]

# -- Insert default categories into categories table if they do not already exist
for category in defaultCategories:
    with conn:
        c.execute("INSERT OR IGNORE INTO Categories (name) VALUES (:name)", {"name": category})

# ---- Creating the Functions ----

# -- Function to add an expense entry to the expenses table
def addExpense(description, category, date, amount):
    with conn:
        c.execute(
            "INSERT INTO Expenses (description, category, date, amount) VALUES (:description, :category, :date, :amount)",
            {"description": description, "category": category, "date": date, "amount": amount}
        )

# -- Function to add a new category to the categories table
def addCategory(categoryName):
    try:
        with conn:
            c.execute("INSERT INTO Categories (name) VALUES (:name)", {"name": categoryName})
            return True
    except sqlite3.IntegrityError:
        return False

# -- Function to retrieve a list of all categories from the categories table
def getCategories():
    c.execute("SELECT name FROM Categories")
    return [row[0] for row in c.fetchall()]

# -- Function to retrieve all expenses from the expenses table
def viewExpenses():
    c.execute("SELECT * FROM Expenses")
    return c.fetchall()

# -- Function to calculate the total amount of all expenses
def totalExpenses():
    c.execute("SELECT SUM(amount) FROM Expenses")
    total = c.fetchone()[0]
    return total if total is not None else 0.0

# -- Function to close the Database Connection
def closeConnection():
    conn.close()
