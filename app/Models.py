from dataclasses import dataclass
from datetime import datetime
@dataclass
class Account:
    Email:str
    Nom:str
    password:str
    id_user:int


@dataclass
class Book:
    book_id:int         
    book_title:str  
    book_author:str   
    book_description:str 
    book_creation:datetime
    book_link:str
    book_categorie:str   
    book_rating:int
