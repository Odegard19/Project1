import tkinter as tk        # Импорт библиотеки tkinter
from tkinter import ttk     # Импорт ttk
import sqlite3              # Импорт библиотеки sqlite3


                            
class Main(tk.Frame):                                       # Создаем класс
    def __init__(self, root):                               # Передаём все методы, функции, свойства класса tk                    
        super().__init__(root)                              
        self.init_main()                                    
        self.db = db                                        
        self.view_records()                                 

    def init_main(self):                                    # Создаем метод со всеми графическими элементами (поля, кнопки)

        
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)              # Установили цвет фона рамки и ширину рамки
        toolbar.pack(side=tk.TOP, fill=tk.X)                # Размещаем в окне


        self.add_img = tk.PhotoImage(file="./img/add.png")  # Загрузили изображение, кнопки, добавление в переменнную
        
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)                  # Размещение кнопки в окне

        self.tree = ttk.Treeview(                           # Создаём таблицу с колонками: "ID", "name", "tel", "email". 
            self, columns=("ID", "name", "tel", "email","salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)          
        self.tree.column("name", width=300, anchor=tk.CENTER)       
        self.tree.column("tel", width=150, anchor=tk.CENTER)        
        self.tree.column("email", width=150, anchor=tk.CENTER)      
        self.tree.column("salary", width=90, anchor=tk.CENTER)     

        self.tree.heading("ID", text="ID")                          
        self.tree.heading("name", text="ФИО")                       
        self.tree.heading("tel", text="Телефон")                    
        self.tree.heading("email", text="E-mail")                   
        self.tree.heading("salary", text="Зарплата")                   

        self.tree.pack(side=tk.LEFT)                                # Размещение таблицы в окне


        self.update_img = tk.PhotoImage(file="./img/update.png")    # Загрузили изображение кнопки обновления в переменнную
        
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)                          # Размещение кнопки в окне


        self.delete_img = tk.PhotoImage(file="./img/delete.png")    # Загрузили изображение кнопки обновления в переменнную
        
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)                               # Размещение кнопки в окне


        self.search_img = tk.PhotoImage(file="./img/search.png")    # Загрузили изображение кнопки обновления в переменнную
        
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)                                                   # Размещение кнопку в окне

    def open_dialog(self):                                                              
        Child()                                                                         
    def records(self, name, tel, email,salary ):
        self.db.insert_data(name, tel, email,salary )                                   
        self.view_records()                                                             

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM Employees")                               # Запрос: Выбираем все данные из таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]                         # Старые данные удаляем
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  # Вписываем новые данные в бд

    def open_update_dialog(self):
        Update()                                                                        

    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(                                                         # Запрос на обновление
            """UPDATE Employees SET name=?, tel=?, email=?, salary=? WHERE id=?""",

            (name, tel, email,salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()                                                           # Сохраняем запрос
        self.view_records()                                                             

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(                                                     
                "DELETE FROM Employees WHERE id=?", (self.tree.set(selection_items, "#1"))     
            )
        self.db.conn.commit()                                                           # Сохраняем запрос
        self.view_records()                                                             

    def open_search_dialog(self):
        Search()                                                                        

    def search_records(self, name):
        name = "%" + name + "%"                                                         
        self.db.cursor.execute("SELECT * FROM Employees WHERE name LIKE ?", (name,))           

        [self.tree.delete(i) for i in self.tree.get_children()]                         # Старые данные удаляем
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  # Вписываем новые данные в бд


class Child(tk.Toplevel):                                   
    def __init__(self):                                     
        super().__init__(root)                              
        self.init_child()                                   
        self.view = app

    def init_child(self):
        self.title("Добавить сотрудника")                   # Указали название заголовка
        self.geometry("400x220")                            
        self.resizable(False, False)                        # Установили ограничения изменения размеров окна

        self.grab_set()                                     
        self.focus_set()                                    

        label_name = tk.Label(self, text="ФИО:")            # Создание формы для ФИО
        label_name.place(x=50, y=50)                        
        label_select = tk.Label(self, text="Телефон:")      # Создание формы для Телефона
        label_select.place(x=50, y=80)                      
        label_sum = tk.Label(self, text="E-mail:")          # Создание формы для E-mail
        label_sum.place(x=50, y=110)                        

        label_salary = tk.Label(self, text="Зарплата:")     #Создание формы для Заплата
        label_salary.place(x=50, y=140)                        

        self.entry_name = ttk.Entry(self)                   # Создали поле для ввода формы ФИО
        self.entry_name.place(x=200, y=50)                  
        self.entry_email = ttk.Entry(self)                  # Создали поле для ввода формы  E-mail
        self.entry_email.place(x=200, y=80)                 
        self.entry_tel = ttk.Entry(self)                    # Создали поле для ввода формы Телефон
        self.entry_tel.place(x=200, y=110)                  

        self.entry_salary = ttk.Entry(self)                 # Создали поле для ввода формы Зарплата
        self.entry_salary.place(x=200, y=140)                  

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # Создали кнопку для добавления текста 
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )


class Update(Child):
    def __init__(self):                                             # Создаем класс
        super().__init__()                                          # Передаём все методы, все функции, все свойства класса tk
        self.init_edit()                                            
        self.view = app                                             
        self.db = db                                                
        self.default_data()                                         

    def init_edit(self):                                             # Метод редактирования данных в бд
        self.title("Редактирование данных сотрудника")               # Указали название заголовка
        btn_edit = ttk.Button(self, text="Редактировать")            # Создали кнопку и укзали текст на ней
        btn_edit.place(x=205, y=170)                                 
        
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

        
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.destroy(), add="+"
        )

        self.btn_ok.destroy()                                               

    def default_data(self):
        self.db.cursor.execute(                                             
            "SELECT * FROM Employees WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),        
        )
        row = self.db.cursor.fetchone()                         
        self.entry_name.insert(0, row[1])                       
        self.entry_email.insert(0, row[2])                      
        self.entry_tel.insert(0, row[3])                        
        self.entry_salary.insert(0,row[4])



