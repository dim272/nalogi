from peewee import *

proxy_db = SqliteDatabase('MyPerfectRequest/proxy.db')


class ProxyList(Model):

    schema = CharField()
    proxy = CharField()

    class Meta:
        database = proxy_db
