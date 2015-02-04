import json
import MySQLdb
import urllib2
from user_model import User

import sys, os
class UserSqlInterface():
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def column_exists(self, column, table):
        query = """SELECT * FROM
                   information_schema.COLUMNS
                   WHERE TABLE_SCHEMA=%s
                   AND TABLE_NAME=%s
                   AND COLUMN_NAME=%s""" % (self.database, table, column)
        conn = self.connection()
        cursor = conn.cursor()
        exists = False
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) > 0:
                exists = True
        except Exception as e:
            #print self.error_string(query, e)
            print 'failed to find column: ' + column + ' in table: ' + table
        conn.close()
        return exists

    def connection(self):
        return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)

    def select_all_single_target(self, table, target_column, target_value, type='*', match_partial=False):
        if self.column_exists(target_column, table):
            query = Query(table=table,
                          columns=(target_column),
                          values=(target_value),
                          match_partial=match_partial,
                          type=type)
            conn = self.connection()
            cursor = conn.cursor()
            results = None
            try:
                print 'querying with: ' + query.selection_query()
                cursor.execute(query.selection_query())
                #results = cursor.fetchall()[0][column_number]
                results = cursor.fetchall()
                print 'results: ' + str(results)
            except Exception as e:
                print self.error_string(query, e)
            conn.close()
            return results
        else:
            print 'ERROR: no column in ' + table + ' named ' + target_column
        return None

    def insert(self, table, columns, values):
        query = Query(table=table,
                      columns=columns,
                      values=values
        )
        conn = self.connection()
        cursor = conn.cursor()
        query_str = query.insertion_query()
        print 'insert query: %s' % query_str
        success = True
        try:
            cursor.execute(query_str)
            conn.commit()
        except Exception as e:
            print self.error_string(query_str, e)
            conn.rollback()
            success = True
        conn.close()
        return success

    def update(self, table, columns, values, target, target_value, comparator):
        query = Query(table=table,
                      columns=columns,
                      values=values,
                      target=target,
                      target_value=target_value,
                      comparator=comparator
        )
        conn = self.connection()
        cursor = conn.cursor()
        query_str = query.update_query()
        try:
            cursor.execute(query_str)
            conn.commit()
            success = True
        except Exception as e:
            print self.error_string(query_str, e)
            conn.rollback()
            success = False
        conn.close()
        return success

    def error_string(self, query, error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_string = 'Error type: ' + str(exc_type) + '\nin file: ' + file_name + '\nline #: ' + str(exc_tb.tb_lineno)
        return """\nFailed querying db: %s\nwith query: %s\n%s""" % (self.database, query, error_string)

class Query:
    def __init__(self,
                 table,
                 columns,
                 values,
                 type='*',
                 target='',
                 target_value='',
                 comparator='=',
                 match_partial=False):
        self.type = type
        self.table = table
        self.columns = columns
        self.values = values
        self.target = target
        self.target_value = target_value
        self.comparator = comparator
        self.match_partial = match_partial

    def tuple_to_string(self, tup, remove_quotes=True):
        if type(tup) == tuple:
            tuple_string = str(tup)
            if remove_quotes:
                cleaned_tuple = tuple_string
                for i in range(len(tuple_string)):
                    j = len(tuple_string) - i - 1
                    if tuple_string[j] == "'":
                        cleaned_tuple = cleaned_tuple[:j] + cleaned_tuple[j+1:]
                tuple_string = cleaned_tuple
        else:
            tuple_string = tup
        return tuple_string

    def selection_query(self):
        query = None
        try:
            query = """SELECT %s FROM %s WHERE %s""" % (self.type,
                                                        self.table,
                                                        self.tuple_to_string(self.columns))
            if self.match_partial:
                query += ''' like "%''' + self.tuple_to_string(self.values) + '''%"'''
            else:
                query += """=%s""" % self.values
            print 'selection query: %s\n' % query
        except Exception as e:
            print self.error_string()
        return query

    def insertion_query(self):
        query = """INSERT INTO %s %s VALUES %s""" % \
                (self.table,
                 self.tuple_to_string(self.columns),
                 self.tuple_to_string(self.values, remove_quotes=False))
        return query

    def update_query(self):
        query = """UPDATE %s SET %s WHERE %s%s%s""" % (self.table,
                                                       self.update_string(),
                                                       self.target,
                                                       self.comparator,
                                                       self.target_value)
        return query

    def update_string(self):
        insert_string = ''
        for i in range(len(self.columns)):
            column = self.columns[i]
            value = self.values[i]
            insert_string += column + '=' + value
            if i != len(self.columns) - 1 and len(self.columns) > 0:
                insert_string += ','
        return insert_string

    def error_string(self, query):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_string = 'Error type: ' + str(exc_type) + '\nin file: ' + file_name + '\nline #: ' + str(exc_tb.tb_lineno)
        return """\nBad query db: %s\nwith query: %s\n%s""" % (self.table, query, error_string)
