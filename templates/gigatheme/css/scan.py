from os.path import exists
import os
import re
path = 'C:/Users/yop/Desktop/proyects/ada_magic/website/templates'
keyword = 'wow'
def absoluteFilePaths(directory, keyword):
    files = {1}
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            new_path = f'{dirpath}/{f}'
            # print(new_path)
            with open(new_path, 'r', encoding='utf-8') as text:
                try:
                    text = text.readlines()
                except Exception as e:
                    print(f'{e}')
                if keyword in text:
                    files.add(new_path)
    print(files)

            
            
            



absoluteFilePaths(path, keyword)