import sqlite3
from vk_metods import *
import logging
 
class DB:
    def __init__(self):
        conn = sqlite3.connect('base.db', check_same_thread=False)
        self.conn = conn
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()

class UserModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id INTEGER, 
                             user_name VARCHAR(16),
                             dialog INTEGER,
                             wiki INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_id, user_name, dialog):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_id, user_name, dialog, wiki) 
                          VALUES (?,?,?,?)''', 
                          (user_id, user_name, dialog, 0))
        logging.info(f'Новый пользователь {user_name}(id={user_id})')
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()
        if row is None:
            info = user_information(user_id)
            self.insert(user_id, info['first_name'], 0)
            row = self.get(user_id)
        return(row)
    
    def new_dialog(self, id_1, id_2):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET dialog = ? WHERE user_id = ?''',(id_2,id_1))
        cursor.execute('''UPDATE users SET dialog = ? WHERE user_id = ?''',(id_1,id_2))
        cursor.close()
        self.connection.commit()

    def stop_dialog(self, id_1, id_2):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET dialog = ? WHERE user_id = ?''',(0,id_1))
        cursor.execute('''UPDATE users SET dialog = ? WHERE user_id = ?''',(0,id_2))
        cursor.close()
        self.connection.commit()

    def wiki(self, user_id, logic):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET wiki = ? WHERE user_id = ?''',(logic,user_id))
        cursor.close()
        self.connection.commit()
 
    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        self.get(user_id)
        cursor.execute('''DELETE FROM users WHERE id = ?''',
                         (str(user_id),))
        cursor.close()
        self.connection.commit()    

    #не работает
    def free_people(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE dialog = ?", (0,))
        row = cursor.fetchone()
        print(row)
        print(len(row))
        if row is None:
            return 'все заняты'
        else:
            return row