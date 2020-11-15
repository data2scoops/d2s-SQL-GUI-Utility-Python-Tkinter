from tkinter import *
import pyodbc


# Function to connect to SQL Database
def connect(server, database, username, password):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        + ';SERVER=' + server
        + ';DATABASE=' + database
        + ';UID=' + username
        + ';PWD=' + password,
        autocommit=True)
    cursor = conn.cursor()
    return cursor


# Function to submit data to SQL Server
def submit(server,
           database,
           username,
           password,
           clientid,
           last_name,
           first_name,
           city):
    cursor = connect(server, database, username, password)
    run_sql = f"""INSERT INTO [dbo].[Clients](ClientID, LastName, FirstName, City) 
                VALUES({clientid}, '{last_name}', '{first_name}', '{city}')"""

    try:
        cursor.execute(run_sql)
        return f"Record Inserted: {run_sql}"
    except pyodbc.IntegrityError:
        return f"primary key violation {run_sql}"
    except pyodbc.ProgrammingError:
        return "Other error"


# function to create parameterless function to be called later
def submit_data():
    list_output.delete(0, END)
    row = submit(server_text.get(),
                 database_text.get(),
                 username_text.get(),
                 password_text.get(),
                 clientid_text.get(),
                 last_name_text.get(),
                 first_name_text.get(),
                 city_text.get()
                 )
    list_output.insert(END, row)


# Show button function
def show_submitted(server, database, username, password, table, clientid):
    cursor = connect(server, database, username, password)
    run_sql = f"SELECT * FROM {table} where ClientID = '{clientid}'"
    try:
        cursor.execute(run_sql)
        return cursor.fetchall()
    except:
        return 'Something went wrong with input', 'please check', '!'


# Show button function parameterless
def show_details():
    list_output.delete(0, END)
    i = 0
    for row in show_submitted(
            server_text.get(),
            database_text.get(),
            username_text.get(),
            password_text.get(),
            table_text.get(),
            clientid_text.get()):
        i += 1
        list_output.insert(END, (i, row))


# function to clear output space
def clear_details():
    list_output.delete(0, END)


if __name__ == '__main__':
    # GUI Window for our Application
    window = Tk()

    # Create a label for SQL Database and login information
    l_sql_label = Label(window, text="SQL Authentication", fg="white", bg="black", width="30")
    l_sql_label.grid(row=0, column=1)

    l_server = Label(window, text="Server", relief="raised")
    l_server.grid(row=1, column=0)

    server_text = StringVar()
    e_server_text = Entry(window, textvariable=server_text, borderwidth=2, relief="sunken")
    e_server_text.grid(row=1, column=1)

    l_database = Label(window, text="Database", relief="raised")
    l_database.grid(row=2, column=0)

    database_text = StringVar()
    e_database_text = Entry(window, textvariable=database_text, borderwidth=2, relief="sunken")
    e_database_text.grid(row=2, column=1)

    l_username = Label(window, text="Username", relief="raised")
    l_username.grid(row=1, column=2)

    username_text = StringVar()
    e_username_text = Entry(window, textvariable=username_text, borderwidth=2, relief="sunken")
    e_username_text.grid(row=1, column=3)

    l_password = Label(window, text="Password", relief="raised")
    l_password.grid(row=2, column=2)

    password_text = StringVar()
    l_password_text = Entry(window, textvariable=password_text, show="*", borderwidth=2, relief="sunken")
    l_password_text.grid(row=2, column=3)

    # Get Client details to enter in the SQL table
    l_client_details = Label(window, text="Client Details", fg="white", bg="black", width="30")
    l_client_details.grid(row=3, column=1)

    l_client_id = Label(window, text="ClientID", relief="raised")
    l_client_id.grid(row=4, column=0)

    clientid_text = StringVar()
    e_clientid_text = Entry(window, textvariable=clientid_text, borderwidth=2, relief="sunken")
    e_clientid_text.grid(row=4, column=1)

    l_last_name = Label(window, text="Last Name", relief="raised")
    l_last_name.grid(row=4, column=2)

    last_name_text = StringVar()
    e_last_name = Entry(window, textvariable=last_name_text, borderwidth=2, relief="sunken")
    e_last_name.grid(row=4, column=3)

    l_first_name = Label(window, text="First Name", relief="raised")
    l_first_name.grid(row=5, column=2)

    first_name_text = StringVar()
    e_first_name = Entry(window, textvariable=first_name_text, borderwidth=2, relief="sunken")
    e_first_name.grid(row=5, column=3)

    l_city = Label(window, text="City", relief="raised")
    l_city.grid(row=5, column=0)

    city_text = StringVar()
    e_city = Entry(window, textvariable=city_text, borderwidth=2, relief="sunken")
    e_city.grid(row=5, column=1)

    # Create submit button
    b_submit = Button(window, text="Submit", width=10, command=submit_data, borderwidth=5, relief="raised")
    b_submit.grid(row=6, column=1)

    # Create output space to look out results
    list_output = Listbox(window, height=15, width=75, borderwidth=5, relief="sunken")
    list_output.grid(row=7, column=0, columnspan=8)

    # add scrollbar in case there are large number of records
    y_scroll_bar = Scrollbar(window)
    y_scroll_bar.grid(row=7, column=5, rowspan=6)

    # configure scroll bar with output space
    list_output.configure(yscrollcommand=y_scroll_bar.set)
    y_scroll_bar.configure(command=list_output.yview)

    # add scroll bar along x axis
    x_scroll_bar = Scrollbar(window, orient='horizontal')
    x_scroll_bar.grid(row=8, column=1, columnspan=3)

    # configure x axis scroll bar with output space area
    list_output.configure(xscrollcommand=x_scroll_bar.set)
    x_scroll_bar.configure(command=list_output.xview)

    # addition of table and primary key to fetch records
    l_table = Label(window, text="Table", relief="raised")
    l_table.grid(row=9, column=0)

    table_text = StringVar()
    e_table_text = Entry(window, textvariable=table_text, borderwidth=2, relief="sunken")
    e_table_text.grid(row=9, column=1)

    l_search_key = Label(window, text="ClientID", relief="raised")
    l_search_key.grid(row=9, column=2)

    search_key_text = StringVar()
    e_search_key_text = Entry(window, textvariable=search_key_text, borderwidth=2, relief="sunken")
    e_search_key_text.grid(row=9, column=3)

    # view button
    b_show = Button(window, text="Show", width=10, command=show_details, borderwidth=5, relief="raised")
    b_show.grid(row=9, column=4)

    # Clear button
    b_clear = Button(window, text="Clear", width=10, command=clear_details, borderwidth=5, relief="raised")
    b_clear.grid(row=9, column=5)

    window.mainloop()
