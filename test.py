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
        self.drinks = ('Espresso', 'Cappuccino', 'Latte')
        self.sizes = ('Small', 'Large')
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

        # initialize the usual button, connect to turnOn method
        self.usual_button = QPushButton('the usual', self)
        self.usual_button.resize(75, 45)
        self.usual_button.move(175, 260)
        self.usual_button.clicked.connect(self.begin_brew)

        # initialize switch it up button, connect to turnOn method
        self.switch_it_up_button = QPushButton('switch it up', self)
        self.switch_it_up_button.resize(75, 45)
        self.switch_it_up_button.move(50, 260)
        self.switch_it_up_button.clicked.connect(self.new_brew)

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
            contact_drink = self.drinks[contact['drink'] - 1]
            contact_size = self.drinks[contact['size'] - 1]
            QMessageBox.information(self, 'Hello, {}!'.format(contact_name.split(' ')[0]),
                                    'Hello {name}!\nOne {size} {choice}, coming right up!'.format(name=contact_name, size=contact_size,
                                                                                           choice=contact_drink))
            # TODO: THIS IS WHERE WE SEND THE SIGNAL TO THE RELAY
        self.text_input_user.setText('')

    # create new user profile
    def create_user(self):
        self.new_user_card = self.text_input_user.text()
        name = QInputDialog.getText(self, 'Get Name', 'Enter Your Name:', QLineEdit.Normal, '')[0]
        user_choice = self.choosing_stage()

        if user_choice['size_choice'] and user_choice['drink_choice'] and user_choice['ok_pressed']:
            drinks_in_integer = self.drinks.index(user_choice['drink_choice']) + 1
            sizes_in_integer = self.sizes.index(user_choice['size_choice']) + 1
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

    # method to prompt user for drink and size choice
    def choosing_stage(self):
        drink_choice, ok_pressed = QInputDialog.getItem(self, "Get Drink", "Select Coffee Type:", self.drinks, 0, False)
        size_choice, ok_pressed = QInputDialog.getItem(self, "Get Size", "Select Size:", self.sizes, 0, False)
        result_dict = {'drink_choice' : drink_choice, 'size_choice' : size_choice, 'ok_pressed' : ok_pressed}
        return result_dict

    def new_brew(self):
        result_dict = self.choosing_stage()
        if result_dict['ok_pressed']:
            QMessageBox.information(self, 'options changed', 'Sure!\nOne {size} {choice}, coming right up!'.format(size=result_dict['size_choice'], 
            choice=result_dict['drink_choice']))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())