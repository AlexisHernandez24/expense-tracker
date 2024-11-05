from tkinter import *
from tkinter import messagebox, ttk
import expenseDB as database

# ---- Creating the Main Window ----
window = Tk()
window.title("Expense Tracker")
window.geometry("500x600")
window.configure(bg = "#1e1e1e")  # Dark background for the window

# -- Set up a style for the themed widgets
style = ttk.Style()
style.theme_use("clam")

# -- Define dark-themed colors and minimalistic styles
bgColor = "#1e1e1e"          # Dark background
entryBg = "#2e2e2e"          # Slightly lighter dark color for entries
buttonBg = "#3e8e7e"         # Accent color for buttons
buttonHoverBg = "#5ea89f"   # Slight hover effect color for buttons
labelColor = "#cccccc"       # Soft white color for labels
fontMain = ("Helvetica", 11)
fontTitle = ("Helvetica", 18, "bold")

# -- Configure styles for labels, entries, and buttons
style.configure("TLabel", background = bgColor, foreground = labelColor, font = fontMain)
style.configure("TEntry", fieldbackground = entryBg, font = fontMain, foreground = "white", padding = 5)
style.configure("TButton", font = fontMain, background = buttonBg, foreground = "white", padding = 8, borderwidth = 0)
style.map("TButton", background = [("active", buttonHoverBg)])

# -- Define default categories
defaultCategories = ['Food', 'Shopping', 'Utilities', 'Gas', 'Fun']
categoryVar = StringVar()
categoryVar.set(defaultCategories[0])

# ---- Creating Minimalistic Header ----
header = Label(window, text = "Expense Tracker", font = fontTitle, fg = labelColor, bg = bgColor)
header.grid(row = 0, column = 0, columnspan = 2, pady = (20, 10), padx = 20, sticky = "W")

# ---- Creating Widgets ----

# -- Description Label and Entry
descriptionLabel = ttk.Label(window, text = "Description")
descriptionLabel.grid(row = 1, column = 0, padx = 20, pady = (10, 5), sticky = "W")
descriptionEntry = ttk.Entry(window)
descriptionEntry.grid(row = 1, column = 1, padx = 20, pady = (10, 5), sticky = "EW")

# -- New Category Label and Entry
newCategoryLabel = ttk.Label(window, text = "New Category")
newCategoryLabel.grid(row = 2, column = 0, padx = 20, pady = (10, 5), sticky = "W")
newCategoryEntry = ttk.Entry(window)
newCategoryEntry.grid(row = 2, column = 1, padx = 20, pady = (10, 5), sticky = "EW")

# -- Category Dropdown
categoryLabel = ttk.Label(window, text = "Category")
categoryLabel.grid(row = 3, column = 0, padx = 20, pady = (10, 5), sticky = "W")
categoryList = ttk.OptionMenu(window, categoryVar, *defaultCategories)
categoryList.grid(row = 3, column = 1, padx = 20, pady = (10, 5), sticky = "EW")

# -- Date Entry
dateLabel = ttk.Label(window, text = "Date (YYYY-MM-DD)")
dateLabel.grid(row = 4, column = 0, padx = 20, pady = (10, 5), sticky = "W")
dateEntry = ttk.Entry(window)
dateEntry.grid(row = 4, column = 1, padx = 20, pady = (10, 5), sticky = "EW")

# -- Amount Entry
amountLabel = ttk.Label(window, text = "Amount")
amountLabel.grid(row = 5, column = 0, padx= 20, pady = (10, 5), sticky = "W")
amountEntry = ttk.Entry(window)
amountEntry.grid(row = 5, column = 1, padx = 20, pady = (10, 5), sticky = "EW")

# ---- Functions for Functionality ----
# -- Function to add a brand new category to the Listmenu and to the Database
def addCategory():
    newCategory = newCategoryEntry.get()
    if newCategory:
        if database.addCategory(newCategory):
            newCategoryEntry.delete(0, END)
            updateCategoryMenu()
            messagebox.showinfo("Expense Tracker", f"Category '{newCategory}' added successfully!")
        else:
            messagebox.showerror("Error", "Category already exists.")
    else:
        messagebox.showwarning("Warning", "Category name cannot be empty.")

# -- Function to update the category menu after adding a new category
def updateCategoryMenu():
    categoryList['menu'].delete(0, 'end')
    categories = database.getCategories()
    for category in categories:
        categoryList['menu'].add_command(label = category, command = lambda v = category: categoryVar.set(v))

# -- Function to add an expense through the GUI
def addExpense():
    description = descriptionEntry.get()
    category = categoryVar.get()  
    date = dateEntry.get()
    try:
        amount = float(amountEntry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid amount")
        return
    
    database.addExpense(description, category, date, amount)
    descriptionEntry.delete(0, END)
    amountEntry.delete(0, END)
    dateEntry.delete(0, END)
    showExpenses()
    messagebox.showinfo("Expense Tracker", "Expense added successfully!")

# -- Function to display expenses
def showExpenses():
    rows = database.viewExpenses()
    expenseList.delete(0, END)
    for row in rows:
        expenseList.insert(END, f"{row[1]} - {row[2]} - {row[3]} - ${row[4]:.2f}")

# -- Function to calculate total expense
def calculateTotal():
    total = database.totalExpenses()
    messagebox.showinfo("Total Expenses", f"Total Expense: ${total:.2f}")
        
# ---- Buttons ----
addExpenseButton = ttk.Button(window, text = "Add Expense", command = addExpense)
addExpenseButton.grid(row = 6, column = 0, columnspan = 2, pady = 15, padx = 20, sticky = "EW")

viewExpenseButton = ttk.Button(window, text = "View Expense", command = showExpenses)
viewExpenseButton.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 20, sticky = "EW")

totalExpenseButton = ttk.Button(window, text = "Total Expense", command = calculateTotal)
totalExpenseButton.grid(row = 8, column = 0, columnspan = 2, pady = 10, padx = 20, sticky = "EW")

addCategoryButton = ttk.Button(window, text = "Add Category", command = addCategory)
addCategoryButton.grid(row = 9, column = 0, columnspan = 2, pady = 10, padx = 20, sticky = "EW")

# ---- Expense List with Scrollbar ----
expenseListFrame = Frame(window, bg = bgColor)
expenseListFrame.grid(row = 10, column = 0, columnspan = 2, pady = 15, padx = 20, sticky = "EW")
expenseList = Listbox(expenseListFrame, width = 50, height = 10, bg = entryBg, fg = "white", font = fontMain, selectbackground = buttonBg)
expenseList.pack(side = LEFT, fill = BOTH, expand = True)
scrollbar = Scrollbar(expenseListFrame)
scrollbar.pack(side = RIGHT, fill = Y)
expenseList.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = expenseList.yview)

window.columnconfigure(1, weight = 1)  # Make columns expandable
window.mainloop()