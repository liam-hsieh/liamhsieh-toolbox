# toolbox.dao.convertor
convertor module provide the capability to convert input data instance to those essential data/file formats such like excel or csv.
Once the instance of `Convertor` is created, based on the type of input object, available class methods may vary 

## toolbox.dao.convertor.Convertor
*class*, essential formats supported for most data type are excel, csv, and sqlite

The basic logic for converting is:
- **CSV**: Dictionary keys will be the file names of csv
- **Excel**:  Dictionary keys will be the worksheet names
- **Sqlite**: Dictionary keys will be the table names
- **JSON**: Dictionary keys will be the properties name; the Dictionary value(s), Dataframe, will be JSON array(s) 


### toolbox.dao.convertor.Convertor.to_csv
*class*, Save as separate CSV files, with each key appended to the filename.

```nohighlight
Args:
    self (FileLoader): instance of FileLoader
    output_path (str): The file path for the CSV files to save.
    index (bool): insert index to csv, default is False
```

### toolbox.dao.convertor.Convertor.to_excel
*class*, Save as an Excel file, with each key as a worksheet name.

```nohighlight
Args:
    self (FileLoader): instance of FileLoader
    output_path (str): The file path of the Excel file to save.
    index (bool): insert index to worksheet, default is False
```

### toolbox.dao.convertor.Convertor.to_json
*class*, Save as a json file

```nohighlight
Args:
    self (FileLoader): instance of FileLoader
    output_path (str): The file path of the json file to save.
```

### toolbox.dao.convertor.Convertor.to_sqlite
*class*, Save as a sqlite db file, with each key as a table name.

```nohighlight
Args:
    self (FileLoader): instance of FileLoader
    output_path (str): The file path of the db file to save.
    if_exists (str) : what to do when table exists. default is 'replace'
```