import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

path_to_ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.ini")

from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read(path_to_ini)

mongo_user = config.get('DB_Inputs', 'user')
mongodb_pass = config.get('DB_Inputs', 'pass')
db_name = config.get('DB_Inputs', 'db_name')
domain = config.get('DB_Inputs', 'domain')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
