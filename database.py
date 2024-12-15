from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import os

# Root
root = Tk()
root.title("My Code")
root.iconbitmap('c:/Users/Documents/Python/GUI')
root.geometry("400x400")

# Creating a Database
db_dir = 'c:/Users/Documents/Python/GUI/'
db_path = os.path.join(db_dir, 'wresting.db')

connect = None

# Creating a table
try:
    # Command to connect the database
    connect = sqlite3.connect('wrestling.db')
    cur = connect.cursor()
    # Create Database
    print("database has been created")

    cur.execute("""CREATE TABLE IF NOT EXISTS Promotions (
            promotions_name TEXT,
            owner_name TEXT,
            based_in TEXT,
            date_founded DATE,
            size TEXT,
            style TEXT
        ) """)
    
    # Delete Function
    def delButton():
        connect = sqlite3.connect('wrestling.db')
        cur = connect.cursor()

        # Table
        cur.execute("DELETE from Promotions WHERE oid= " + selBox.get())

        connect.commit()

        connect.close()
    
    # Submit Function
    def subButton():
        connect = sqlite3.connect('wrestling.db')
        cur = connect.cursor()

        # Table
        cur.execute("INSERT INTO Promotions VALUES (:p_name, :o_name, :based, :date_found, :p_size, :p_style)",
                   {
                       'p_name': p_name.get(),
                       'o_name': o_name.get(),
                       'based': based.get(),
                       'date_found': date_found.get(),
                       'p_size': p_size.get(),
                       'p_style': p_style.get()
                   })

        connect.commit()

        connect.close()

        # Clear Text Box
        p_name.delete(0, END)
        o_name.delete(0, END)
        based.delete(0, END)
        date_found.delete(0, END)
        p_size.delete(0, END)
        p_style.delete(0, END)

    # Show Button
    def showButton():
        connect = sqlite3.connect('wrestling.db')
        cur = connect.cursor()

        cur.execute("SELECT *, oid FROM Promotions")
        promotions = cur.fetchall()
        # print(promotions)
        print_promotions = ''

        # Results
        for promotion in promotions:
            print_promotions += str(promotion[0]) + " " + str(promotion[6]) +"\n"

        promotion_label = Label(root, text=print_promotions)
        promotion_label.grid(row=12, column=0, columnspan=2)

        connect.commit()

        connect.close()

    # Update Button
    def updateButton():
        global update
        update = Tk()
        update.title("Update a Record")
        update.iconbitmap('c:/Users/corru/OneDrive/Documents/Python/GUI')
        update.geometry("400x400")

        connect = sqlite3.connect('wrestling.db')
        cur = connect.cursor()

        promotion_id = selBox.get()
        cur.execute("SELECT * FROM Promotions WHERE oid = " + promotion_id)
        promotions = cur.fetchall()

        # Global Variables
        global p_nameUpdate
        global o_nameUpdate
        global basedUpdate
        global date_foundUpdate
        global p_sizeUpdate
        global p_styleUpdate

        # Text Boxes
        p_nameUpdate = Entry(update, width=30)
        p_nameUpdate.grid(row=0, column=1, padx=20, pady=(10, 0))
        o_nameUpdate = Entry(update, width=30)
        o_nameUpdate.grid(row=1, column=1, padx=20)
        basedUpdate = Entry(update, width=30)
        basedUpdate.grid(row=2, column=1, padx=20)
        date_foundUpdate = Entry(update, width=30)
        date_foundUpdate.grid(row=3, column=1, padx=20)
        p_sizeUpdate = Entry(update, width=30)
        p_sizeUpdate.grid(row=4, column=1, padx=20)
        p_styleUpdate = Entry(update, width=30)
        p_styleUpdate.grid(row=5, column=1, padx=20)

        # Text Box Labels
        p_nameUpdate_label = Label(update, text="Promotion Name")
        p_nameUpdate_label.grid(row=0, column=0, pady= (10, 0))
        o_nameUpdate_label = Label(update, text="Owner Name")
        o_nameUpdate_label.grid(row=1, column=0)
        basedUpdate_label = Label(update, text="Based In")
        basedUpdate_label.grid(row=2, column=0)
        date_foundUpdate_label = Label(update, text="Date Found")
        date_foundUpdate_label.grid(row=3, column=0)
        p_sizeUpdate_label = Label(update, text="Promotion Size")
        p_sizeUpdate_label.grid(row=4, column=0)
        p_styleUpdate_label = Label(update, text="Promotion Style")
        p_styleUpdate_label.grid(row=5, column=0)

        # Insert
        for promotion in promotions:
            p_nameUpdate.insert(0, promotion[0])
            o_nameUpdate.insert(0, promotion[1])
            basedUpdate.insert(0, promotion[2])
            date_foundUpdate.insert(0, promotion[3])
            p_sizeUpdate.insert(0, promotion[4])
            p_styleUpdate.insert(0, promotion[5])

        # Update Button
        save_button = Button(update, text="Update Record", command=saveButton)
        save_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        connect.commit()

        connect.close()

    # Save Button
    def saveButton():
        connect = sqlite3.connect('wrestling.db')
        cur = connect.cursor()

        promotion_id = selBox.get()

        cur.execute("""UPDATE Promotions SET
                'promotions_name' = :p_name,
                'owner_name'= :o_name,
                'based_in' = :based,
                'date_founded'= :date_found,
                'size' = :p_size,
                'style' = :p_style   
                WHERE oid =:oid""",
                { 
                'p_name': p_nameUpdate.get(),
                'o_name': o_nameUpdate.get(),
                'based': basedUpdate.get(),
                'date_found': date_foundUpdate.get(),
                'p_size': p_sizeUpdate.get(),
                'p_style': p_styleUpdate.get(),

                'oid': promotion_id
                })

        # Commit Changes
        connect.commit()

        connect.close()

        # Clear Text Box
        p_nameUpdate.delete(0, END)
        o_nameUpdate.delete(0, END)
        basedUpdate.delete(0, END)
        date_foundUpdate.delete(0, END)
        p_sizeUpdate.delete(0, END)
        p_styleUpdate.delete(0, END)

        update.destroy()

    # Text Boxes
    p_name = Entry(root, width=30)
    p_name.grid(row=0, column=1, padx=20, pady=(10, 0))
    o_name = Entry(root, width=30)
    o_name.grid(row=1, column=1, padx=20)
    based = Entry(root, width=30)
    based.grid(row=2, column=1, padx=20)
    date_found = Entry(root, width=30)
    date_found.grid(row=3, column=1, padx=20)
    p_size = Entry(root, width=30)
    p_size.grid(row=4, column=1, padx=20)
    p_style = Entry(root, width=30)
    p_style.grid(row=5, column=1, padx=20)
    selBox = Entry(root, width=30)
    selBox.grid(row=6, column=1, padx=20)

    # Text Box Labels
    p_name_label = Label(root, text="Promotion Name")
    p_name_label.grid(row=0, column=0, pady= (10, 0))
    o_name_label = Label(root, text="Owner Name")
    o_name_label.grid(row=1, column=0)
    based_label = Label(root, text="Based In")
    based_label.grid(row=2, column=0)
    date_found_label = Label(root, text="Date Found")
    date_found_label.grid(row=3, column=0)
    p_size_label = Label(root, text="Promotion Size")
    p_size_label.grid(row=4, column=0)
    p_style_label = Label(root, text="Promotion Style")
    p_style_label.grid(row=5, column=0)
    selBox_label = Label(root, text="Select ID")
    selBox_label.grid(row=6, column=0, pady=5)

    # Submit Button
    sub_button = Button(root, text="Add Record", command=subButton)
    sub_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Query Button
    show_button = Button(root, text="Show Record", command=showButton)
    show_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Delete Button
    del_button = Button(root, text="Delete Record", command=delButton)
    del_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Update Button
    update_button = Button(root, text="Update Record", command=updateButton)
    update_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Commit Changes
    connect.commit()

except sqlite3.OperationalError as e:
    print(f"SQLite Error has occoured: {e}")

except Exception as e:
    print(f"Error has occured {e}")

finally:
    if connect:
        # Connection Close
        connect.close()
        print("Database connection has closed")

# Excution
root.mainloop()
