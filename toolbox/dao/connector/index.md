# toolbox.dao.connector
*module*, connector is a wrapper for formalizing the way we access databases, it currently supports:

- MS SQL Server
- Oracle
- MariaDB
- mongodb (testing)
- Azure Blob Storage

## toolbox.dao.connector.parse_db_access
*function*, parse the , e.g., db.ini, to acquire required information for connecting DB.
```nohighlight
Args:
    config_path (str): path of configuration file
    section_name (str): section name for db access in config file

Returns:
    Dict: access information
```

Configuration file should have contents as below, please note that the section [SSL] is required if create connection via ssl, i.e., via_ssl = True. Default port won't be always fit your environment, it is better set in db.ini if this information is given.
For setting a section for SQL server, you can set driver = FreeTDS if that is the case; package will detect the installed ODBC driver on your machine to create connection if driver is not assigned.

```ini
# db_type is mandatory for every section and its value must be an element in (mssql, oracle, azure-blob, mariadb, mongodb)
# the only exception is SSL which provides the required infomration to connect via ssl

[<section_name1>]
server_username = <username>
server_password = <passwd>
server = <hostname.domainname>
database_name = <db_name>
db_type = mssql


[<section_name2>]
server_username = <username>
server_password = <passwd>
server = <hostname.domainname>
service_name = <intended_service_name>
db_type = oracle
port = 1521

[<section_name3>]
DefaultEndpointsProtocol = https
AccountName = <Account name>
AccountKey = <Access key>
EndpointSuffix = core.windows.net
container = <container name>
db_type = azure-blob

[<section_name4>]
user = <username>
password = <passwd>
host = <hostname.domainname>
port = 3307
database = <db_name>
raise_on_warnings = True
db_type = mariadb

[SSL]
cert = /<path>/<yours>.crt
key = /<path>/<yours>.key
ca_certificate = /<path>/<your-chain>.pem
```

`parse_db_access` parse .ini file and return required information for creating instance of `DBConnector` 

**example**
```python
from toolbox.dao.connector import parse_db_access

db_access = parse_db_access("db.ini","BASE")
```

## toolbox.dao.connector.estimate_chunk_size
*function*, This function will estimate the idea chunk size which will result the output file around desired size
```nohighlight
Args:
    conn_str (str): connection string for creating database connection object; it has to meet the requirement for sqlalchemy 
    query (str): query statement
    cached_file_type (str, optional): intended file type in these options ['parquet.gzip','pickle','csv']. Defaults to 'parquet.gzip'.
    compression_method (str, optional): compression method for output file. Defaults to 'gzip'.
    threshold_size (float, optional): desired size for output file in MB. Defaults to 10.0.
    sample_nrow (int, optional): sample size in number of rows. Defaults to 2000.

Returns:
    int: number of rows as chunk size

For more information regarding conn_str, see https://docs.sqlalchemy.org/en/20/core/engines.html    
```

## toolbox.dao.connector.read_sql_query_in_chunks_sqlalchemy
*function*, Retrieve data from a database in assigned-sized chunks.
```nohighlight
Args:
  query: SQL query to execute.
  engine: SQLAlchemy engine object.
  threshold: Maximum number of rows to fetch in each chunk.

Returns:
  A generator that yields DataFrames for each chunk of data.
```

## toolbox.dao.connector.read_sql_query_in_chunks_oracle
*function*, Retrieve data from an Oracle database in adaptive-sized chunks using cx_Oracle.
```nohighlight
Args:
  query: SQL query to execute.
  connection: cx_Oracle Database connection object; Establish a connection to the Oracle database by cx_Oracle.connect(connection_string) and the format of connection_string is "user/password@hostname:1521/your_service_name"
  threshold: Maximum number of rows to fetch in each chunk (default is 20,000).

Returns:
  A generator that yields DataFrames for each chunk of data.
```



