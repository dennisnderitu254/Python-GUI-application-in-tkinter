#!/usr/bin/python3

# This is a GUI application Performing CRUD Operations on a DATABASE

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0,select['student_registration'])
    e2.insert(0,select['student_name'])
    e3.insert(0,select['student_email'])
    e4.insert(0,select['student_county'])

def Add():
    stud_reg = e1.get()
    stud_name = e2.get()
    stud_email = e3.get()
    stud_county = e4.get()

    mysqldb=mysql.connector.connect(host='localhost', user='admin', password='Root@1234', database='campus_registration')
    mycursor=mysqldb.cursor()

    try:
        mycursor.callproc("insert_student")
        # sql = "INSERT INTO student_details(student_registration, student_name, student_email, student_county) VALUES(%s,%s,%s,%s)"
        # val = (stud_reg, stud_name, stud_email, stud_county)
        # mycursor.execute(sql, val)
        mycursor.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Employee inserted Successfully....")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

        e1.focus_set()
    except Exception as e:
        print(e)
        # mysqldb.rollblack()
        mysqldb.close()

def update():
    stud_reg = e1.get()
    stud_name = e2.get()
    stud_email = e3.get()
    stud_county = e4.get()

    mysqldb=mysql.connector.connect(host='localhost', user='admin', password='Root@1234', database='campus_registration')
    mycursor=mysqldb.cursor()

    try:
        mycursor.callproc("update_student")
        # sql = "UPDATE student_details SET student_name= %s,student_email= %s, student_county= %s WHERE student_registration= %s"
        # val = (stud_name, stud_email, stud_county, stud_reg)
        # mycursor.execute(sql, val)
        mysqldb.commit()
        
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record Updated successfully...")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()

    except Exception as e:

       print(e)
       mysqldb.rollback()
       mysqldb.close()

def delete():
    stud_reg = e1.get()

    mysqldb=mysql.connector.connect(host='localhost', user='admin', password='Root@1234', database='campus_registration')
    mycursor=mysqldb.cursor()

    try:
        # mycursor.callproc("delete_student")
        sql = "DELETE FROM student_details WHERE student_registration = %s"
        val = (stud_reg)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record Deleteeeee successfully...")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()

    except Exception as e:

       print(e)
       mysqldb.rollback()
       mysqldb.close()

def show():
        mysqldb = mysql.connector.connect(host='localhost', user='admin', password='Root@1234', database='campus_registration')
        mycursor = mysqldb.cursor()
        # mycursor.callproc("list_all_students")
        mycursor.execute("SELECT student_registration,student_name,student_email,student_county FROM student_details")
        records = mycursor.fetchall()
        print(records)

        for i, (stud_reg,stud_name, stud_email,stud_county) in enumerate(records, start=1):
            listBox.insert("", "end", values=(stud_reg,stud_name, stud_email,stud_county))
            mysqldb.close()

root = Tk()
root.geometry("800x500")
global e1
global e2
global e3
global e4

tk.Label(root, text="Campus Registation", fg="red", font=(None, 30)).place(x=300, y=5)

tk.Label(root, text="Student Reg.No").place(x=10, y=10)
Label(root, text="Student Name").place(x=10, y=40)
Label(root, text="Student Email").place(x=10, y=70)
Label(root, text="Student County").place(x=10, y=100)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)

e3 = Entry(root)
e3.place(x=140, y=70)

e4 = Entry(root)
e4.place(x=140, y=100)

Button(root, text="Add",command = Add,height=3, width= 13).place(x=30, y=130)
Button(root, text="update",command = update,height=3, width= 13).place(x=140, y=130)
Button(root, text="Delete",command = delete,height=3, width= 13).place(x=250, y=130)
Button(root, text="ShowAll",command = show,height=3, width= 13).place(x=250, y=130)


    def getvalue(self, event):
    
cols = ('student_registration', 'student_name', 'student_email','student_county')
listBox = ttk.Treeview(root, columns=cols, show='headings' )

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=200)

Button(root, text="Add",command = Add,height=3, width= 13).place(x=30, y=130)
Button(root, text="update",command = update,height=3, width= 13).place(x=140, y=130)
Button(root, text="Delete",command = delete,height=3, width= 13).place(x=250, y=130)

cols = ('student_registration', 'student_name', 'student_email','student_county')
listBox = ttk.Treeview(root, columns=cols, show='headings' )

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=200)

# show()
listBox.bind('<Double-Button-1>',GetValue)

root.mainloop()
