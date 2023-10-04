# toolbox.dao.Feed
*class*, Feed has a simple but organized structure to store the data
```nohighlight 
Args:
    multi_group (bool, optional): Allows a hierarchical stucture. Defaults to False.
**kwargs: keyword-only argument
    dict_DF : attrDict assign to DF attribute
    dict_PAR: attrDict assign to PAR attribute
    dict_MAP: attrDict assign to MAP attribute
```

## **Basic Feed**
The default mode for Feed (when multi_group=False). It has three attributes:
- DF: Dictionary that all values are Dataframes
- PAR: Dictionary that all values are Constants (int, float, string)
- MAP: Dictionary that all values are hash mapping


### toolbox.dao.Feed.DF.add  
*method*, add an item for DF  
```nohighlight
Args:
    var (DataFrame): DataFrame to add to DF
    property_name (str): property name  
```

### toolbox.dao.Feed.DF.delete 
*method*, delete an item for DF  
```nohighlight
Args:
    property_name (str): property in DF  
```

### toolbox.dao.Feed.DF.allitems 
*property*, list of all items in DF

### toolbox.dao.Feed.DF.df_dtype_refine
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

### toolbox.dao.Feed.DF.key_standardization
*method*, standardize the dictionary key by standardize_func
```nohighlight
Args:
    standardize_func (callable, optional): string conversion function. Defaults to toolbox.string.convert_functions.upper_and_replace_space_with_underscore.
```


### toolbox.dao.Feed.DF.column_standardization
*method*, standardize the column name for each dataframe under DF by standardize_func
```nohighlight
Args:
    standardize_func (callable, optional): string conversion function. Defaults to upper_and_replace_space_with_underscore.
    inplace (bool, optional): whether to modify the DataFrame rather than creating a new one. Defaults to False.

Returns:
    Dataframe: it would be different than original DF property if `inplace=False`
```


### toolbox.dao.Feed.DF.size_summary 
*property*, the size of each item; data storage units are self-adjusted

### toolbox.dao.Feed.PAR.add 
*method*, add an item for PAR
```nohighlight
Args:
    var (any): variable to add to PAR
    property_name (str): property name  
```

### toolbox.dao.Feed.PAR.delete 
*method*, delete an item for PAR
```nohighlight
Args:
    property_name (str): property in PAR  
```

### toolbox.dao.Feed.PAR.allitems 
*property*, list of all items in PAR


### toolbox.dao.Feed.PAR.export_df
*method*, Return a DataFrame by gathering all parameter:value pairs within PAR; two return formats are provided  
```nohighlight
Args:
    format (_export_mode, optional): 
            "stacked" or "multi-column". 
             Defaults to "multi-column".
Returns:
    DataFrame
```

### toolbox.dao.Feed.PAR.key_standardization
*method*, standardize the dictionary key by standardize_func
```nohighlight
Args:
    standardize_func (callable, optional): string conversion function. Defaults to toolbox.string.convert_functions.upper_and_replace_space_with_underscore.
```

### toolbox.dao.Feed.PAR.df_dtype_refine
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

### toolbox.dao.Feed.PAR.size_summary 
*property*, the size of each item; data storage units are self-adjusted


### toolbox.dao.Feed.MAP.add 
*method*, add an item for MAP
```nohighlight
Args:
    var (dict): hash mapping to add to MAP
    property_name (str): property name  
```

### toolbox.dao.Feed.MAP.delete 
*method*, delete an item for MAP
```nohighlight
Args:
    property_name (str): property in MAP 
```

### toolbox.dao.Feed.MAP.allitems 
*property*, list of all items in MAP


### toolbox.dao.Feed.MAP.key_standardization
*method*, standardize the dictionary key by standardize_func
```nohighlight
Args:
    standardize_func (callable, optional): string conversion function. Defaults to toolbox.string.convert_functions.upper_and_replace_space_with_underscore.
```

### toolbox.dao.Feed.MAP.df_dtype_refine
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

### toolbox.dao.Feed.MAP.size_summary 
*property*, the size of each item; data storage units are self-adjusted


## Example of basic Feed
### Insert data from scratch 
```python
from toolbox.dao import Feed
 
feed = Feed()
feed.PAR.add("liam",property_name="user_name")
print(feed.PAR.user_name)

feed.MAP.add(
    {"liam":"boy","milly":"girl"},
    "sexual"
)
print(feed.MAP.sexual["milly"])
```
```shell
liam
girl
```

### Initial a Feed by Loader
Insert data by passing a `toolbox.dao.files.Loader` or `toolbox.dao.attrDict` 

```python
from toolbox.dao import Feed
from toolbox.dao.files import FileLoader

path = "projects/testing/test2"
FL = FileLoader(path, archive=False)
FL.execute()

model_input = Feed(dict_DF=FL)
print(model_input)
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
  ]
},
{
  "PAR": []
},
{
  "MAP": []
}

```





## **Hierarchical Feed**
When initial an instance of Feed, set `multi_group = True`.
This mode enables self-named properties for Feed to create a hierarchical structure to better organize data.

### toolbox.dao.Feed.add_new_group
*method*, add property for the instance of Feed

```nohighlight
Args:
    group_name (str): group name
**kwargs: keyword-only argument
    dict_DF : attrDict assign to DF attribute for this new group
    dict_PAR: attrDict assign to PAR attribute for this new group
    dict_MAP: attrDict assign to MAP attribute for this new group
```
Once you have executed this method, a new property will be added on the instance of Feed. Each new property will just be like a basic Feed which has three attributes DF, PAR, and MAP to organize your data.


