# ----- Task.Do ---------------------------------------------------------------------------------------------------- #

# Task.Do is a to-do list that helps you organize your tasks
# Created by Steven Pereira aka Cursed Cancer
# Github: https://github.com/CursedCancer

# ----- Import Section --------------------------------------------------------------------------------------------- #

import sqlite3
import os
import time
import typer
from rich import print
from rich import box
from rich.console import Console
from rich.table import Table
from rich.table import Column

# ----- Global Declaration ----------------------------------------------------------------------------------------- #

console = Console()
app = typer.Typer()

# ----- Database --------------------------------------------------------------------------------------------------- #

def database_connect():
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    connect.commit()
    return connect

def database_create():
    if os.path.exists (r"Database/"):
        if os.path.exists(r"Database/TaskDo.db"):
            database_connect()
            pass
        else:
            database_connect()
    else:
        os.mkdir(r"Database/")
        database_connect()

# ----- Tables ----------------------------------------------------------------------------------------------------- #

def tables():
    database_create()
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS 'Tasks'
                    (
                        ID                  INTEGER            Primary Key,
                        Name                CHAR(100),
                        Status              TEXT(100))''')
    connect.commit()

# ----- Banner ----------------------------------------------------------------------------------------------------- #

def ascii():
    console.print(r"""[#79d45e]
        ┌──────────────────────────────────────────────────────────────────────────────────────┐
        │                                                                                      │                   
        │        [#a484e9] _________  ________  ________  ___  __        ________  ________ [#79d45e]            │
        │        [#a484e9]|\___   ___\\   __  \|\   ____\|\  \|\  \     |\   ___ \|\   __  \ [#79d45e]           │
        │        [#a484e9]\|___ \  \_\ \  \|\  \ \  \___|\ \  \/  /|_   \ \  \_|\ \ \  \|\  \ [#79d45e]          │
        │             [#a484e9]\ \  \ \ \   __  \ \_____  \ \   ___  \   \ \  \ \\ \ \  \\\  \ [#79d45e]         │
        │              [#a484e9]\ \  \ \ \  \ \  \|____|\  \ \  \\ \  \ __\ \  \_\\ \ \  \\\  \ [#79d45e]        │
        │               [#a484e9]\ \__\ \ \__\ \__\____\_\  \ \__\\ \__\\__\ \_______\ \_______\ [#79d45e]       │
        │                [#a484e9]\|__|  \|__|\|__|\_________\|__| \|__\|__|\|_______|\|_______|  [#79d45e]      │
        │                          [#a484e9]      \|_________|  [#79d45e]                                        │
        │                                                                                      │
        │                                                                                      │
        │                              [#31bff3]- WELCOME TO Task.Do -[#79d45e]                                  │
        │           Task.Do is a To-Do List that helps you organize your daily tasks           │
        │                                                                                      │
        │                                      +-+-+                                           │
        │                                 [red] Cursed Cancer[#79d45e]                                       │
        │                                      +-+-+                                           │
        └──────────────────────────────────────────────────────────────────────────────────────┘
        """)


# ----- Menu ------------------------------------------------------------------------------------------------------- #

def clear():
    time.sleep(1)
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# ----- Add -------------------------------------------------------------------------------------------------------- #

@app.command()
def add():
    clear()
    ascii()
    console.print("[#5bd2f0]──────[#ffaf68] Adding a Task [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
    name = console.input("[#ffaf68]Enter the Name of the Task: ")
    check = console.input("[#ffaf68]Is this task completed? (Y/n) ")
    if check == "y" or check == "Y":
        status = "✅"
    elif check == "n" or check == "N":
        status = "❎"
    values(name, status)
    console.print("[#79d45e][+] Successfully added a Task")
    console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
    display()

# ----- Store ------------------------------------------------------------------------------------------------------ #

def values(name, status):
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    sqlQuery = "Insert into 'Tasks' (Name, Status) VALUES (?, ?)"
    values = (name, status)
    cursor.execute(sqlQuery, values)
    connect.commit()

# ----- Display ---------------------------------------------------------------------------------------------------- #

@app.command()
def display():
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    sqlQuery = "SELECT * FROM 'Tasks'"
    cursor.execute(sqlQuery)
    rows = cursor.fetchall()
    table = Table(
                    Column(header="ID", style="#B9EAED", header_style="#7CB5D2"),
                    Column(header="Name", style="#D9C4EC", header_style="#B19CD8"),
                    Column(header="Status", style="#B9EAED", header_style="#7CB5D2"),
                    box=box.ROUNDED, 
                    safe_box=False
        )
    for row in rows:
        table.add_row(str(row[0]),str(row[1]), str(row[2]))
    console.print(table)

# ----- Update ----------------------------------------------------------------------------------------------------- #

@app.command()
def update():
    clear()
    ascii()
    console.print("[#5bd2f0]──────[#ffaf68] Updating a Task [#5bd2f0]─────────────────────────────────────────────────────────────────────────────\n")
    display()
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    id_no = console.input("[#ffaf68]Enter the ID of the Task that you want to update: ")
    console.print("[#79d45e][+] Updating a Task: ")
    column_name = str.title(console.input("[#ffaf68]Enter the column name that you want to update: "))
    if column_name == "Name":
        sqlQuery = "UPDATE 'Tasks' SET Name = ? WHERE ID = ?"
        column_value = console.input("[#ffaf68]Enter the value of Name: ")
        cursor.execute(sqlQuery, ([column_value, id_no]))
        console.print("[#79d45e][+] Successfully updated a Task")
    elif column_name == "Status":
        sqlQuery = "UPDATE 'Tasks' SET Status = ? WHERE ID = ?"
        check = console.input("[#ffaf68]Is this task completed? (Y/n) ")
        if check == "y" or check == "Y":
            status = "✅"
        elif check == "n" or check == "N":
            status = "❎"
        cursor.execute(sqlQuery, ([status, id_no]))
        console.print("[#79d45e][+] Successfully updated a Task")
    else:
        console.print("[#FF756D][!] Column doesn't exists")
    connect.commit()
    console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
    display()

# ----- Delete ----------------------------------------------------------------------------------------------------- #

@app.command()
def delete():
    clear()
    ascii()
    console.print("[#5bd2f0]──────[#ffaf68] Deleting a Task [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────\n")
    display()
    connect = sqlite3.connect(r"Database/TaskDo.db")
    cursor = connect.cursor()
    multi_delete = console.input("[#ffaf68][?] Do you want to delete multiple Tasks? (Y/n) ")
    if multi_delete == "Y" or multi_delete == "y":
        id_no_1 = console.input("[#ffaf68]Enter the First ID of the Tasks Range that you want to delete: ")
        id_no_2 = console.input("[#ffaf68]Enter the Last ID of the Tasks Range that you want to delete: ")
        sqlQuery = "DELETE FROM 'Tasks' WHERE ID between ? and ?"
        cursor.execute(sqlQuery, [id_no_1, id_no_2])
        print("[#79d45e][+] Successfully deleted Multiple Tasks from Task Do")
        connect.commit()
        console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
        display()
    elif multi_delete == "N" or multi_delete == "n":
        id_no = console.input("[#ffaf68]Enter the ID of the Tasks that you want to delete: ")
        sqlQuery = "DELETE FROM 'Tasks' WHERE ID = ?"
        cursor.execute(sqlQuery, [id_no])
        print("[#79d45e][+] Successfully deleted a Task from Task Do")
        connect.commit()
        console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
        display()

# ----- Main Function ---------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    database_create()
    tables()
    app()

# ----- End -------------------------------------------------------------------------------------------------------- #