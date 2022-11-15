from tkinter import *
from tkinter import ttk,Canvas
from PIL import Image,ImageTk
import mysql.connector


d1=mysql.connector.connect(
    host='localhost', user='root', password='fortnitedire') 

#connecting to dashboard
if d1.is_connected:
    print('Connected')

curs=d1.cursor()

# fetch all data from table
curs.execute('select * from resman.food;')
res=curs.fetchall()

columns=('id','name','veg','price')

# define main window
win=Tk()
win.title('Restaurant Management System')
win.geometry('800x600')
win.resizable(0,0)
win.configure(bg='#d6c2a1')

# define frame
frame=Frame(win,bg='#d6c2a1')


# variables
yn=1
price_list=[]
items_count=30
price_count=0


# define tree - host for table
tree=ttk.Treeview(frame,columns=columns,show='headings',height=20)
ttk.Style().configure('Treeview',background='#bdab8e',fieldbackground='#bdab8e')
tree.heading('id',text='Food ID')
tree.heading('name',text='Name')
tree.heading('veg',text='Veg')
tree.heading('price',text='Price')


# filter for price
def search_price():
    curs=d1.cursor()
    query_filter_1 = price_low.get()
    query_filter_2 = price_high.get()
    if yn%3==1:
        sql_query=f'select * from resman.food where price between {query_filter_1} and {query_filter_2}' 
    if yn%3==2:
        sql_query=f'select * from resman.food where price between {query_filter_1} and {query_filter_2} and veg="V"' 
    elif yn%3==0:
        sql_query=f'select * from resman.food where price between {query_filter_1} and {query_filter_2} and veg="N"' 
    curs.execute(sql_query)
    res=curs.fetchall()

    for i in tree.get_children():
        tree.delete(i)
    win.update() 

    for row in res:
        tree.insert('',END,values=row)

# search function to search for name of items
def search_name():
    curs=d1.cursor()
    query_filter = "'%"+name_search.get().upper()+"%'"
    if yn%3==1:
        sql_query=f'select * from resman.food where name like {query_filter}'
    elif yn%3==2:
        sql_query=f'select * from resman.food where name like {query_filter} and veg="V"'
    elif yn%3==0:
        sql_query=f'select * from resman.food where name like {query_filter} and veg="N"'
    curs.execute(sql_query)
    res=curs.fetchall()

    for i in tree.get_children():
        tree.delete(i)
    win.update() 
    for row in res:
        tree.insert('',END,values=row)

# function to filter between veg and non-veg
def yn_fun():
    global yn
    yn+=1
    curs=d1.cursor()
    # check for mod of 3 for 3 states of button: all items, veg items and non-veg items
    if yn%3==1:
        yn_button.config(highlightbackground='white')
        sql_query=f"select * from resman.food"

    elif yn%3==2:
        yn_button.config(highlightbackground='green')
        sql_query=f" select * from resman.food where veg='V'"

    elif yn%3==0:
        yn_button.config(highlightbackground='red')
        sql_query=f"select * from resman.food where veg='N'"

    curs.execute(sql_query)
    res=curs.fetchall()

    for i in tree.get_children():
        tree.delete(i)
    win.update() 
    for row in res:
        tree.insert('',END,values=row)

# function to calculate price of total of items selected
def price():
    global price_count
    n=price_entry.get()
    if n=='' or int(n)>items_count:
        price_entry_button.config(highlightbackground='red')
    else:
        price_list.append(n)
        price_entry_button.config(highlightbackground='white')
        curs.execute(f'select price from resman.food where id like {n}')
        res=curs.fetchall()
        #fetch price from table in form of int from list
        price=int(str(res[0])[2:5])
        price_count+=price
        price_count_button.config(text=u"\u20B9"+str(price_count))
        items_selected.config(text=price_list)

# function to clear all items selected for pricing 
def clear():
    global price_count,price_list
    price_list.clear()
    price_count=0
    price_count_button.config(text=u"\u20B9"+'0')
    items_selected.config(text='Items')


# define images and specifications
momo_canvas=Canvas(win,bg='#bdab8e',width=120,height=120)
momo_canvas.place(relx=0.08,rely=0.79)
momo_img=Image.open('assets/momo.png')
momo_img.thumbnail((125,125))
momo_img=ImageTk.PhotoImage(momo_img)
momo_canvas.create_image(60,60,image=momo_img)

chinese_man_canvas=Canvas(win,bg='#bdab8e',width=120,height=120)
chinese_man_canvas.place(relx=0.8,rely=0.79)
chinese_man_img=Image.open('assets/chinese man.png')
chinese_man_img.thumbnail((125,125))
chinese_man_img=ImageTk.PhotoImage(chinese_man_img)
chinese_man_canvas.create_image(60,67,image=chinese_man_img)

# define widgets
hellfire_button=Label(frame,width=15,height=1,font=('Verdana',18),text='Fu King Chinese',fg='Black',bg='#d6c2a1')
dummy_label_1=Label(frame,width=1,height=1,bg='#d6c2a1')
dummy_label_2=Label(frame,width=1,height=1,bg='#d6c2a1')
price_count_button=Label(win,text=u"\u20B9"+'0',width=5,height=1)
momo_img_label=Label(win,image=momo_img)
chinese_man_img_label=Label(win,image=chinese_man_img)
items_selected=Label(win,text='Items',width=10)

name_search=Entry(frame,width=18,font=('Verdana',12), bg='#969b9e')
price_low=Entry(frame,width=5,font=('Verdana',12),bg='#969b9e',fg='black',foreground='#969b9e')
price_high=Entry(frame,width=5,font=('Verdana',12),bg='#969b9e',fg='black')
price_entry=Entry(win,width=5,font=('Verdana',12),bg='#969b9e')

name_button=Button(frame,text='Search',width=15,command=search_name,bg='#595555')
price_button=Button(frame,text='Search',width=15,command=search_price,bg='cyan')
yn_button=Button(frame,text='V/N',width=5,command=yn_fun)
price_entry_button=Button(win,text='Add',width=5,command=price)
clear_button=Button(win,text='Clear',width=5,command=clear)

# define scrollbar to view whole table with limited space
scb=Scrollbar(frame,orient=HORIZONTAL)

#insert all rows into tree
for row in res:
    tree.insert('',END,values=row )

# place all widgets
hellfire_button.pack()
name_search.place(relx=0.4,rely=0.082)
price_low.place(relx=0.83,rely=0.082)
price_high.place(relx=0.9,rely=0.082)
yn_button.place(relx=0.65,rely=0.12)
dummy_label_1.pack()
dummy_label_2.pack()
name_button.pack()
price_button.place(relx=0.82,rely=0.15)
price_entry.place(relx=0.5,rely=0.9)
price_entry_button.place(relx=0.6,rely=0.91)
price_count_button.place(relx=0.4,rely=0.91)
clear_button.place(relx=0.7,rely=0.91)
items_selected.place(relx=0.25,rely=0.91)

frame.pack()
tree.pack(side=TOP)


win.mainloop()