## toolbox.dao.connector.load_query_result_into_df_with_intended_dtypes
*function*, Turn query record set into Pandas dataframe with intended dtype.
```nohighlight
Args:
    rs : record set, i.e.,sequence[row]. Returns of sqlalchemy result.fetchall() or .fetchmany() 
    result : sqlalchemy CursorResult
    mapper (dict): map out database data type and dtypes for dataframe

Returns:
    pd.DataFrame
```

## toolbox.dao.connector.BlobConnector
*class*
```nohighlight
Args:
  db_access (dict): return of parse_db_access()
```

### toolbox.dao.connector.BlobConector.check_blob_existance
*method*, Blob exists or not
```nohighight
Args:
    blob_name (str): path of target blob

Returns:
  bool: exists or not
```

### toolbox.dao.connector.BlobConnector.get_blob_list
*method*, list of existing blob names in target container  
If folder_path is None, return all blob names in the container
```nohighlight
Args:
    folder_path (str, optional): path of a specific folder. Defaults to None. If it ends with '/', folder itself won't be included as part of results

Returns:
    list[str]: list of blob names
```

### toolbox.dao.connector.BlobConnector.walk_blob_container  
*method*, returns a generator to list the blobs under the specified container. The generator will lazily follow the continuation tokens returned by the service. This operation will list blobs in accordance with a hierarchy, as delimited by the specified delimiter character.  
```nohighlight
args:
    name_starts_with (str): Filters the results to return only blobs whose names begin with the specified prefix.
    include (list[str] or str): Specifies one or more additional datasets to include in the response. 
            Options include: 'snapshots', 'metadata', 'uncommittedblobs', 'copy', 'deleted', 'deletedwithversions', 'tags', 'versions', 'immutabilitypolicy', 'legalhold'.
    delimiter (sr): When the request includes this parameter, the operation returns a BlobPrefix element in the response body that acts as a placeholder for all blobs whose 
                    names begin with the same substring up to the appearance of the delimiter character. The delimiter may be a single character or a string.
Returns:
    generator: An iterable (auto-paging) response of BlobProperties.
Check doc for blob_container_client.walk_blobs to learn more 
```

### toolbox.dao.connector.BlobConnector.get_blob_name  
*method*,blob_name is the path for accessing a specific blob via blob_container_client
        Conceptually, it will look like <folder_name>/<subfolder_name>/<file_name>
        it only provides file_name as blob_path, it sets container root as like 'working directory'  
```nohighlight
Args:
    file_name (str): file name
    blob_path (str): blob path

Returns:
    blob_name (str): blob_name
```


### toolbox.dao.connector.BlobConnector.del_blob
*method*, delete a blob
```nohighlight
Args:
    blob_name (str): path of target blob
```

### toolbox.dao.connector.BlobConnector.add_folder
*method*, Add a empty virtual folder. If the folder exists, all contents will be purged.
        For example, in target container, we already have a virtual folder called <folder_X> and you want to add a empty folder,<folder_Y>, under <folder_X>, set folder_name as '<folder_X>/<folder_Y>'
```nohighlight
Args:
    folder_path (str): full path of intended virtual folder which should not end with `/`
```


### toolbox.dao.connector.BlobConnector.file_upload
*method*, upload local file to Azure Blob Storage; delete blob first, if same blob exists.
When blob_path is None, file will be put right in the container.
To put file in a given folder, blob_path is required.
```nohighlight
Args:
    file_path (str): file path
    blob_path (str): blob path; default in None
```

### toolbox.dao.connector.BlobConnector.upload_parquet_from_df
*method*, convert a DataFrame object to parquet then upload to Azure Blob Storage; delete blob first, if same blob exists. This method is a stream-base operation. Remember, blob only has virtual folder so files in a folder have blob name including folder name. As reference, gzip is often a good choice for cold data, which is accessed infrequently; snappy are a better choice for hot data, which is accessed frequently.
```nohighlight
Args:
    df (pd.DataFrame): source dataframe
    blob_path (str): path points to the location for uploading the file 
    file_name (str): name of the file
    compression (str, optional): 'gzip' or 'snappy'. Defaults to None.

Raises:
    ValueError: file_name should end by .gzip or .snappy if enable compression
    ValueError: file_name should end by .parquet if no compression
    ValueError: unsupported string is passed as compression
```


