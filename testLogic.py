import json
from CodeList import pack_type_codeList
from ifcsumTemplate import *
from datetime import datetime
from reusable_function import *


# Some Reusable Function:
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


# Example usage
file_path = 'C:\\Users\\rakro\\Desktop\\EDI Template Class Based\\Input\\XML_IFCSUM Map files\\Sea\\VEN-152017\\VEN-152017.json'  
json_data = read_json_file(file_path)

