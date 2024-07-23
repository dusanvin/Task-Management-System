def load_stylesheet():
    return """
    * {
        font-family: 'Cantarell', sans-serif;
    }
    QMainWindow {
        background-color: #FAFAFA;
    }
    QLineEdit {
        background-color: #FFFFFF;
        color: #4A4A4A;
        border: 1px solid #FFFFFF;
        border-radius: 6px;
        padding: 5px;
    }
    QPushButton {
        background-color: #EEEEEE;
        color: #4A4A4A;
        border: 1px solid #EEEEEE;
        border-radius: 6px;
        padding: 5px;
        padding-left: 15px;
        padding-right: 15px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #FAFAFA;
    }
    QPushButton.priority:hover {
        background-color: #fff;
    }
    QListWidget {
        background-color: #FFFFFF;
        color: #4A4A4A;
        border-radius: 6px;
    }
    QListWidget::item:hover {
        background: #FFFFFF;
    }
    QListWidget::item:selected {
        background: #FFFFFF;
        color: #4A4A4A;
    }
    QListWidget::item:selected:focus {
        outline: none !important;
    }
    QListWidget::item:pressed {
        background: #0d0000 !important;
    }
    QCheckBox {
        color: #4A4A4A;
    }
    QLabel {
        color: #4A4A4A;
        border-bottom: 2px solid #1E1E1E;
    }
    QLabel#subtitle {
        font-size: 14px;
        font-weight: bold;
        margin-top: 20px;
    }
    QLabel#description {
        font-size: 12px;
        font-weight: normal;
        color: #4A4A4A;
        margin-bottom: 10px;
    }
    QMessageBox {
        background-color: #363636;
        color: #4A4A4A;
    }
    QInputDialog {
        background-color: #2E3440;
        color: #4A4A4A;
    }
    """