### toolbox.dao.connector.BlobConnector.upload_csv_from_df
*method*, convert a DataFrame object to csv then upload to Azure Blob Storage; delete blob first, if same blob exists. This method is a stream-base operation. Remember, blob only has virtual folder so files in a folder have blob name including folder name.
```nohighlight
Args:
    df (pd.DataFrame): source dataframe
    blob_path (str): path points to the location for uploading the file 
    file_name (str): name of the file
    archive (bool, optional): zip it or not. Defaults to True.

Raises:
    ValueError: blob_name should end by .zip if archive
    ValueError: blob_name should end by .csv if not archive
```

**Example**

```python
from toolbox.dao.connector import parse_db_access, BlobConnector
import pandas as pd
db_access = parse_db_access("./examples/db_connector_testing/db.ini","localsolverdata")
BC = BlobConnector(db_access)

#upload to Blob storage from a dataframe instance
df = pd.read_pickle("./examples/db_connector_testing/oracle_queries/test.pkl")
BC.upload_csv_from_df(df,'implanttestavail/wafer_cost/',"example.zip", archive=True)

#upload a file to Blob storage from local machine
BC.file_upload(file_path="example.csv",blob_path='implanttestavail/wafer_cost/')
```


### toolbox.dao.connector.BlobConnector.blob_dump
*method*, download specified blob to the specified location
```nohighlight
Args:
    blob_name (str): blob_path+file_name, path of the blob because Blob storage uses virtual folder
    dir_path (str, optional): specified location of keeping the blob file. Defaults to ".".
    to_memory (bool, optional): assign in-momery zip object as return type if True. Defaults to False.
    to_dataframe (bool, optional): assign pandas dataframe as return type. It works only if the blob is csv/xlsx. Defaults to False.
    to_attrDict (bool, optional): assign toolbox.dao.feed.attrDict as return type if True. It works only if the blob is an archive of csv file(s). Defaults to False.

Raises:
    ValueError: if target container doesn't have any blob named blob_name

Returns:
    _type_: Defaults to None; But toolbox.dao.feed.attrDict if to_attrDict else in-momery zip object if to_memory
```

**Example**

```python
display(BC.blob_list)
blob_name='implanttestavail/wafer_cost/2548.zip'
# download blob to the specified location (for those formats that toolbox doesn't support processing in stream)
_ = BC.blob_dump(blob_name, dir_path = "./examples")

# return an in-memory zip object (better for shortening the download time and developers can continue the remaining process in stream)
rs = BC.blob_dump(blob_name, to_memory=True)
display(rs)

# return toolbox.dao.feed.attrDict (one of essentail Python Class for AODS projects, Blob has to be zipped csv/xlsx)
# if blob is a single csv/xlsx, it returns a Pandas DataFrame
rs = BC.blob_dump(blob_name, to_attrDict=True)
display(rs)

# return Pandas DataFrame (when blob is a single csv/xlsx)
_ = BC.blob_dump(blob_name, to_dataframe=True)
```

```
['2548.zip', 'blob_example.zip', 'test.zip', 'test3.zip', 'test_full_fab.zip']

<zipfile.ZipFile file=<_io.BytesIO object at 0x7fb5dc87a8e0> mode='r'>

{
  "avaliable keys": [
    "acl_output",
    "baseline_depr",
    "capital_plug",
    "cash_cost_probe_yield",
    "die_specs",
    "max_outs",
    "params",
    "solver_output",
    "solve_details",
    "week_month_qtr_year"
  ]
}
```


