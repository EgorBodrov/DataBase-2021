import psycopg2 as ps
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DataBase:
    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name
        #self.engine = None
        #self.cursor = None
        self.connect_database("postgres")
        self.cursor.execute("SELECT * FROM pg_catalog.pg_database WHERE datname = %s", (self.db_name,))
        flag = self.cursor.fetchone()
        if flag is None:
            self.cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name)))
        self.engine.close()
        self.connect_database(self.db_name)
        if flag is None:
            self.cursor.execute(open("instructions.sql", "r").read())

    def connect_database(self, name):
        self.engine = ps.connect(dbname=name, user=self.user, password=self.password, host='localhost', port='5432')
        self.engine.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.engine.cursor()

    def create_database(self):
        self.cursor.callproc("create_database")

    def drop_database(self):
        self.connect_database("postgres")
        self.cursor.execute(sql.SQL(f"DROP DATABASE {self.db_name}"))
        self.engine.close()
        del self

    def get_companies(self):
        self.cursor.callproc("get_companies")
        return self.cursor.fetchone()[0]

    def get_games(self):
        self.cursor.callproc("get_games")
        return self.cursor.fetchone()[0]

    def new_company(self, name, email, release):
        self.cursor.callproc("new_company", (name, email, release, ))

    def new_game(self, title, version, release, genre, author):
        self.cursor.callproc("new_game", (title, version, release, genre, author, ))

    def clear_companies(self):
        self.cursor.callproc("clear_companies")

    def clear_games(self):
        self.cursor.callproc("clear_games")

    def clear_all(self):
        self.cursor.callproc("clear_companies")
        self.cursor.callproc("clear_games")

    def find_game(self, genre):
        self.cursor.callproc("find_game", (genre, ))
        return self.cursor.fetchone()[0]

    def find_company(self, genre):
        self.cursor.callproc("find_company", (genre, ))
        return self.cursor.fetchone()[0]

    def delete_game(self, genre):
        self.cursor.callproc("delete_game", (genre, ))

    def delete_game_tuple(self, id):
        self.cursor.callproc("delete_game_tuple", (id, ))

    def delete_company_tuple(self, name):
        self.cursor.callproc("delete_company_tuple", (name, ))

    def update_company_name(self, new_name, old_name):
        self.cursor.callproc("update_company_name", (new_name, old_name,))

    def update_company_email(self, email, name):
        self.cursor.callproc("update_company_email", (email, name, ))

    def update_game_title(self, new_title, id):
        self.cursor.callproc("update_game_title", (new_title, id, ))

    def update_game_version(self, new_version, id):
        self.cursor.callproc("update_game_version", (new_version, id, ))

    def update_game_release(self, new_release, id):
        self.cursor.callproc("update_game_release", (new_release, id, ))

    def update_game_genre(self, new_genre, id):
        self.cursor.callproc("update_game_genre", (new_genre, id, ))

    def update_game_author(self, new_author, id):
        self.cursor.callproc("update_game_author", (new_author, id, ))

    def close(self):
        self.engine.close()







