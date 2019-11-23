# -*- coding: utf-8 -*-
"""
Obsługa bazy danych książek

by Jacek Piłka
"""

import pandas as pd
import sqlite3
import sqlalchemy as sqla
from os import path, system

#Functions

def addBook(con):
    system("cls")
    print("Add a book")
    title=input("Title: ")
    author=input("Author: ")
    year=input("Year: ")
    publisher=input("Publisher: ")
    isbn=input("ISBN: ")
    typeBook=input("Type: ")
    genre=input("Genre: ")
    language=input("Language: ")
    status=input("Status: ")
    notes=input("Additional notes: ")
    
    data=(title,author,year,publisher,isbn,typeBook,genre,language,status,notes)
    cursor=con.cursor()
    cursor.execute("""INSERT INTO books(title, author, year, publisher, isbn, type, 
        genre, language, status, notes) VALUES (?,?,?,?,?,?,?,?,?,?)""",data)
    bookID=cursor.lastrowid
    con.execute("CREATE TABLE "+ "tags_"+str(bookID)+"(id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT)")
    con.commit()   
    return 1

def removeBook(con):
    remID=input("ID of the book for removing (0 will cancel this operation): ")
    if not remID==0:
        con.execute("DELETE FROM books WHERE id=?", remID)
        con.execute("DROP TABLE tags_"+str(remID))
        con.commit()
        print ("Book " + str(remID) +" was removed!")
    return 1

def readAll(db):
    system("cls")
    print(pd.read_sql("SELECT id, title, author FROM books ORDER BY title",db))
    option=input("Look at specific book [t/n]?: ")
    if option=='t':
        bookID=input("Book's ID: ")
        bookInfo(con,bookID)
    return 1

def bookInfo(con, bookID):  
    try:
        while True:
            cursor=con.execute("SELECT * FROM books WHERE id=?",bookID)
            rows=cursor.fetchall()
            row=rows[0]
            for i,desc in enumerate(cursor.description):
                print(desc[0]+": ",row[i])
            
            print("tags: ", end = '')
            cursor=con.execute("SELECT * FROM tags_"+str(bookID))
            rows=cursor.fetchall()
            for x in rows:
                print(x[1]+", ", end = '')
            print(" ")
            
            option=input("[A]dd a tag, [R]emove a tag, [E]dit book's info or exit [any key]: ")
            if option=='a':
                nTag=input("New tag: ")
                con.execute("INSERT INTO tags_"+str(bookID)+"(tag) VALUES ('"+nTag+"')")
                con.commit()
            elif option=='r':
                nTag=input("Remove tag: ")
                con.execute("DELETE FROM tags_"+str(bookID)+" WHERE tag='"+nTag+"'")
                con.commit()
            elif option=='e':
                bookChange(con,bookID)
            else:
                break
    except IndexError:
        print("There's no book with such ID!")
        return 0
    return 1

def bookChange(con, bookID):
    option=input("""Change: [T]itle, [A]uthor, [Y]ear, [P]ublisher, [I]SBN, [T]ype, 
          [G]enre, [L]anguage, [S]tatus, [N]otes: """)
    if option=='t':
        nVal=input("New title: ")
        con.execute("UPDATE books SET title='"+nVal+"' WHERE id="+str(bookID))
    elif option=='a':
        nVal=input("New author: ")
        con.execute("UPDATE books SET author='"+nVal+"' WHERE id="+str(bookID))
    elif option=='y':
        nVal=input("New year: ")
        con.execute("UPDATE books SET year='"+str(nVal)+"' WHERE id="+str(bookID))
    elif option=='p':
        nVal=input("New publisher: ")
        con.execute("UPDATE books SET publisher='"+nVal+"' WHERE id="+str(bookID))
    elif option=='i':
        nVal=input("New ISBN: ")
        con.execute("UPDATE books SET isbn='"+nVal+"' WHERE id="+str(bookID))
    elif option=='t':
        nVal=input("New type: ")
        con.execute("UPDATE books SET type='"+nVal+"' WHERE id="+str(bookID))
    elif option=='g':
        nVal=input("New genre: ")
        con.execute("UPDATE books SET genre='"+nVal+"' WHERE id="+str(bookID))
    elif option=='l':
        nVal=input("New language: ")
        con.execute("UPDATE books SET language='"+nVal+"' WHERE id="+str(bookID))
    elif option=='s':
        nVal=input("New status: ")
        con.execute("UPDATE books SET status='"+nVal+"' WHERE id="+str(bookID))
    elif option=='n':
        nVal=input("New notes: ")
        con.execute("UPDATE books SET notes='"+nVal+"' WHERE id="+str(bookID))
    else:
        print("Wrong option!")
        return 0
    con.commit()
    return 1