## toolbox.dao.connector.DBConnector
*class*
```nohighlight
Args:
  db_access (dict): return of parse_db_access()
  via_ssl (bool, optional): connect via ssl. Default is False
```

### toolbox.dao.connector.DBConnector.pull_SQL
*method*, return the results of the SQL query
```nohighlight
Args:
    query (str): sql statement

Return:
    df (DataFrame): results of executing SQL statement if it has return
```

**Example**

```python
from toolbox.dao.connector import DBConnector
db_access = parse_db_access("db.ini","MariaDB")
DBC = DBConnector(db_access)
df = DBC.pull_SQL("select top(2) * from example_DB2..wkg_ww ww")
print(df)
```
```nohighlight
    ww_id  ww_num  mon_num  fis_qtr_num  cal_qtr_num          start_date  \
0  27842  199901   199812       199902       199804 1998-12-31 19:00:00   
1  27843  199902   199901       199902       199901 1999-01-07 19:00:00   

              end_date work_ww work_mon work_qtr  
0 1999-01-07 18:59:59     None      None      None  
1 1999-01-14 18:59:59     None      None      None  
```

```python
# connect via ssl
DBC = DBConnector(db_access,via_ssl=True)
print(DBC.pull_SQL("SELECT * FROM test_table"))
```
```nohighlight
  id name value 
0 A1 Milly  100
1 A2 Liam    60
```

### toolbox.dao.connector.DBConnector.set_queries_dir
*method*, set up path for directory where predefined sql statement files are stored
```nohighlight
Args:
    queires_dir (str): path of directory
**kwargs:
    all variables within predefiend sql queries can assign their values to DBConnector via keyword arguments
```        
This method accepts keyword arguments (`**kwargs`). The most common usage is to assign values for all variables within predefined SQL statement files to a dictionary as an argument for intended method/function; `DBConnector` will handle the rest of things while pulling data by predefined SQL statement files for you. See example of `DBConnector.pull_predefined_query`.

### toolbox.dao.connector.DBConnector.pull_predefined_query
*method*, pull data by predefined SQL statement file including variables. Reliable chunk_mode allows to pull large scale data by chunk with a self-adaptive chunk size determination. database data types could be converted to intended dtypes for resulted DataFrame to avoid unexpected errors.  
```nohighlight
Args:
    query_name (str): name of a predefined sql statement file; no extension needed
    chunk_mode (bool): pull data by chunk mode or not
    
    kwargs: 
            - chunk_size (int): number of rows for a chunk; estimate_chunk_size() will be trigger when chunk_size is not assigned. Therefore, more details for accepted kwargs could check description of function estimate_chunk_size()
            - capitalize_column_name (bool): convert all column name to uppercase or not
            - enforce_dtype (bool): convert database data types to intended dtypes for resulted dataframe; only enables for chunk_mode
Raises:
    Exception: queries_dir can't be empty, set by method set_queries_dir() first
    ValueError: if <query_name>.sql can't be found in queries_dir

Returns:
    DataFrame: result of executing SQL statement
```


### toolbox.dao.connector.DBConnector.load_args_for_predefined_query
*method*, This method returns the query statement for pulling data by filling in query arguments for predefined query
```nohighlight
Args:
    query_file (str): name of predifined query file (extension should be .sql)
    query_args (dict, optional): dictionary of query arguments. Defaults to None.

Returns:
    str: sql query statement
```


### toolbox.dao.connector.DBConnector.set_cache_dir
*method*, set up path for directory where cached files are stored
```nohighlight
Args:
    cache_dir (str): directory for keeping/searching cache files

    cache_mode (int, optional): 
                        0: always pull data from db
                        1: only pull data if cache doesn't exist
                        2: refresh cache before using 
                        Default to 1 (Class defaults is 0)
```

### toolbox.dao.connector.DBConnector.del_cache
*method*, delete all cache files in cache directory


**Example** 

