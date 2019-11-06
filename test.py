import sys
import json
import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    # fill in dimension and general window variables
    def __init__(self):
        super().__init__()
        self.title = 'IEEE Espresso Machine'
        self.left = 200
        self.top = 200
        self.width = 300
        self.height = 400
        self.start_ui()

    # place window variables in UI
    def start_ui(self):
        # set window title
        self.setWindowTitle(self.title)

        # set window dimensions
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize LMU Logo
        self.logo = QLabel(self)
        self.pixmap = QPixmap('image.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.resize(self.pixmap.width(), self.pixmap.height())
        self.logo.move(110, 10)

        # # initialize returning user label
        # self.returning_user_label = QLabel(self)
        # self.returning_user_label.setText('Returning Users')
        # self.returning_user_label.move(50, 50)

        # initialize text field for all users
        self.text_input_user = QLineEdit(self)
        self.text_input_user.resize(100, 100)
        self.text_input_user.move(100, 130)

        # initialize brewing button, connect to turnOn method
        self.brew_button = QPushButton('Start Brewing!', self)
        self.brew_button.resize(150, 32)
        self.brew_button.move(75, 260)
        self.brew_button.clicked.connect(self.begin_brew)

        # initialize "please swipe your onecard" label
        self.swipe_card_label = QLabel(self)
        self.swipe_card_label.resize(300, 50)
        self.swipe_card_label.setText('Please swipe your OneCard')
        self.swipe_card_label.move(80, 90)

        # initialize brewing button, connect to turnOn method
        self.creation_button = QPushButton('Create New User', self)
        self.creation_button.resize(150, 32)
        self.creation_button.move(75, 300)
        self.creation_button.clicked.connect(self.create_user)

    # begin brew for returning users
    @pyqtSlot()
    def begin_brew(self):
        drinks = ('Espresso', 'Cappuccino', 'Latte')
        search_key = self.encode_card(self.text_input_user.text())

        with open('user_db.txt', 'r') as f:
            users = f.read()
        users_json = json.loads(users) if users else []

        contact = None
        for user in users_json:
            if user['card'] == search_key:
                contact = user
                break

        if contact == None:
            QMessageBox.critical(self, 'Error!', 'User Not Found, trying creating a new profile.', QMessageBox.Ok,
                                 QMessageBox.Ok)
        else:
            contact_name = contact['name']
            contact_coffee = drinks[contact['coffee'] - 1]
            QMessageBox.information(self, 'Hello, {}!'.format(contact_name.split(' ')[0]),
                                    'Hello {name}!\nOne {choice}, coming right up!'.format(name=contact_name,
                                                                                           choice=contact_coffee))
            # TODO: THIS IS WHERE WE SEND THE SIGNAL TO THE RELAY
        self.text_input_user.setText('')

    # create new user profile
    def create_user(self):
        self.new_user_card = self.text_input_user.text()

        name = QInputDialog.getText(self, 'Get Name', 'Enter Your Name:', QLineEdit.Normal, '')[0]
        drinks = ('Espresso', 'Cappuccino', 'Latte')
        drink_choice, ok_pressed = QInputDialog.getItem(self, "Get Drink", "Select Coffee Type:", drinks, 0, False)
        sizes = ('Small', 'Large')
        size_choice, ok_pressed = QInputDialog.getItem(self, "Get Size", "Select Size:", sizes, 0, False)
        if size_choice and drink_choice and ok_pressed:
            drinks_in_integer = drinks.index(drink_choice) + 1
            sizes_in_integer = sizes.index(size_choice) + 1
            self.save_user(name, drinks_in_integer, sizes_in_integer, self.encode_card(self.text_input_user.text()))
            self.text_input_user.setText('')
            QMessageBox.information(self, 'Success!', 'User Created!', QMessageBox.Ok, QMessageBox.Ok)

    # save new user profile to list of existing users
    def save_user(self, name, drink, size, card):
        json_profile = {'card': card, 'name': name, 'drink': drink, 'size': size}
        with open('user_db.txt', 'r') as f:
            users = f.read()

        with open('user_db.txt', 'w') as f:
            users_json = json.loads(users) if users else []
            users_json.append(json_profile)
            f.write(json.dumps(users_json))

    # hash card to store safely in users_db
    def encode_card(self, card):
        hash = hashlib.sha256(card.encode())
        return hash.hexdigest()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())