### Example of Hierarchical Feed
```python
import pandas as pd

mf = Feed(multi_group=True)
mf.add_new_group("school")
student_info = pd.DataFrame({
    "name":["liam","krishna","asha"],
    "department":["IEOR","IEOR","STAT"]
}
)
mf.school.DF.add(student_info,"student")
print(mf.school.DF.student)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>department</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>liam</td>
      <td>IEOR</td>
    </tr>
    <tr>
      <th>1</th>
      <td>krishna</td>
      <td>IEOR</td>
    </tr>
    <tr>
      <th>2</th>
      <td>asha</td>
      <td>STAT</td>
    </tr>
  </tbody>
</table>
</div>

### Initial a Feed by Loader
Here is an example of how to collaborate with `toolbox.dao.files.Loader`

```python
from toolbox.dao import Feed
from toolbox.dao.files import FileLoader

path = "projects/testing/test2"
FL = FileLoader(path, archive=False)
FL.execute()

model_input = Feed(multi_group=True)
model_input.add_new_group("group_A",dict_DF=FL)
print(model_input)
```

```nohighlight
data attributes: 
{
  "group_A": [
    {
      "DF": [
        "projection_2427",
        "eng_hours",
        "workstation_2427",
        "flowAdjust_2427_HAZ",
        "conversion_2427_HAZ",
        "EMSAvailableTools_2427",
      ]
    },
    {
      "PAR": []
    },
    {
      "MAP": []
    }
  ]
}
```

### Reduce memory usage
apply method `df_dtype_refine` to reduce memory usage by assigning different data types.
This method also works for `toolbox.dao.files.FileLoader`. 
Property `size_summary` helps checking the results in size. 

```python
from IPython.display import HTML
FL = FileLoader("examples/file_loader_testing/2427.tar.gz",True)
FL.execute()
display(HTML("original summary:\n"),FL.size_summary)

display(HTML("revised summary:\n"),FL.df_dtype_refine().size_summary)
```

```nohighlight
original summary:
{'projection_2427': '1.93 MB',
 'eng_hours': '63.74 KB',
 'workstation_2427': '781.95 KB',
 'flowAdjust_2427_HAZ': '30.00 MB',
 'conversion_2427_HAZ': '571.81 KB',
 'EMSAvailableTools_2427': '5.22 MB',
 'availableSummary-Readonly': '35.17 MB'}
revised summary:
{'projection_2427': '774.86 KB',
 'eng_hours': '29.17 KB',
 'workstation_2427': '291.27 KB',
 'flowAdjust_2427_HAZ': '10.78 MB',
 'conversion_2427_HAZ': '222.98 KB',
 'EMSAvailableTools_2427': '1.93 MB',
 'availableSummary-Readonly': '15.81 MB'}
```

FL.df_dtype_refine() will only return a copy of FL with revised data types; you either assign the result to a varialbe such as  

```python
new_FL = FL.df_dtype_refine()
```

or use Arg inplace, just like it works for most Pandas methods, to activate the change right on original data

```python
FL.df_dtype_refine(inplace=True)
```

# toolbox.dao.DataMigrator
*class*, DataMigrator is created to migrate data from a database to Azure Blob Storage
```nohighlight
Args:
    blob_access (toolbox.dao.connector.db_access): db_access for target blob storage
    db_access (toolbox.dao.connector.db_access): db_access for source database
```
### toolbox.dao.Feed.DF.migrate  
*method*, migrate data from source db to target Azure Blob Storage    
```nohighlight
Args:
    period (tuple(int,)): (start_week,end_week), e.g., (202201,202208)
    target_folder_path (str): path of the target folder
    predefined_query_name (str): name of predefined query for source db
    cache_name (str): label for the cache file(s) without timestamp
    queires_dir (str, optional): where to looking for predefined query. Defaults to "./queries".
    chunk_mode (bool, optional): pull data in chunk mode or not. Defaults to False.
    enforce_dtype (bool, optional): enforce to convert data type for resulted dataframe. Defaults to True.
```
Example:
```python
from toolbox.dao import DataMigrator
from toolbox.dao.connector import BlobConnector,DBConnector,parse_db_access
from toolbox.utility import set_logger

logger = set_logger('DEBUG')

blob_access = parse_db_access("db.ini","BLOB_Storage")
BC = BlobConnector(blob_access)

db_access = parse_db_access("db.ini","XEUS")
DBC = DBConnector(db_access)

DM=DataMigrator(
    blob_access=blob_access,
    db_access=db_access
)

DM.migrate(
    period=(202338,202339),
    target_folder_path="test",
    cache_name="test_df",
    queires_dir="./toolbox/dao/queries/",
    predefined_query_name="pull_raw_lot_flow",
    chunk_mode=True,
    enforce_dtype=True
)
```

### toolbox.dao.map_db_datatypes_to_dtype
*method*, map database data type to dtype for Pandas dataframe
```nohighlight
Args:
    database_type (str): engine.dialect.name where engine is Sqlalchemy Engine
    database_driver (str): engine.driver where where engine is Sqlalchemy Engine
    db_data_type (str): str(result.cursor.description[i][1]) for the ith columns of query result where result is the Sqlalchemy CursorResult
    datatype_mapper (dict): map out db data types to dtypes for dataframe

Returns:
    type/str: dtype for Pandas
```

### toolbox.dao.get_column_names_and_date_types
*method*, get names and data types of each columns from sqlalchemy.engine.CursorResult  
```nohighlight
Args:
    result (CursorResult): sqlalchemy.engine.CursorResult

Returns:
    (List,List)
```