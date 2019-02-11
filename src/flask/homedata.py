import peewee as pw
import os

import config


DATABASE = os.path.dirname(os.path.realpath(__file__)) + '/..' + config.db_config['queries']['url']
database = pw.SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(pw.Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class Query(BaseModel):
    file_name = pw.CharField()
    params = pw.CharField()
    title = pw.CharField()
    description = pw.CharField()
    image = pw.CharField()

    class Meta:
        db_table = 'queries'


class HomeData:
    def __init__(self):
        self.queries = HomeData.get_queries()

    @staticmethod
    def get_queries():
        return Query





