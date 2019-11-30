# -*- coding: utf-8 -*-
"""
Obsługa bazy danych książek

by Jacek Piłka
"""

import sqlite3
from os import path
import tkinter as tk
import tkinter.ttk as ttk


#Classes
class MainWindow:    
    def __init__(self,con):
        self.window=tk.Tk()
        self.window.title("Libros Datas")
        self.window.geometry("300x200")
        self.createButtons()
        self.window.mainloop()
        
    def createButtons(self):
        tk.Label(self.window).pack()
        #Add a book button
        addBook=tk.Button()
        addBook["text"]="Add a book"
        addBook["command"]=self.addBook
        addBook.pack()
        #Print all books button
        addBook=tk.Button()
        addBook["text"]="Print all books"
        addBook["command"]=self.printAll
        addBook.pack()
        #Search button
        addBook=tk.Button()
        addBook["text"]="Search for the book"
        addBook["command"]=self.searchBook
        addBook.pack()
        #Exit button
        exit=tk.Button()
        exit["text"]="Exit"
        exit["command"]=self.quit
        exit.pack()
        
        label=tk.Label(text="Libros Datas\n by Jacek Piłka \n2019")
        label.pack()
        
    def addBook(self):
        addBookWindow(con)
        
    def printAll(self):
        data=getAllBooks(con)
        printListWindow(data)
        
    def searchBook(self):
        searchWindow(con)
        
    def quit(self):
        self.window.destroy()
        
class addBookWindow:    
    def __init__(self,con):
        self.window=tk.Tk()
        self.window.title("Add a book")
        self.createControls()
        self.window.mainloop()
        
    def createControls(self):
        #Create entries for each parameter
        titleDesc = tk.Label(self.window, text="Title:")
        self.title = tk.Entry(self.window,width=40)
        titleDesc.grid(row=1,column=1)
        self.title.grid(row=1,column=2)
        
        authorDesc = tk.Label(self.window, text="Author:")
        self.author = tk.Entry(self.window,width=40)
        authorDesc.grid(row=2,column=1)
        self.author.grid(row=2,column=2)
        
        yearDesc = tk.Label(self.window, text="Year:")
        self.year = tk.Entry(self.window,width=40)
        yearDesc.grid(row=3,column=1)
        self.year.grid(row=3,column=2)
        
        publishDesc = tk.Label(self.window, text="Publisher:")
        self.publish = tk.Entry(self.window,width=40)
        publishDesc.grid(row=4,column=1)
        self.publish.grid(row=4,column=2)
        
        isbnDesc = tk.Label(self.window, text="ISBN:")
        self.isbn = tk.Entry(self.window,width=40)
        isbnDesc.grid(row=5,column=1)
        self.isbn.grid(row=5,column=2)
        
        typeDesc = tk.Label(self.window, text="Type:")
        self.typeEn = tk.Entry(self.window,width=40)
        typeDesc.grid(row=6,column=1)
        self.typeEn.grid(row=6,column=2)
        
        genreDesc = tk.Label(self.window, text="Genre:")
        self.genre = tk.Entry(self.window,width=40)
        genreDesc.grid(row=7,column=1)
        self.genre.grid(row=7,column=2)
        
        languageDesc = tk.Label(self.window, text="Language:")
        self.language = tk.Entry(self.window,width=40)
        languageDesc.grid(row=8,column=1)
        self.language.grid(row=8,column=2)
        
        statusDesc = tk.Label(self.window, text="Status:")
        self.status = tk.Entry(self.window,width=40)
        statusDesc.grid(row=9,column=1)
        self.status.grid(row=9,column=2)
        
        notesDesc = tk.Label(self.window, text="Notes:")
        self.notes = tk.Entry(self.window,width=40)
        notesDesc.grid(row=10,column=1)
        self.notes.grid(row=10,column=2)
        
        tagsDesc = tk.Label(self.window, text="Tags:")
        self.tags = tk.Entry(self.window,width=40)
        tagsDesc.grid(row=11,column=1)
        self.tags.grid(row=11,column=2)
        
        addButt=tk.Button(self.window)
        addButt["text"]="Add"
        addButt["command"]=self.add
        addButt.grid(row=12,column=1)
        
        cancelButt=tk.Button(self.window)
        cancelButt["text"]="Cancel"
        cancelButt["command"]=self.quit
        cancelButt.grid(row=12,column=2)
        
    def add(self):
        data=(self.title.get(),self.author.get(),self.year.get(),
              self.publish.get(),self.isbn.get(),self.typeEn.get(),
              self.genre.get(),self.language.get(),
              self.status.get(),self.notes.get(),self.tags.get())
        addBook(con,data)
        self.window.destroy()
        
    def quit(self):
        self.window.destroy()