class Search(tk.Toplevel):
    def __init__(self):                                         # Создаем класс
        super().__init__()                                      # Передаём все методы, все функции, все свойства класса tk
        self.init_search()                                      
        self.view = app                                         

    def init_search(self):
        self.title("Поиск сотрудника")                          # Указали название заголовка
        self.geometry("300x100")                                # Установили размер 
        self.resizable(False, False)                            # Установили ограничения изменеия размеров окна

        label_search = tk.Label(self, text="Имя:")              # Создание формы для поиска ФИО
        label_search.place(x=50, y=20)                          
        self.entry_search = ttk.Entry(self)                     # Создали поле для ввода формы поиска по  ФИО
        self.entry_search.place(x=100, y=20, width=150)         

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)  # Создали кнопку, указали текст на ней и функцию, которая вызовется по нажатию на ней
        btn_cancel.place(x=185, y=50)

        search_btn = ttk.Button(self, text="Найти")              # Создали кнопку, указали текст на ней
        search_btn.place(x=105, y=50)

        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")



class DB:
    def __init__(self):                                                                 # Создаем класс
        self.conn = sqlite3.connect("contacts.db")                                      # Создание соединения с базой данных(имя бд)
        self.cursor = self.conn.cursor()                                                # Вызываем курсор бд
        self.cursor.execute(                                                            # Запрос на создание бд
            '''
            CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL,
            salary INTEGER
            )
            '''
        )
        self.conn.commit()                                                               # Сохраниям изменения                    
        self.data()

    
    def data(self):                                                                      # Создаем метод для добавления данных в бд
        insert_into = 'INSERT INTO Employees (name, tel, email, salary) VALUES (?, ?, ?, ?)'


        user_data = ('Jakob Kristensen', '+91 (294) 711-91-10', 'jakob@gmail.com', '59000')
        user_data1 = ('Martin Odegaard', '+62 (940) 291-23-82', 'martin@hotmail.com', '75000')
        user_data2 = ('Elias Nielsen', '+41 (415) 872-05-99', 'elias@yahoo.com', '45000')
        user_data3 = ('Lucas Iversen', '+354 (219) 853-46-17', 'lucas@gmail.com', '89000')
        user_data4 = ('Johansen Strand', '+47 (542) 454-73-77', 'johansen@hotmail.com', '95000')
        self.cursor.execute(insert_into,user_data )
        self.cursor.execute(insert_into,user_data1 )
        self.cursor.execute(insert_into,user_data2 )
        self.cursor.execute(insert_into,user_data3 )
        self.cursor.execute(insert_into,user_data4 )

        self.conn.commit()                                                                                          # Сохраняем изменения


    def insert_data(self, name, tel, email, salary):                                                                # Метод для добавления данных в таблицу
        self.cursor.execute(                                                                                        # Запрос на создание бд
            """INSERT INTO Employees(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)    
        )
        self.conn.commit()                                                                                          # Сохраняем изменения

if __name__ == "__main__":
    root = tk.Tk()                                  # Создали Tk
    db = DB()                                       
    app = Main(root)                                
    app.pack()                                      
    root.title("Список сотрудников компании")       # Установили заголовок Tk
    root.geometry("765x450")                        # Установили размер Tk
    root.resizable(False, False)                    # Установили ограничения изменения размеров окна
    root.mainloop()                                 