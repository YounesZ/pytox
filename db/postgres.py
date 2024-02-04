import csv
import pandas as pd
from io import StringIO
from json import dumps
from psycopg2 import DatabaseError, connect
#from apps.home.config.postgres import HDR_MAPPING
from submodules.pytox.utils.data_structures import is_list_of_strings


FLYER_DESCRIPTION_MAX_WORDS = 50
"""
HDR_MAPPING = {'varchar': [str],
               'numeric': [float, np.float16, np.float32, np.float64, int, np.int16, np.int32, np.int64],
               'numeric[]': [list],
               'text[]': [list],
               'real': [float, np.float16, np.float32, np.float64],
               'integer': [int, np.int16, np.int32, np.int64],
               'serial': [int],
               'boolean': [bool, np.bool_],
               'date': [str]}
"""


# ========================== #
# ===----    INIT    ----=== #
# ========================== #
def init_db_connection(pipeline, POSTGRES_PIPELINES, POSTGRES_SERVER_NAME, POSTGRES_SERVER_PORT):
        # Make connection
        db_name = POSTGRES_PIPELINES[pipeline]['db_name']
        connection = connect(host=POSTGRES_SERVER_NAME,
                             port=POSTGRES_SERVER_PORT,
                             database=db_name,
                             user="mlflow_user",
                             password="mlflow")
        return connection


# ========================== #
# ===----   CREATE   ----=== #
# ========================== #
def create_table(connection, pipeline, POSTGRES_PIPELINES):
    # Make  sure table does not exist
    db_name = connection.info.dbname
    assert db_name == POSTGRES_PIPELINES[pipeline]['db_name']
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    tbl_head = POSTGRES_PIPELINES[pipeline]['tbl_head']
    if check_table_exists(connection, pipeline, POSTGRES_PIPELINES):
        print(f'Table {tbl_name} already exists in postgresql db {db_name}')
        return
    else:
        # Make command
        cmd_col = ["%s %s %s, " % (k_, tbl_head[k_]['type'], tbl_head[k_]['constraint']) for k_ in tbl_head.keys()]
        command = f"CREATE TABLE {tbl_name} ({''.join(cmd_col)[:-2]})"
        try:
            # Make cursor
            cursor = connection.cursor()
            # Create table
            cursor.execute(command)
            # Close
            cursor.close()
            connection.commit()
        except (Exception, DatabaseError) as error:
            print(error)
            cursor.execute("ROLLBACK")
    return


def check_table_exists(connection, pipeline, POSTGRES_PIPELINES):
    # Make cursor
    cursor = connection.cursor()

    # Execute
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    output = False
    try:
        cursor.execute(f"select count(*) from information_schema.tables where table_name='{tbl_name}';")
        output = max(cursor.fetchall()[0])>0
        cursor.close()
    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        print(error)

    # Close
    cursor.close()
    return output


# ========================== #
# ===----    I/O     ----=== #
# ========================== #
def check_entry_exists_in_table(connection, id, pipeline, POSTGRES_PIPELINES):
    # Make cursor
    cursor = connection.cursor()

    # Format input to handle single and batch requests
    if not isinstance(id, list):
        id = [id]

    # Execute
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    interx = []
    output = False
    try:
        cursor.execute(f"select id from {tbl_name};")
        all_ids = cursor.fetchall()
        all_ids = [i_[0] for i_ in all_ids]
        interx = list( set(id).intersection(all_ids) )
        output = len(interx)==len(id)
    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        print(error)

    # Close
    cursor.close()
    return output, interx


def get_entry_by_id(connection, id, pipeline, POSTGRES_PIPELINES):

    # Make cursor
    cursor = connection.cursor()

    # Format input to handle single and batch requests
    if not isinstance(id, str):
        raise TypeError('Unknown type for id: must be a string')

    # Execute
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    output = None
    try:
        cursor.execute(f"select * from {tbl_name} where id='{id}';")
        output = cursor.fetchall()
    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        print(error)

    # Close
    cursor.close()
    return output


