import mysql.connector
import os
import numpy as np
from imgarray import save_array_img, load_array_img
from os import fsync


def sync(fh):
    fh.flush()
    fsync(fh.fileno())
    return True


def save_array_to_PNG(numpy_array, save_path):
    with open(save_path, 'wb+') as fh:
        save_array_img(numpy_array, save_path, img_format='png')
        sync(fh)

    return save_path


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(png_image):
    try:
        connection = mysql.connector.connect(
            user='Your_user_name',
            password='Your_MySQL_password',
            host='host_address',
            database='database_name')

        sql_table = 'your_table_name'
        image_column_name = 'your_blob_column_name'

        file = convertToBinaryData(png_image)

        cursor = connection.cursor()
        sql_insert_blob_query = "INSERT INTO " + sql_table + " (" + image_column_name + ") VALUES (" + file + ")"
        result = cursor.execute(sql_insert_blob_query)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(save_file_as, ID):
    try:
        connection = mysql.connector.connect(
            user='Your_user_name',
            password='Your_MySQL_password',
            host='host_address',
            database='database_name')

        sql_table = 'your_table_name'
        image_column_name = 'your_blob_column_name'

        cursor = connection.cursor()
        sql_fetch_blob_query = "SELECT " + image_column_name + " from " + sql_table + " where ID = '" + str(ID)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchone()

        file = record[0]
        write_file(file, save_file_as)
        numpy_arr_sql = load_array_img(save_file_as)

        return numpy_arr_sql

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# write Numpy array into MySQL database
# my_numpy_array = np.ones(150, 150)
# insertBLOB(save_array_to_PNG(my_numpy_array, 'image.png'))

# retrieve numpy array from MySQL
# my_numpy_array_from_SQL = readBLOB('image_from_SQL.png', ID=1)