class printListWindow:
    def __init__(self,bookList):
        self.window=tk.Tk()
        self.window.title("Books list")
        self.window.geometry("620x360")
        self.bookList=bookList
        self.bookIDChoose=-1
        self.createList()
        self.window.mainloop()
        
    def createList(self):
        self.bookListBox = tk.Listbox(self.window, width=100, height = 20) #Create listbox
        self.bookListBox.grid(row=1,columnspan=4)
        
        for i,book in enumerate(self.bookList):
            title = (book[1][:45] + '...') if len(book[1]) > 48 else book[1]
            author = (book[2][:45] + '...') if len(book[2]) > 48 else book[2]
            self.bookListBox.insert(tk.END, str(i+1)+'. "'+title+'" - '+author)
            
        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.place(in_=self.bookListBox, relx = 1., rely = 0, relheight = 1.)
        self.scrollbar.config(command = self.bookListBox.yview)
        self.bookListBox.bind('<<ListboxSelect>>', self.listBoxSelect)
            
        infoButt=tk.Button(self.window)
        infoButt["text"]="Info"
        infoButt["command"]=self.info
        infoButt.grid(row=2,column=0)
        
        addButt=tk.Button(self.window)
        addButt["text"]="Add"
        addButt["command"]=self.add
        addButt.grid(row=2,column=1)
        
        removeButt=tk.Button(self.window)
        removeButt["text"]="Remove"
        removeButt["command"]=self.remove
        removeButt.grid(row=2,column=2)
        
        backButt=tk.Button(self.window)
        backButt["text"]="Back"
        backButt["command"]=self.quit
        backButt.grid(row=2,column=3)
        
    def info(self):
        if self.bookIDChoose>=0:
            idBook=self.bookList[self.bookIDChoose]
            infoWindow(con,idBook[0])
        
    def listBoxSelect(self,index):
        tmp=self.bookListBox.curselection()
        self.bookIDChoose=tmp[0]
        
    def add(self):
        addBookWindow(con)
        
    def remove(self):
        if self.bookIDChoose>=0:
            idBook=self.bookList[self.bookIDChoose]
        else:
            return 0
        if tk.messagebox.askokcancel("Remove", "Do you want to remove this book?"):
            removeBook(con,idBook)
            tk.messagebox.showinfo("Removed", "The book has been removed")
            
    def quit(self):
        self.window.destroy()
        
class infoWindow:
    def __init__(self,con,idBook):
        self.window=tk.Tk()
        self.window.title("Book's info")
        self.idBook=idBook
        self.data=[]
        self.getBookInfo(idBook)
        self.createControls()
        self.window.mainloop()
        
    def getBookInfo(self,idBook):
        cursor=con.execute("SELECT * FROM books WHERE id=?",str(idBook))
        rows=cursor.fetchall()
        row=rows[0]
        for i,desc in enumerate(cursor.description):
            self.data.append((str(row[i])))
        
    def createControls(self):
        #Create entries for each parameter
        titleDesc = tk.Label(self.window, text="Title:")
        self.title = tk.Entry(self.window,width=40)
        self.title.insert(0,str(self.data[1]))
        titleDesc.grid(row=1,column=1)
        self.title.grid(row=1,column=2)
        
        authorDesc = tk.Label(self.window, text="Author:")
        self.author = tk.Entry(self.window,width=40)
        self.author.insert(0,str(self.data[2]))
        authorDesc.grid(row=2,column=1)
        self.author.grid(row=2,column=2)
        
        yearDesc = tk.Label(self.window, text="Year:")
        self.year = tk.Entry(self.window,width=40)
        self.year.insert(0,str(self.data[3]))
        yearDesc.grid(row=3,column=1)
        self.year.grid(row=3,column=2)
        
        publishDesc = tk.Label(self.window, text="Publisher:")
        self.publish = tk.Entry(self.window,width=40)
        self.publish.insert(0,str(self.data[4]))
        publishDesc.grid(row=4,column=1)
        self.publish.grid(row=4,column=2)
        
        isbnDesc = tk.Label(self.window, text="ISBN:")
        self.isbn = tk.Entry(self.window,width=40)
        self.isbn.insert(0,str(self.data[5]))
        isbnDesc.grid(row=5,column=1)
        self.isbn.grid(row=5,column=2)
        
        typeDesc = tk.Label(self.window, text="Type:")
        self.typeEn = tk.Entry(self.window,width=40)
        self.typeEn.insert(0,str(self.data[6]))
        typeDesc.grid(row=6,column=1)
        self.typeEn.grid(row=6,column=2)
        
        genreDesc = tk.Label(self.window, text="Genre:")
        self.genre = tk.Entry(self.window,width=40)
        self.genre.insert(0,str(self.data[7]))
        genreDesc.grid(row=7,column=1)
        self.genre.grid(row=7,column=2)
        
        languageDesc = tk.Label(self.window, text="Language:")
        self.language = tk.Entry(self.window,width=40)
        self.language.insert(0,str(self.data[8]))
        languageDesc.grid(row=8,column=1)
        self.language.grid(row=8,column=2)
        
        statusDesc = tk.Label(self.window, text="Status:")
        self.status = tk.Entry(self.window,width=40)
        self.status.insert(0,str(self.data[9]))
        statusDesc.grid(row=9,column=1)
        self.status.grid(row=9,column=2)
        
        notesDesc = tk.Label(self.window, text="Notes:")
        self.notes = tk.Entry(self.window,width=40)
        self.notes.insert(0,str(self.data[10]))
        notesDesc.grid(row=10,column=1)
        self.notes.grid(row=10,column=2)
        
        tagsDesc = tk.Label(self.window, text="Tags:")
        self.tags = tk.Entry(self.window,width=40)
        self.tags.insert(0,str(self.data[11]))
        tagsDesc.grid(row=11,column=1)
        self.tags.grid(row=11,column=2)
        
        updateButt=tk.Button(self.window)
        updateButt["text"]="Update"
        updateButt["command"]=self.update
        updateButt.grid(row=12,column=1)
        
        cancelButt=tk.Button(self.window)
        cancelButt["text"]="Back"
        cancelButt["command"]=self.quit
        cancelButt.grid(row=12,column=2)
        
    def update(self):
        data=(self.idBook,self.title.get(),self.author.get(),self.year.get(),
              self.publish.get(),self.isbn.get(),self.typeEn.get(),
              self.genre.get(),self.language.get(),
              self.status.get(),self.notes.get(), self.tags.get())
        updateBook(con,data)
        self.window.destroy()
        infoWindow(con,self.idBook)
    def quit(self):
        self.window.destroy()
        