```python
query_args = {
        "scen_id" : 2440,
        "iter_num" : 1,
}
DBC = DBConnector(db_access)
DBC.set_queries_dir("./loader/queries", **query_args)
df = DBC.pull_predefined_query("wafer_eq-projection")
df
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>scen_id</th>
      <th>iter</th>
      <th>fab_loc_name</th>
      <th>design_name</th>
      <th>node</th>
      <th>ww_num</th>
      <th>qty</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>16A</td>
      <td>1100</td>
      <td>201801</td>
      <td>5000.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>16AX</td>
      <td>1100</td>
      <td>201801</td>
      <td>200.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>17A</td>
      <td>1100</td>
      <td>201801</td>
      <td>2207.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>17AX</td>
      <td>1100</td>
      <td>201801</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>27A</td>
      <td>1200</td>
      <td>201801</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>307</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>27A</td>
      <td>1200</td>
      <td>201826</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>308</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>17AX</td>
      <td>1100</td>
      <td>201826</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>309</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>17A</td>
      <td>1100</td>
      <td>201826</td>
      <td>6357.0</td>
    </tr>
    <tr>
      <th>310</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>16AX</td>
      <td>1100</td>
      <td>201826</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>311</th>
      <td>2440</td>
      <td>1</td>
      <td>F68</td>
      <td>16A</td>
      <td>1100</td>
      <td>201826</td>
      <td>5000.0</td>
    </tr>
  </tbody>
</table>
<p>312 rows × 7 columns</p>
</div>

contents of *wafer_eq-projection.sql*:
```sql
declare @scen_id int = '{scen_id}'
declare @iter int = '{iter_num}'

select 
    iter.scen_id, 
    iter.iter, 
    iter.fab_loc_name, 
    iter.design_name, 
    iter.node, 
    ww.ww_num, 
    iter.qty
from example_DB1..z_iter_fab_design_parm iter
join example_DB2..wkg_ww ww
on ww.ww_id = iter.ww_id
where iter.scen_id = @scen_id
and iter.iter = @iter 
```
### toolbox.dao.connector.DBConnector.dump_dfs_generator
*static method*, Dump DataFrames from a generator into a dictionary.

```nohighlight
Args:
    dfs_generator (generator): A generator that yields DataFrames.
    keys (list or None, optional): List of keys for the generated dictionary.
        If None, numerical indices will be used as keys. Default is None.

Returns:
    dict: A dictionary containing DataFrames from the generator, with keys as specified.
```
Example:
```python
# Generate sample DataFrames
num_dataframes = 5
rows_per_dataframe = 10
dataframes = generate_dfs(num_dataframes, rows_per_dataframe)

# Test the dump_dfs_generator method
keys = ['DF1', 'DF2', 'DF3', 'DF4', 'DF5']  # Example keys
result = dump_dfs_generator(dataframes, keys)
print(result)

```

### toolbox.dao.connector.DBConnector.dump_to_db
*method*, dump a dataframe to a specific db table  

```nohighlight
Args:
    df (_type_): _description_
    dest_tb_name (_type_): _description_
    is_fast_executemany (bool, optional): _description_. Defaults to True.
    is_index (bool, optional): add index automatically. Defaults to False.
    if_exists (str, optional): what to do while data exists in table. 'fail', 'replace', 'append'. Defaults to 'append'.
                            How to behave if the table already exists.
                            fail: Raise a ValueError.
                            replace: Drop the table before inserting new values.
                            append: Insert new values to the existing table.
    dtype (dict, optional): dict to dedicate the dtype for each columns. Defaults to None.
                            example dtype:
                            using df column names as keys
                            {
                            'datefld': sqlalchemy.DateTime(), 
                            'intfld':  sqlalchemy.types.INTEGER(),
                            'strfld': sqlalchemy.types.NVARCHAR(length=255)
                            'floatfld': sqlalchemy.types.Float(precision=3, asdecimal=True)
                            'booleanfld': sqlalchemy.types.Boolean
                            }   
```