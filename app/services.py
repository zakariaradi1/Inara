from dal import *



class UserManager:
    def __init__(self) -> None:
        self.userDao = UserManager()
        
    def create_account(self, account: Account) -> bool:
        return self.userDao.create_account(account)
    
    def auth(self, email: str, password: str) -> Account | None:
        return self.userDao.auth(email,password)
    
    def get_account(self, email: str) -> Account | None:
        return self.userDao.get_account(email)
    
    def rest_password(self, email: str, password: str) -> bool:
        return self.userDao.rest_password(email,password)
    
    def select_categories(self, book_categorie: str) -> bool:
        return self.userDao.select_categories(book_categorie)

    def read_book(self, book_title: str):
        return self.userDao.read_book(book_title)
    
    def describe_book(self, book_title: str):
        return self.userDao.describe_book(book_title)
    
    def rate(self, book_title: str, book_rating: int):
        return self.userDao.rate(book_title, book_rating)
    
    def update_book_ratings(self):
        return self.userDao.update_book_ratings()
    
    def user_info(self,email:str):
        return self.userDao.user_info(email)
    
    def change_email(self, old_email, new_email):
        return self.userDao.change_email(old_email, new_email)
    
    def chercher(self,title:str):
        return self.userDao.chercher(title)
    
    def get_messages(self, email):
        return self.userDao.get_messages(email)
    
    def send_message(self, sender, recipient, subject, content):
        return self.userDao.send_message(sender, recipient, subject, content)
    
    def mark_message_as_read(self, message_id):
        return self.userDao.mark_message_as_read(message_id)
    
    def delete_message(self, message_id, email):
        return self.userDao.delete_message(message_id, email)
    
    def get_unread_messages_count(self, email: str) -> int:
        return self.userDao.get_unread_messages_count(email)