class searchWindow:
    def __init__(self,con):
        self.window=tk.Tk()
        self.window.title("Search for the book")
        self.createControls()
        self.window.mainloop()
        
    def createControls(self):
        argNames=('title', 'author', 'year', 'publisher', 'isbn', 'type', 'genre',
              'language', 'status', 'notes', 'tags')
        
        tk.Label(self.window).grid(columnspan=4,row=0)
        
        self.entryText=tk.Entry(self.window, width=50)
        self.entryText.grid(columnspan=4,row=1)
        
        self.searchLabel=tk.Label(self.window, text="Search by:")
        self.searchLabel.grid(row=2,column=1)
        
        self.combobox = ttk.Combobox(self.window, values=argNames)
        self.combobox.grid(row=2,column=2)
        
        self.searchButt=tk.Button(self.window, text="Search")
        self.searchButt.grid(row=2,column=3)
        self.searchButt["command"]=self.search
    
    def search(self):
        listOfBooks=searchBook(con,self.combobox.get(),self.entryText.get())
        self.window.destroy()
        printListWindow(listOfBooks)

#Functions

def addBook(con,data):
    cursor=con.cursor()
    cursor.execute("""INSERT INTO books(title, author, year, publisher, isbn, type, 
        genre, language, status, notes, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",data)
    con.commit()   
    return 1

def updateBook(con,data):
    argNames=('title', 'author', 'year', 'publisher', 'isbn', 'type', 'genre',
              'language', 'status', 'notes', 'tags')
    for i,val in enumerate(data[1:]):
        con.execute("UPDATE books SET "+argNames[i]+"='"+val+"' WHERE id="+str(data[0]))
    con.commit()
    return 1

def getAllBooks(con):
    cursor=con.execute("SELECT id, title, author FROM books ORDER BY title")
    rows=cursor.fetchall()
    bookList=[]
    for row in rows:
        bookList.append((row[0],row[1],row[2]))
    return bookList   

def searchBook(con,searchArg,searchVal):
    cursor=con.execute("SELECT id, title, author FROM books WHERE "+str(searchArg)+
                " LIKE '%"+str(searchVal)+"%' ORDER BY title")
    rows=cursor.fetchall()
    bookList=[]
    for row in rows:
        bookList.append((row[0],row[1],row[2]))
    return bookList

def removeBook(con,idBook):
    if not idBook==0:
        con.execute("DELETE FROM books WHERE id=?", idBook)
        con.commit()
        print ("Book " + str(idBook) +" was removed!")
    return 1

#Main program

print("LibrosDatas\nby Jacek Piłka\n")

print("Checking if data base exists...")
    
if not path.exists('books.db'):
    query="""CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT, author TEXT, year INTEGER, publisher TEXT, isbn TEXT, type TEXT, 
    genre TEXT, language TEXT, status TEXT, notes TEXT, tags TEXT);"""
    con=sqlite3.connect('books.db')
    con.execute(query)
    con.commit()
    print("Data base created!\n")
else:
    con=sqlite3.connect('books.db')
    print("Data base finded!\n")

mainWindow=MainWindow(con)

print("Libros Datas has been stoped!")