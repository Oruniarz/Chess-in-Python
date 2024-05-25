from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QDialog


class EndGameWindow(QDialog):
    def __init__(self, parent=None, result=None, winning_team=None):
        super().__init__(parent)
        self.winning_team = winning_team
        self.result = result
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Over')
        layout = QVBoxLayout()

        if self.result == "draw":
            final_label = QLabel("It's a draw!")
        elif self.result == "check mate":
            final_label = QLabel(f"Check mate! {self.winning_team.capitalize()} side wins!")
        layout.addWidget(final_label)
        exit_button = QPushButton('Ok', self)
        exit_button.clicked.connect(self.exit_app)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def exit_app(self):
        QApplication.instance().quit()

