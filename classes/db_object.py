# Database object

import sqlite3
import config

class db_object():

        """Handles database connexion"""

        def __init__(self, table, fields):

                conf = config.get_conf()
                self.connexion = sqlite3.connect(conf['db_path'])
                self.connexion.row_factory = sqlite3.Row
                self.table = table
                self.fields = fields
                self.prefix = self.table + '_'

                self.namespaces = {
                        'itunes' : 'http://www.itunes.com/dtds/podcast-1.0.dtd',
                        'podcastRF' : 'http://radiofrance.fr/Lancelot/Podcast#',
                }

        def save(self, data):

                cursor = self.connexion.cursor()
                join_prefix = ', ' + self.prefix

                for data_row in data :

                        if data_row['id'] is None:
                                query = """INSERT INTO """ + self.table + """(""" + self.prefix + join_prefix.join(self.fields) + """) VALUES(:""" + ', :'.join(self.fields) + """)"""
                        else:

                                query = """UPDATE """ + self.table + """ SET """

                                for field in self.fields:

                                        if field != 'id':

                                                query += self.prefix + field + """ = :""" + field

                                                if field != self.fields[-1]:
                                                        query += """, """

                                query += """ WHERE """ + self.prefix + """id = :id"""

                        cursor.execute(query, data_row)

                self.connexion.commit()

        def delete(self, data):

                cursor = self.connexion.cursor()
                join_prefix = ', ' + self.prefix

                cursor.execute("""DELETE FROM """ + self.table + """ WHERE """ + self.prefix + """id = :id""", data)
                self.connexion.commit()

        def flush(self):

                cursor = self.connexion.cursor()

                cursor.execute("""DELETE FROM """ + self.table)
                cursor.execute("""DELETE FROM sqlite_sequence WHERE name = '""" + self.table + """'""")
                self.connexion.commit()

        def get_all(self, where, itemLimit, sortOption):

                cursor = self.connexion.cursor()
                join_prefix = ', ' + self.prefix
                
                fields = """"""
                fields += self.prefix + """id"""
                for field in self.fields:
                        fields += join_prefix + field

                condition = """"""

                if where:
                        condition = """ WHERE """
                        for field, value in where.items():
                                
                                if 'timestamp' in field:
                                        condition += self.prefix + field + """ > """ + str(value)
                                else : 
                                        if isinstance(value, str):
                                                condition += self.prefix + field + """ LIKE '""" + value + """'"""
                                        else:
                                                condition += self.prefix + field + """ = """ + str(value)
                                                
                                condition += ' AND ';
                                
                        condition = condition[:-5]
                
                limit = """"""
                if itemLimit:
                        limit = """ LIMIT """ + str(itemLimit)
                        
                
                sort = """"""
                if sortOption:
                        sort = """ ORDER BY """ + sortOption 
                
                query = """SELECT * FROM """ + self.table + condition + sort + limit   
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                return rows

        def get_by_id(self, itemId, maxItems = None):                
                
                item_list = db_object.get_all(self, {'id' : itemId}, maxItems, '')

                return item_list[0]

        def get_class(self, kls):

                parts = kls.split('.')
                module = ".".join(parts[:-1])
                m = __import__( module )

                for comp in parts[1:]:
                        m = getattr(m, comp)

                return m

        # def get_item_by_id(self):


