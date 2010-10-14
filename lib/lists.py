import os
from dbtk.lib.templates import TEMPLATES

class DbTkList:
    """A categorical list of scripts."""
    def __init__(self, name, scripts):
        self.name = name
        self.scripts = scripts


def get_lists():
    from dbtk import DBTK_LIST
    DBTK_LIST = DBTK_LIST()

    lists = []
    lists.append(DbTkList("All Datasets", DBTK_LIST))
    
    # Check for .cat files
    files = os.listdir('categories')
    cat_files = [file for file in files if file[-4:] == ".cat"]
    for file in cat_files:
        cat = open(os.path.join('categories', file), 'rb')
        scriptname = cat.readline().replace("\n", "")
        scripts = []
        for line in [line.replace("\n", "") for line in cat]:
            new_scripts = [script for script in DBTK_LIST
                           if script.shortname == line]
            for script in new_scripts:
                scripts.append(script)
        lists.append(DbTkList(scriptname, scripts))


    # Get list of additional datasets from dbtk.config file
    if os.path.isfile("scripts.config"):
        other_dbtks = []
        config = open("scripts.config", 'rb')
        for line in config:
            if line:
                line = line.strip('\n').strip('\r')
                values = line.split(',')
                try:
                    temp, dbname, tablename, url = (values[0], values[1], 
                                                    values[2], values[3])
                    for template in TEMPLATES:
                        if template[0] == temp:
                            new_dataset = template[1]
                            
                    new_dataset.name = dbname + '.' + tablename
                    new_dataset.shortname = dbname
                    new_dataset.tablename = tablename
                    new_dataset.url = url                    
                    
                    other_dbtks.append(new_dataset)
                except:
                    pass

        if len(other_dbtks) > 0:
            lists.append(DbTkList("Custom", other_dbtks))
            for script in other_dbtks:
                lists[0].scripts.append(script)
    
    return lists