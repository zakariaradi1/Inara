import mysql.connector as my
from Models import *

class DataBase:
    cnx = None

    @staticmethod
    def get_connection():
        if DataBase.cnx is None:
            try:
                DataBase.cnx = my.connect(
                    user="root",
                    password="zakaria1234radi@",
                    host="localhost",
                    database="db_Books"
                )
                print('Connection OK')
            except Exception as e:
                print(f'Connection Error: {e}')
                return None
        return DataBase.cnx



class UserManage:
    def __init__(self):
        self.cnx = DataBase.get_connection()

    def create_account(self, account: Account) -> bool:
        if account.Email is None or account.Nom is None or account.password is None:
            raise ValueError("Fields cannot be null or empty.")
    
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            query = "INSERT INTO T_Accounts(Email, Nom, password) VALUES(%s, %s, %s);"
            cursor.execute(query, (account.Email, account.Nom, account.password))
            self.cnx.commit()
            cursor.close()
            return True
        return False

       
        
    def auth(self, email: str, password: str) -> Account | None:
        query = "SELECT * FROM T_Accounts WHERE Email = %s AND password = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (email, password))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return Account(**row)  # type: ignore 
            return None
        return None

        
    def get_account(self, email: str) -> Account | None:
        query = "SELECT * FROM T_Accounts WHERE Email = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return Account(**row)  # type: ignore 
        return None

        
        
    def rest_password(self,email:str,password:str)->bool:
        query:str = "UPDATE T_Accounts SET password=%s WHERE Email=%s ;"
        if self.cnx != None:
            cursor = self.cnx.cursor()
            cursor.execute(query,(password,email))
            self.cnx.commit()
            return True
        return False
    
    
    def change_email(self,old_email, new_email)->bool:
            query = "UPDATE T_Accounts SET email = %s WHERE email = %s"
            if self.cnx != None:
                cursor = self.cnx.cursor()
                cursor.execute(query, (new_email, old_email))
                self.cnx.commit()
                cursor.close()
                return True
            return False
    
    
    def read_book(self, book_title: str):
        query: str = "SELECT book_link FROM T_Books WHERE book_title = %s;"
        if self.cnx != None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (book_title,))
            book = cursor.fetchone()
            cursor.close()
            if book != None:
                return book  # type: ignore
            return None
        return None


    def describe_book(self, book_title: str):
        query: str = "SELECT * FROM T_Books WHERE book_title = %s;"
        if self.cnx != None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (book_title,))
            book = cursor.fetchone()
            cursor.close()
            if book != None:
                return book
            return None
        return None
    
    
    def rate(self,book_id:int,rating:float):
        query:str = "INSERT INTO ratings(book_id,rating) VALUES(%s,%s);"
        if self.cnx != None:
            cursor = self.cnx.cursor()
            cursor.execute(query,(book_id,rating))
            self.cnx.commit()
            return True
        return False
    
    def update_book_ratings(self):
        query = """
                UPDATE T_Books b
                JOIN (
                    SELECT book_id, AVG(rating) AS average_rating
                    FROM ratings
                    GROUP BY book_id
                    ) r ON b.book_id = r.book_id
                    SET b.book_rating = r.average_rating;
                """
        if self.cnx != None:
            cursor = self.cnx.cursor()
            cursor.execute(query)
            self.cnx.commit()
            cursor.close()
            return True
        return False

     
    def user_info(self,email:str):
        query: str = "SELECT * FROM T_Accounts WHERE Email = %s;"
        if self.cnx != None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (email,))
            account = cursor.fetchone()
            cursor.close()
            if account != None:
                return account
            return None
        return None
        

    def chercher(self,title:str):
        query: str = "SELECT * FROM T_Books WHERE book_title LIKE %s;"
        if self.cnx != None:
            wildcard_title = f"%{title}%"
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (wildcard_title,))
            book = cursor.fetchall()
            cursor.close()
            if book != None:
                return book
            return None
        return None
        

    def get_messages(self, email):
        if self.cnx != None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM mail WHERE recipient = %s", (email,))
            messages = cursor.fetchall()
            cursor.close()
            return messages
        return []

    def send_message(self, sender, recipient, subject, content):
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            query = """
                INSERT INTO mail (sender, recipient, subject, content, is_read)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (sender, recipient, subject, content, False))
            self.cnx.commit()

            # Fetch the newly created message
            cursor.execute("SELECT * FROM mail WHERE id = LAST_INSERT_ID()")
            new_message = cursor.fetchone()
            cursor.close()

            return new_message
        return None


    def mark_message_as_read(self, message_id):
        if self.cnx != None:
            cursor = self.cnx.cursor()
            cursor.execute("UPDATE mail SET is_read = TRUE WHERE id = %s", (message_id,))
            self.cnx.commit()
            cursor.close()
            return True
        return False

    def delete_message(self, message_id, email):
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(
                "DELETE FROM mail WHERE id = %s AND recipient = %s", (message_id, email)
            )
            self.cnx.commit()
            cursor.execute("ALTER TABLE mail AUTO_INCREMENT = 1")
            self.cnx.commit()
            cursor.close()
            return True
        return False


    def get_unread_messages_count(self, email: str) -> int:
        query = "SELECT COUNT(*) FROM mail WHERE recipient = %s AND is_read = 0;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()  # result will be a tuple like (count,)
            cursor.close()
            if result:
                if result and isinstance(result, tuple) and isinstance(result[0], (int, str)):
                    return int(result[0])
                return 0
            else:
                return 0
        return 0





