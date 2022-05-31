#!/usr/bin/python3
from select import select
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

# root window
# root = Tk()
# root.geometry("400x400")

class Campusreg(Frame):
    def __init__(self):
        self.DB = DB()
        self.root = Tk()
        # self.stud_regno = StringVar()
        self.root.geometry("1000x600")
        self.root.title("Campus Registration System")

        self.var =StringVar()

        self.stud_regno = Label(self.root , text="Student Registration:", width = 25)
        self.stud_regno.grid(row=1,column=1)

        self.stud_name = Label(self.root , text="Student Name:", width = 25)
        self.stud_name.grid(row=2,column=1)

        self.stud_email = Label(self.root , text="Student Email:", width = 25)
        self.stud_email.grid(row=3,column=1)

        self.stud_county = Label(self.root , text="Student County:", width = 25)
        self.stud_county.grid(row=4,column=1)

        self.reg_entry = Entry(self.root, width=25, borderwidth=8)
        self.reg_entry.grid(row=1, column=2)

        self.studname_entry = Entry(self.root, width=25, borderwidth=8)
        self.studname_entry.grid(row=2, column=2)

        self.studemail_entry = Entry(self.root, width=25, borderwidth = 8)
        self.studemail_entry.grid(row=3, column=2)

        self.studcounty_entry = Entry(self.root, width=25, borderwidth = 8)
        self.studcounty_entry.grid(row=4, column=2)

        self.register = Button(self.root, text="Register", width = 10, command=self.add_student)
        self.register.grid(row = 5, column = 1, padx=5)
  
        self.update = Button(self.root, text="Update", width = 10)
        self.update.grid(row = 5, column = 2)

        self.delete = Button(self.root, text="Delete", width = 10)
        self.delete.grid(row = 5, column = 3)

        self.clear = Button(self.root, text="Clear", width = 10)
        self.clear.grid(row = 5, column = 4)

        self.showall = Button(self.root, text="ShowAll", width = 10, command = self.showdata)
        self.showall.grid(row = 5, column = 5)

        self.search = Label(self.root , text="Search", width = 10)
        self.search.grid(row=11,column=2)

        self.search_entry = Entry(self.root, text="Search", width = 25, borderwidth = 8)
        self.search_entry.grid(row = 11, column = 3)

        self.showinfo = Label(self.root , textvariable= self.var, width = 10)
        self.showinfo.grid(row=13,column=2)
        
        self.cols = ('student_registration', 'student_name', 'student_email','student_county')
        self.listBox = ttk.Treeview(self.root, columns=self.cols, show='headings' )
        
        for col in self.cols:
            self.listBox.heading(col, text=col)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.place(x=50, y=200)
            
        self.listBox.bind('<Double-Button-1>',self.getvalue)


        self.root.mainloop()

    def getroot(self):
        return self.root

    def showdata(self):
        details = self.DB.select_all()
        student = ""
        
        # for insterting data in listbox
        self.handle_details(details)
        
      
    def handle_details(self, details):
        # spacer = " "
        # student = str(detail[0]) + spacer + detail[1] + spacer + detail[2] + spacer + detail[3]
        
        # stud_reg = detail[0]
        # stud_name = detail[1]
        # stud_email = detail[2]
        # stud_county = detail[3]
        
        for i, (stud_reg,stud_name, stud_email,stud_county) in enumerate(details, start=1):
            self.listBox.insert("", "end", values=(stud_reg,stud_name, stud_email,stud_county))
        
        # print(student)
    
        # return student
        
    def clearentry(self):
        self.reg_entry.delete(0,END)
        self.studname_entry.delete(0,END)
        self.studemail_entry.delete(0,END)
        self.studcounty_entry.delete(0,END)
        
    def addvalue(self):
        
        studentregno = self.listBox.selection()[0]
        select = self.listBox.set(studentregno)
        self.reg_entry.insert(0,select['student_registration'])
        self.studname_entry.insert(0,select['student_name'])
        self.studemail_entry.insert(0,select['student_email'])
        self.studcounty_entry.insert(0,select['student_county'])
        
        
    
    def getvalue(self, event):
        self.clearentry()
        self.addvalue()
        
    def add_student(self):
        # student_id = self.reg_entry.get()
        student_name = self.studname_entry.get()
        student_email = self.studemail_entry.get()
        student_county = self.studcounty_entry.get()
        
        details = self.DB.addstudent(student_name,student_email,student_county)
        
        # self.handle_details(details)
             


class DB():
    def __init__(self, host='localhost', user='admin', password='Root@1234', database='campus_registration'):
        self.host   = host
        self.user   = user
        self.password = password
        self.database = database
        self.mydb =mysql.connector.connect(
                   host =self.host,
                   user = self.user,
                   password = self.password,
                   database =self.database,
                   )
        # self.cur = self.conn.cursor()
        # self.conn.commit()

    def select_all(self):
        details = None
        obj = self.mydb.cursor()
        obj.callproc("list_students")
        

        for result in obj.stored_results():
            details = result.fetchall()
            # print(details)
            # messagebox('students',details)

            # for det in details:
            #     print(det)

        return details

    def searchstudent(self, studname):
        details = None
        obj = self.mydb.cursor()
        obj.callproc("search_student", [studname])
        

        for result in obj.stored_results():
            details = result.fetchall()
            
        return details


    def updatestudent(self, studentreg, studentname, studentemail, studentcounty):
        self.details = None
        obj = self.mydb.cursor()
        obj.callproc("update_student",[studentreg], [studentname], [studentemail], [studentcounty])
        
        
        for result in obj.stored_results():
            details = result.fetchall()
        
        return details
        
       
    
    def addstudent(self, name, email, county):
        details = None
        obj = self.mydb.cursor()
        obj.callproc("insert_student", [name, email, county])
        
        for result in obj.stored_results():
            details = result.fetchall()
            print(details)
            
        return details
            
            
            

    def __exit__(self):
        self.mydb.close()



def main():
    # Campusreg().mainloop()
    # r = Campusreg()
    # r.select_all()
    # r.getroot().title("Uni Registration")
    # print()
    # r.mainloop()
    
    r = DB()
    
    k = r.addstudent('Kerry Rowland' , 'kerryrowland@yahoo.com', 'Arizona')
    
    print(k)

if __name__ == '__main__':
    main()