def new_entry_in_table(connection, vdict, pipeline, POSTGRES_PIPELINES, mapping):
    # Get table name
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    tbl_head = POSTGRES_PIPELINES[pipeline]['tbl_head']

    # Delete if exists:
    remove_entry_from_table(connection, vdict['id'], pipeline, POSTGRES_PIPELINES)

    # Make new entry
    values = format_values_for_command(tbl_head, vdict, mapping)
    cursor = connection.cursor()
    succes = False
    try:
        cursor.execute(f"insert into {tbl_name} values {values};")
        # Commit changes
        connection.commit()
        succes = True
    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        print(error)
    cursor.close()

    return succes


def remove_entry_from_table(connection, id, pipeline, POSTGRES_PIPELINES):
    # Check if entry is present
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    success = True
    if check_entry_exists_in_table(connection, id, pipeline, POSTGRES_PIPELINES)[0]:
        # Delete entry
        cursor = connection.cursor()
        try:
            cursor.execute(f"delete from {tbl_name} where id='{id}'")
            cursor.close()
            # Commit changes
            connection.commit()
        except (Exception, DatabaseError) as error:
            print(error)
            cursor.execute("ROLLBACK")
            success = False
    return success


def clear_table(connection, pipeline, POSTGRES_PIPELINES):
    success = True
    tbl_name= POSTGRES_PIPELINES[pipeline]['tbl_name']
    if check_table_exists(connection, pipeline, POSTGRES_PIPELINES):
        # Delete entry
        cursor = connection.cursor()
        try:
            cursor.execute(f"delete from {tbl_name};")
            cursor.close()
            # Commit changes
            connection.commit()
        except (Exception, DatabaseError) as error:
            print(error)
            cursor.execute("ROLLBACK")
            success = False
    return success


def read_full_table(connection, pipeline, POSTGRES_PIPELINES):

    # Read pipeline info
    tbl_nm = POSTGRES_PIPELINES[pipeline]['tbl_name']
    tbl_hd = POSTGRES_PIPELINES[pipeline]['tbl_head']

    # Make query
    pg_cmd = f"select * from {tbl_nm}"
    df = execute_manual_query(connection, pg_cmd, tbl_hd)

    return df


def execute_manual_query(connection, pg_cmd, tbl_header):
    # Init connection + cursor
    cursor = connection.cursor()

    try:

        # Make query
        cursor.execute(pg_cmd)
        data = cursor.fetchall()

        # Structure data
        df = pd.DataFrame(data=[], columns=tbl_header)
        for row in data:
            df.loc[len(df),:] = row

        cursor.close()

    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        cursor.close()
        raise Exception(f"Error while executing query data from PostgreSQL %s" % pg_cmd, error)

    return df


def execute_manual_batch_query(connection, pg_cmd, tbl_header, chunksize=None):
    # Init connection + cursor
    cursor = connection.cursor()

    # Define the chunk size
    if chunksize is None:
        chunk_size = 10000

    # Prep container
    allDt = []
    df = pd.DataFrame()

    try:

        offset = 0
        while True:

            # Make query
            query = f"{pg_cmd} LIMIT {chunksize} OFFSET {offset};"
            cursor.execute(query)
            data = cursor.fetchall()

            # If no more rows are returned, break the loop
            if not data:
                break

            # Append to data
            allDt += [pd.DataFrame(data=data, columns=tbl_header)]

            # Increment the offset for the next chunk
            offset += chunksize

        cursor.close()

        # Structure data
        df = pd.concat(allDt)

    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        cursor.close()
        raise Exception(f"Error while executing query data from PostgreSQL %s" % pg_cmd, error)

    return df


def execute_manual_command(connection, pg_cmd):
    try:
        # Init connection + cursor
        cursor = connection.cursor()

        # Make query
        cursor.execute(pg_cmd)
        connection.commit()
        cursor.close()

    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        cursor.close()
        raise Exception(f"Error while executing query data from PostgreSQL %s" % pg_cmd, error)

    return


