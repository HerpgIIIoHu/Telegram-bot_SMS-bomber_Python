import sqlite3
import datetime
class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_id`, `money` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO `users` (`user_id`) VALUES (?)', (user_id,))
    
    def add_data_zapuska(self, date, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `zapusk` = ? WHERE `user_id` = ?", (date, user_id,))
    
    def data_user_zapusk(self, user_id):
        with self.connection:
            try:
                result = self.cursor.execute("SELECT `zapusk` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
                return result[0][0]
            except Exception as d:
                b =0
                print(d)
   
    
    def user_money(self, user_id):
        with self.connection:
            try:
                result = self.cursor.execute("SELECT `money` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
                return result[0][0]
            except Exception as d:
                b =0
                print(d)
    
    def set_money(self, user_id, money):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `money` = ? WHERE `user_id` = ?", (money, user_id,))
        
    def add_check(self, user_id, money, bill_id, date, date_check):
        with self.connection:
            self.cursor.execute('INSERT INTO `check` (`user_id`, `money`, `bill_id`, `date`, `date_check`) VALUES (?, ?, ?, ?, ?)', (user_id, money, bill_id, date, date_check,))
    
    def add_checks(self, user_id, money, date, date_check):
        with self.connection:
            self.cursor.execute('INSERT INTO `checks` (`user_id`, `money`, `date`, `date_check`) VALUES (?, ?, ?, ?)', (user_id, money, date, date_check,))
        
    def set_date(self, user_id, date_check):
        with self.connection:
            return self.cursor.execute("UPDATE `check` SET `date_check` = ? WHERE `user_id` = ?", (date_check , user_id,))
            
    def get_check(self, bill_id):
        with self.connection:
            try:
                result = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)
                if not bool(len(result)):
                    return False
                return result[0]
            except Exception as d:
                b =0
                print(d)
    
    def del_check(self, date):
        now = datetime.datetime.now()#Текущая дата
        nows = ("{}.{}.{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute))
        date_for_db = ("{}.{}.{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute+10))
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `check` WHERE `date_check` = "Не оплачен"', (date,))