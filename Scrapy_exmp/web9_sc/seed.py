import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from customs.custom_logger import my_logger
from customs.custom_timer import sync_time, async_time

from conn_modd.models import Author, Quote
import conn_modd.connect

import json

def data_from_file(filename: str) -> dict: 

    path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(path_to_file, 'r', encoding='utf-8') as fh:
            content = json.load(fh)
            return content
    except FileNotFoundError as ex:
        my_logger.log(f"File does not exist - {ex} !", 40)

def upload_authors():

    try:
        authors = data_from_file("authors.json")
        for el in authors:
            Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                born_location=el.get('born_location'), description=el.get('description')).save()
    except Exception as ex:
        my_logger.log(ex, 40)

def upload_quotes():
    
    try:
        quotes = data_from_file('quotes.json')
        for el in quotes:
            author, *_ = Author.objects(fullname=el.get('author'))
            Quote(quote=el.get('quote'), tags=el.get('tags'), author=author).save()
    except Exception as ex:
        my_logger.log(ex, 40)

@sync_time
def main():
    try:  
        upload_authors()
        upload_quotes()
    except Exception as ex:
        my_logger.log(ex, 40)

if __name__ == "__main__":
    main()