def execute_raw_query(cmd, connection):

    try:
        cursor = connection.cursor()

        # Make query
        cursor.execute(cmd)

        # Commit the changes to the database
        connection.commit()

        # Housekeeping
        cursor.close()

    except (Exception, DatabaseError) as error:
        raise Exception(f"Error while executing raw query from PostgreSQL %s" % cmd, error)

    return


# ========================== #
# ===---   Bulk I/O   ---=== #
# ========================== #
def send_dataframe_to_postgres(df, connection, pipeline, POSTGRES_PIPELINES, mapping, ignore_existing=False):

    # Get table name
    tbl_name = POSTGRES_PIPELINES[pipeline]['tbl_name']
    tbl_head = POSTGRES_PIPELINES[pipeline]['tbl_head']
    db_name = connection.info.dbname

    # --- Ignore IDs already present
    if ignore_existing:
        # Get table ids
        _, all_ids = check_entry_exists_in_table(connection, list(df.id), pipeline, POSTGRES_PIPELINES)
        # Remove from df
        df = df.loc[~df.id.isin(all_ids)]

    # --- EXIT if empty
    if len(df)==0:
        print(f'Did not sync dataframe with {db_name} db, was empty')
        return True, 0, db_name

    # --- Create a StringIO object
    # Make new entry
    values = [format_values_for_command(tbl_head, df.loc[i_].to_dict(), mapping) for i_ in df.index]
    # Turn values into StringIO
    output = StringIO()
    csv_writer = csv.writer(output)
    for row in values:
        csv_writer.writerow(row)
    # Rewind pointer
    output.seek(0)

    # --- Append to postgres
    # create an SQL statement to insert the data into the table
    columns = ','.join(tbl_head.keys())
    stmt = f'COPY {tbl_name} ({columns}) FROM STDIN WITH (FORMAT CSV, DELIMITER ",", NULL " ")'

    cursor = connection.cursor()
    succes = False
    try:
        cursor.copy_expert(stmt, output)
        # Commit changes
        connection.commit()
        succes = True
    except (Exception, DatabaseError) as error:
        cursor.execute("ROLLBACK")
        print(error)
    cursor.close()

    print(f'Synced dataframe with {db_name} db, {len(df)} entries made')
    return succes, len(df), db_name


# =========================== #
# ===---- DATA FORMAT ----=== #
# =========================== #
def format_values_for_command(header, values, mapping):
    # Prepare output
    output = []
    # Loop over header values
    for i_ in header.keys():
        # Check if value has the right type
        assert isinstance(values, dict)
        assert i_ in values.keys()
        # Assert type
        valtp = header[i_]['type']
        if '(' in header[i_]['type']:
            valtp = header[i_]['type'].split('(')[0]
        try:
            assert type(values[i_]) in mapping[valtp]
        except:
            print('Key %s: type is %s, expected %s'%(i_, type(values[i_]), mapping[valtp]))
        # Append prefix
        if '[]' in valtp:
            # Determine list type
            if is_list_of_strings(values[i_]):
                # Reformat
                strvalues = dumps(values[i_])
                strvalues = '{'+strvalues[1:-1] + '}'
                output.append(strvalues)
            else:
                # Array keyword
                output.append('{' + str(values[i_])[1:-1] + '}')
        else:
            # Process string
            strvalue = values[i_]
            if isinstance(values[i_], str):
                strvalue = values[i_].replace("'", " ")
            output.append(strvalue)
    return tuple(output)




if __name__ == '__main__':
    pass


"""
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d carsnatch.ai -d www.carsnatch.ai -d minio.carsnatch.ai -d minioconsole.carsnatch.ai -d mlflow.carsnatch.ai -d pgadmin.carsnatch.ai -d postgre.carsnatch.ai

docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot -d carsnatch.ai -d www.carsnatch.ai -d minio.carsnatch.ai -d minioconsole.carsnatch.ai -d mlflow.carsnatch.ai -d pgadmin.carsnatch.ai -d postgre.carsnatch.ai
"""
