import traceback
import design
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from database import DataBase
import welcome

class WelcomeWindow(QtWidgets.QMainWindow, welcome.Ui_WelcomeWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.push_connect_button.clicked.connect(self.connect_to_database)

    def connect_to_database(self):
        try:
            self.app.connect(self.enter_database_line.text())
            self.close()
        except Exception as ex:
            print(traceback.format_exc())
            self.message("This database doesn't exist!", traceback.format_exc())

class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db = None
        self.setupUi(self)
        self.welcomeWindow = WelcomeWindow(self)
        self.columns_companies = ['name', 'email', 'last_release']
        self.columns_games = ['id', 'title', 'version', 'release', 'genre', 'author']

        # buttons
        self.add_company_button.clicked.connect(self.add_company_record)
        self.add_game_button.clicked.connect(self.add_game_record)
        self.games_delete_button.clicked.connect(self.delete_game)
        self.companies_search_button.clicked.connect(self.find_company_by_genre)
        self.games_search_button.clicked.connect(self.find_game_by_genre)

        # updates
        self.companies_table.itemChanged.connect(self.update_companies)
        self.games_table.itemChanged.connect(self.update_games)

        # actions
        self.connect_action.triggered.connect(self.welcomeWindow.show)
        self.drop_action.triggered.connect(self.delete_database)
        self.clear_companies_action.triggered.connect(self.clear_company)
        self.clear_games_action.triggered.connect(self.clear_game)
        self.clear_all_action.triggered.connect(self.clear_all)
        self.delete_record_action.triggered.connect(self.delete_record)

        self.companies_table.setColumnCount(3)
        self.companies_table.setHorizontalHeaderLabels(self.columns_companies)
        self.games_table.setColumnCount(6)
        self.games_table.setHorizontalHeaderLabels(self.columns_games)
        self.edited = False

    def connect(self, dbname):
        self.db = DataBase("myuser", "test", dbname)
        try:
            self.data_games = self.db.get_games()
            self.data_companies = self.db.get_companies()
            self.set_data(self.companies_table, self.columns_companies, self.data_companies)
            self.set_data(self.games_table, self.columns_games, self.data_games)
        except Exception as ex:
            print(traceback.format_exc())
            self.message("Connection error!", traceback.format_exc())

    def set_data(self, table, columns, data):
        self.edited = True
        try:
            if data is not None:
                table.setRowCount(len(data))
                for i, row in enumerate(data):
                    for j, col in enumerate(columns):
                        table.setItem(i, j, QTableWidgetItem(str(row[col])))
            else:
                table.setRowCount(0)
        except Exception as ex:
            self.message("Error during setting data!", traceback.format_exc())
        self.edited = False

    def message(self, error, detailed_error="Error", icon=QMessageBox.Warning):
        msg = QMessageBox()
        msg.setWindowTitle("Отчёт")
        msg.setIcon(icon)
        msg.setText(f"{error}")
        msg.setDetailedText(detailed_error)
        msg.addButton(QMessageBox.Ok)
        msg.exec()
    
    def add_game_record(self):
        try:
            title = self.game_title.text()
            version = self.game_version.text()
            release = self.game_release.text()
            genre = self.game_genre.text()
            author = self.game_author.text()

            if title != "" and version != "" and release != "" and genre != "" and author != "" and self.db is not None:
                self.db.new_game(title, version, release, genre, author)
                self.data_games = self.db.get_games()
                self.set_data(self.games_table, self.columns_games, self.data_games)
                self.game_title.clear()
                self.game_version.clear()
                self.game_release.clear()
                self.game_genre.clear()
                self.game_author.clear()
            else:
                self.message("Check if all fields are filled or if you have connected to db")
        except Exception as ex:
            self.message("Error during additing data!", traceback.format_exc())

    def add_company_record(self):
        try:
            name = self.company_name.text()
            email = self.company_email.text()
            release = self.company_release.text()
            if name != "" and email != "" and release != "" and self.db is not None:
                self.db.new_company(name, email, release)
                self.data_companies = self.db.get_companies()
                self.set_data(self.companies_table, self.columns_companies, self.data_companies)
                self.company_name.clear()
                self.company_email.clear()
                self.company_release.clear()
            else:
                self.message("Check if all fields are filled or if you have connected to db")

        except Exception as ex:
            print(traceback.format_exc())
            self.message("Error during additing data!", str(ex))        

    def clear_game(self):
        try:
            self.db.clear_games()
            self.data_games = self.db.get_games()
            self.set_data(self.games_table, self.columns_games, self.data_games)
        except Exception as ex:
            self.message("Error during clearing data!", traceback.format_exc())

    def clear_company(self):
        try:
            self.db.clear_companies()
            self.data_companies = self.db.get_companies()
            self.set_data(self.companies_table, self.columns_companies, self.data_companies)
        except Exception as ex:
            self.message("Error during clearing data!", traceback.format_exc())

    def clear_all(self):
        self.clear_game()
        self.clear_company()

    def delete_database(self):
        try:
            if self.db is not None:
                self.db.drop_database()
                self.message("Dropped database")
                self.data_companies = []
                self.data_games = []
                self.set_data(self.companies_table, self.columns_companies, self.data_companies)
                self.set_data(self.games_table, self.columns_games, self.data_games)
                self.db = None
                self.welcomeWindow.show()

            else:
                self.message("Check if you have connected to db")
        except Exception as ex:
            self.message("Error during deleting database!", traceback.format_exc())

    def delete_game(self):
        try:
            genre = self.games_genre_search.text()
            if genre != "" and self.db is not None:
                self.db.delete_game(genre)
                self.data_games = self.db.get_games()
                self.set_data(self.games_table, self.columns_games, self.data_games)
                self.games_genre_search.clear()
            else:
                self.message("Check if all fields are filled or if you have connected to db")
        except Exception as ex:
            self.message("Error during deleting data!", traceback.format_exc())

    def find_game_by_genre(self):
        try:
            genre = self.games_genre_search.text()

            if genre != "" and self.db is not None:
                self.set_data(self.games_table, self.columns_games, self.db.find_game(genre))
                self.games_genre_search.clear()
            else:
                self.set_data(self.games_table, self.columns_games, self.data_games)
        except Exception:
            self.message("Error during data search!", traceback.format_exc())

    def find_company_by_genre(self):
        try:
            genre = self.companies_genre_search.text()

            if genre != "" and self.db is not None:
                self.set_data(self.companies_table, self.columns_companies, self.db.find_company(genre))
                self.companies_genre_search.clear()
            else:
                self.set_data(self.companies_table, self.columns_companies, self.data_companies)
        except Exception:
            self.message("Error during data search!", traceback.format_exc())

    def update_games(self, item):
        if not self.edited:
            try:
                if item.column() == 1:
                    self.db.update_game_title(item.text(), self.games_table.item(item.row(), 0).text())
                elif item.column() == 2:
                    self.db.update_game_version(item.text(), self.games_table.item(item.row(), 0).text())
                elif item.column() == 3:
                    self.db.update_game_release(item.text(), self.games_table.item(item.row(), 0).text())
                elif item.column() == 4:
                    self.db.update_game_genre(item.text(), self.games_table.item(item.row(), 0).text())
                elif item.column() == 5:
                    self.db.update_game_author(item.text(), self.games_table.item(item.row(), 0).text())
                self.data_games = self.db.get_games()
                self.set_data(self.games_table, self.columns_games, self.data_games)
                self.data_companies = self.db.get_companies()
                self.set_data(self.companies_table, self.columns_companies, self.data_companies)
            except Exception:
                self.message("Error during data update!", traceback.format_exc())

    def update_companies(self, item):
        if not self.edited:
            try:
                if item.column() == 0:
                    self.db.update_company_name(item.text(), self.data_companies[item.row()]['name'])
                elif item.column() == 1:
                    self.db.update_company_email(item.text(), self.companies_table.item(item.row(), 0).text())
                elif item.column() == 2:
                    self.db.update_company_release(item.text(), self.companies_table.item(item.row(), 0).text())
                self.data_companies = self.db.get_companies()
                self.set_data(self.companies_table, self.columns_companies, self.data_companies)
                self.data_games = self.db.get_games()
                self.set_data(self.games_table, self.columns_games, self.data_games)
            except Exception:
                print(traceback.format_exc())
                self.message("Error during data update!", traceback.format_exc())

    def delete_record(self):
        if len(self.companies_table.selectedIndexes()):
            try:
                for i in self.companies_table.selectedIndexes():
                    self.db.delete_company_tuple(self.data_companies[i.row()]['name'])
                    self.data_companies = self.db.get_companies()
                    self.set_data(self.companies_table, self.columns_companies, self.data_companies)
            except Exception:
                self.message("Error during data delete!", traceback.format_exc())
        else:
            try:
                for i in self.games_table.selectedIndexes():
                    self.db.delete_game_tuple(self.data_games[i.row()]['id'] )
                    self.data_games = self.db.get_games()
                    self.set_data(self.games_table, self.columns_games, self.data_games)
            except Exception:
                self.message("Error during data delete!", traceback.format_exc())