def search(con,db):
    option=input("""Search by [T]itle, [A]uthor, [Y]ear, [P]ublisher, [I]SBN,
                 [T]ype, [G]enre, [L]anguage, [S]tatus, tags [E]: """)
    if option=='t':
        nVal=input("Put the title: ")
        sVal="title"
    elif option=='a':
        nVal=input("Put the author: ")
        sVal="author"
    elif option=='y':
        nVal=input("Put the year: ")
        sVal="year"
    elif option=='p':
        nVal=input("Put the publisher: ")
        sVal="publisher"
    elif option=='i':
        nVal=input("Put the ISBN: ")
        sVal="isbn"
    elif option=='t':
        nVal=input("Put a type: ")
        sVal="type"
    elif option=='g':
        nVal=input("Put a genre: ")
        sVal="genre"
    elif option=='l':
        nVal=input("Put a language: ")
        sVal="language"
    elif option=='s':
        nVal=input("Put a status: ")
        sVal="status"
    elif option=='e':
        nVal=input("Put a tag: ")
        searchTag(con,db,nVal)
        return 1
    else:
        print("Wrong option!")
        return 0
    
    system("cls")
    print(pd.read_sql("""SELECT id, title, author FROM books WHERE 
                   """+sVal+"='"+nVal+"' ORDER BY title",db))
    option=input("Look at specific book [t/n]?: ")
    if option=='t':
        bookID=input("Book's ID: ")
        bookInfo(con,bookID)
    return 1

def searchTag(con,db,tag):
    #Iteruj po każdej książce i po każdej tablicy tagów
    cursor=con.execute("SELECT id FROM books")
    rows=cursor.fetchall()
    idList=[]
    for row in rows:
        cursor1=con.execute("SELECT id FROM tags_"+str(row[0])+" WHERE tag='"+tag+"'")
        if cursor1.fetchall(): #Jeżeli jest tag -> dopisz id do listy
            idList.extend(str(row[0]))
    if idList:
        query="SELECT id, title, author FROM books WHERE "
        for i,ii in enumerate(idList):
            if not i:
                query+="id="+str(ii)+" "
            else:
                query+="OR id="+str(ii)+" "
        system("cls")
        print("Books with tag: ")
        print(pd.read_sql(query+"ORDER BY title",db))
        option=input("Look at specific book [t/n]?: ")
        if option=='t':
            bookID=input("Book's ID: ")
            bookInfo(con,bookID)
    else:
        print("There'are no books with a such tag!")
    return 1

#Main program

print("LibrosDatas\nby Jacek Piłka\n")

print("Checking if data base exists...")
    
if not path.exists('books.db'):
    query="""CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT, author TEXT, year INTEGER, publisher TEXT, isbn TEXT, type TEXT, 
    genre TEXT, language TEXT, status TEXT, notes TEXT);"""
    con=sqlite3.connect('books.db')
    con.execute(query)
    con.commit()
    print("Data base created!\n")
else:
    con=sqlite3.connect('books.db')
    print("Data base finded!\n")
    
db=sqla.create_engine("sqlite:///books.db")
pd.set_option('expand_frame_repr', False)

while True:
    system("cls")
    print("\nLibrosDatas\nby Jacek Piłka\n")
    print("Main menu:")
    print("A - Add a book")
    print("R - Remove a book")
    print("P - Print the book's info")
    print("W - Print all books")
    print("S - Search for the book")
    print("X - Exit")
    
    optionButt=input("Choose option: ")
    if optionButt=="a":
        addBook(con)
    elif optionButt=="r":
        removeBook(con)
    elif optionButt=="p":
        bookID=input("Book's ID: ")
        system("cls")
        bookInfo(con,bookID)
    elif optionButt=="w":
        readAll(con)
    elif optionButt=="s":
        search(con,db)
    elif optionButt=="x":
        print("Ending this program")
        con.close()
        break
    else:
        print("Wrong option!")