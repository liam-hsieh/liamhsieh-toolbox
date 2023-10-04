# toolbox.dao.files

As the core data structure in the field of data analytics, Dataframe has been widely supported by many software packages especially in Python/R open-source communities. Just like a table in conventional databases or a spreadsheet, Dataframe organizes data into a 2-dimentional table of rows and columns.  

The class *Loader* provides the basic functionality for loading data from those essential data sources/types and storing the data in Dataframe(s) which are organized by a Python Dictionary. If the data sources are a number of spreadsheets, the Python Dictionary is going to be composed of several key-value pairs that uses names of spreadsheets as key and Dataframes as value. 

It also has an *export* method to convert the Dictionary to flat files, the supported formats are:  

- **CSV**: the Dictionary keys will be the file names of csv
- **Excel**:  the Dictionary keys will be the worksheet names
- **Sqlite**: the Dictionary keys will be the table names
- **JSON**: the Dictionary keys will be the properties name; the Dictionary value(s), Dataframe, will be JSON array(s) 


## toolbox.dao.files.FileLoader
*class*
```nohighlight
Args:
    path (str): a path to a file or directory
    archive (bool, optional): if an archive file is the target of the path. Defaults to False.
```

## toolbox.dao.files.FileLoader.execute
*method*, load file(s) 

argument `path` could be the path to a file of folder; if the file is archived, optional argument `archive` should be passed with value True.  
Once the instance has been initialized, use method `execute` to return the results as a dictionary. 

Load source data to a dictionary. Path can only point to a file or directory(includes multiple identical files).
        Supported file types:  
            - comma-separated values (.csv)
            - Excel (.xlsx, .xlsb)
            - Sqlite (.db, .sqlite)
            - JSON (.json)
            - Apache Parquet (.parquet)
            - Python pickle file (.pkl)

For loading multiple files, only supports csv, pkl, or parquet.
path can also point to an archive of file(s) of a folder, the compress method can be:  
                - tar.gz
                - tar.bz2
                - tar.xz
                - zip

### toolbox.dao.files.FileLoader.df_dtype_refine
*method*, refine all Pandas DataFrames by assigning new data types which save more memory
Based on the contents, data types of numerical columns will be downcast; Pyarrow string will be assigned for string columns.  
```nohighlight
Args:
    inplace (bool, optional): affects original data or not. Defaults to False.
    ignored_dfs (list, optional): list of keys that will be ignored by this method.

Returns:
    object: copy of effective instance
"""
```

### toolbox.dao.files.FileLoader.size_summary 
*property*, the size of each item; data storage units are self-adjusted


## Example of Loader  

```python
from toolbox.dao.files import FileLoader

# for single file
path = "./projects/test/dev.csv"
FL = FileLoader(path, archive=False)
FL.execute()

# for multiple files (assume a number of csv are under directory test)
path = "./projects/test"
FL = FileLoader(path, archive=False)
FL.execute()

# for archive 
path = "./projects/test/dev.tar.gz"
FL = FileLoader(path, archive=True)
FL.execute()

print(FL)
print(FL.eng_hours) #alternative use: FL["eng_hours"]
```

```nohighlight
{
    "avaliable keys": [
        "projection_2427",
        "eng_hours",
        "workstation_2427",
        "flowAdjust_2427_HAZ",
        "conversion_2427_HAZ",
        "EMSAvailableTools_2427"
    ],
    "input_path": "/home/lhsieh/projects/../test/dev.tar.gz",
    "archive": false
}



          Area           WS_name  start_ww_num  engg_hours
0        PHOTO        AMAT_6I_CD        202327      252.00
1     DRY ETCH    AMAT_ADVTG_MET        202327       28.57
2    DIFFUSION  AMAT_CENT_DPNRTP        202327       28.38
3    DIFFUSION     AMAT_CENT_RPO        202327       65.68
4    DIFFUSION    AMAT_CENT_RPO2        202327       79.75
..         ...               ...           ...         ...
174        PVD      ULVAC_ENT_HM        202327       59.00
175    IMPLANT  VARI_PLAD_HC_B2H        202327       17.47
176    IMPLANT  VARI_PLAD_HC_BF3        202327       19.65
177    IMPLANT   VARI_VST900P_MC        202327      120.96
178    IMPLANT  VARI_VSTTRDXP_HC        202327      260.04

[179 rows x 4 columns]
```

`files.FileLoader` can pass to `toolbox.dao.Feed` as its attribute `DF`

**example**
```python
from toolbox.dao import Feed
from toolbox.dao.files import FileLoader

path = "./projects/test/dev.tar.gz"
FL = FileLoader(path, archive=True)
FL.execute()

model_input = Feed(dict_DF=FL)
print(model_input)
# access DataFrame eng_hours using model_input.DF.eng_hours
```

```nohighlight
data attributes: 
{
    "DF": [
        "projection_2427",
        "eng_hours",
        "workstation_2427",
        "flowAdjust_2427_HAZ",
        "conversion_2427_HAZ",
        "EMSAvailableTools_2427",
    ],
    "MAP": [],
    "PAR": []
}


print(model_input.DF.eng_hours)
```

**Reference**  
JSON example  

An example JSON format for Loader is like:  
```json
{
    "Dataset_1": [
        {
            "First_name": "Liam",
            "Last_name": "Hsieh",
            "Weight": 140,
            "Espanol": False,
        },
        {
            "First_name": "Milly",
            "Last_name": "Hsieh",
            "Weight": 45,
            "Espanol": False,
        },
    ], 
    "Dataset_2": [
        {
            "Week": 202235,
            "Math": "Tue-4",
            "English": "Wed-2",
            "Recess": "Thu-6",
        },
        {
            "Week": 202236,
            "Math": "Tue-3",
            "English": "Fri-1",
            "Recess": "Wed-5",
        },
    ]
}
```

JSON arrays are applied for pandas DataFrame. 

