from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QCheckBox, QLabel, QMessageBox, QInputDialog, QSizePolicy, QApplication
from PyQt5.QtCore import Qt, QSize, QDateTime
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from resources.icons import TablerIcons, OutlineIcon
from utils.encryption import load_data, save_data
from styles import load_stylesheet

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Management")

        self.items = load_data()

        # Ensure backward compatibility for existing data
        for item in self.items:
            if len(item) < 5:
                item.append("")  # Completed timestamp
                item.append(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm AP"))  # Added timestamp
                

        self.initUI()
        self.setStyleSheet(load_stylesheet())

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        # Add Titles and Descriptions for Tasks
        add_item_title = QLabel("Add Task")
        add_item_title.setObjectName("subtitle")
        main_layout.addWidget(add_item_title)
        
        add_item_description = QLabel("Add a task to your list.")
        add_item_description.setObjectName("description")
        main_layout.addWidget(add_item_description)

        entry_layout = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter a new task...")
        entry_layout.addWidget(self.entry)

        # Load plus icon
        BUTTON_ICON_SIZE = 18
        icon_plus = TablerIcons.load(OutlineIcon.PLUS, size=BUTTON_ICON_SIZE, color='#000', stroke_width=2.0)
        
        add_button = QPushButton()
        add_button.setIcon(QIcon(self.image_to_qpixmap(icon_plus)))
        add_button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        add_button.clicked.connect(self.add_item)
        entry_layout.addWidget(add_button)
        
        main_layout.addLayout(entry_layout)
        
        add_item_title = QLabel("Tasks")
        add_item_title.setObjectName("subtitle")
        main_layout.addWidget(add_item_title)
        
        add_item_description = QLabel("Check, prioritize, edit or delete your tasks.")
        add_item_description.setObjectName("description")
        main_layout.addWidget(add_item_description)

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        # Add Titles and Descriptions for Completed Tasks
        completed_item_title = QLabel("Completed Tasks")
        completed_item_title.setObjectName("subtitle")
        main_layout.addWidget(completed_item_title)
        
        completed_item_description = QLabel("Uncheck, prioritize, edit or delete your completed tasks.")
        completed_item_description.setObjectName("description")
        main_layout.addWidget(completed_item_description)

        self.completed_list_widget = QListWidget()
        main_layout.addWidget(self.completed_list_widget)

        self.update_list()

    def add_item(self):
        item_text = self.entry.text()
        if item_text:
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm AP")
            self.items.append(["0", item_text, "#233031", timestamp, ""])  # Default color, added timestamp, empty completed timestamp
            self.update_list()
            self.entry.clear()
            save_data(self.items)
        else:
            QMessageBox.warning(self, "Warning", "The text field is empty!")

    def edit_item(self, index):
        new_value, ok = QInputDialog.getText(self, "Edit", "New value:", QLineEdit.Normal, self.items[index][1])
        if ok and new_value:
            self.items[index][1] = new_value
            self.update_list()
            save_data(self.items)

    def delete_item(self, index):
        del self.items[index]
        self.update_list()
        save_data(self.items)

    def toggle_check(self, index):
        self.items[index][0] = "1" if self.items[index][0] == "0" else "0"
        if self.items[index][0] == "1":
            self.items[index][4] = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm AP")  # Completed timestamp
        else:
            self.items[index][4] = ""  # Clear completed timestamp
        self.update_list()
        save_data(self.items)

    def toggle_priority(self, index):
        colors = ["#233031", "#557258", "#E69B01", "#E95420"]
        current_color = self.items[index][2]
        if current_color not in colors:
            next_color = colors[0]
        else:
            next_color = colors[(colors.index(current_color) + 1) % len(colors)]
        self.items[index][2] = next_color
        self.update_list()
        save_data(self.items)

    def update_list(self):
        self.list_widget.clear()
        self.completed_list_widget.clear()
        
        for index, item in enumerate(self.items):
            if item[0] == "0":
                self.add_list_item(self.list_widget, index, item, item[3])
            else:
                self.add_list_item(self.completed_list_widget, index, item, item[4])

    def add_list_item(self, list_widget, index, item, timestamp):
        list_item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(item[0] == "1")
        checkbox.stateChanged.connect(lambda state, idx=index: self.toggle_check(idx))
        layout.addWidget(checkbox)

        label = QLabel(item[1])
        layout.addWidget(label)

        # Spacer to push buttons to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(spacer)

        # Timestamp label
        timestamp_label = QLabel(timestamp)
        timestamp_label.setFixedWidth(200)
        layout.addWidget(timestamp_label)

        # Load priority icon
        BUTTON_ICON_SIZE = 18
        icon_priority = TablerIcons.load(OutlineIcon.ADJUSTMENTS_COG, size=BUTTON_ICON_SIZE, color='#fff', stroke_width=1.5)

        priority_button = self.create_priority_button(item[2], index, icon_priority)
        layout.addWidget(priority_button)

        # Load edit icon
        icon_edit = TablerIcons.load(OutlineIcon.EDIT, size=BUTTON_ICON_SIZE, color='#000', stroke_width=1.5)
        
        edit_button = QPushButton()
        edit_button.setIcon(QIcon(self.image_to_qpixmap(icon_edit)))
        edit_button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        edit_button.clicked.connect(lambda _, idx=index: self.edit_item(idx))
        layout.addWidget(edit_button)

        # Load trash icon
        icon_trash = TablerIcons.load(OutlineIcon.TRASH, size=BUTTON_ICON_SIZE, color='#000', stroke_width=1.5)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon(self.image_to_qpixmap(icon_trash)))
        delete_button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        delete_button.clicked.connect(lambda _, idx=index: self.delete_item(idx))
        layout.addWidget(delete_button)

        widget.setLayout(layout)
        list_item.setSizeHint(widget.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, widget)

    def create_priority_button(self, color, index, icon_priority):
        BUTTON_ICON_SIZE = 18
        labels = {
            "#233031": "Low",
            "#557258": "Medium",
            "#E69B01": "High",
            "#E95420": "Urgent"
        }
        label_text = labels.get(color, "Low")
        priority_button = QPushButton(f"{label_text} ")
        priority_button.setIcon(QIcon(self.image_to_qpixmap(icon_priority)))
        priority_button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        priority_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                margin-right: 20px;
            }}
            QPushButton:hover {{
                background-color: #000;
            }}
        """)
        priority_button.setFixedWidth(120)
        priority_button.clicked.connect(lambda _, idx=index: self.toggle_priority(idx))
        return priority_button

    def image_to_qpixmap(self, image):
        q_image = QImage(image.tobytes('raw', 'RGBA'), image.width,
                        image.height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(q_image)

if __name__ == "__main__":
    app = QApplication([])
    window = TodoApp()
    window.showMaximized()
    app.exec_()
