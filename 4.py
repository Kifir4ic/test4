import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QTextEdit, QPushButton, QFileDialog, QMessageBox, QInputDialog)

# DB setup
db = sqlite3.connect("test.db")
cur = db.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        priority INTEGER
    )
""")
try:
    cur.execute("INSERT INTO notes (id, text, priority) VALUES (1, 'sample', 1)")
    db.commit()
except sqlite3.IntegrityError:
    pass

def setup_ui():
    win = QWidget()
    win.setWindowTitle("Заметки")
    win.resize(600, 500)

    layout = QVBoxLayout()
    text_area = QTextEdit()

    buttons = [
        ("Создать", "lightgreen", lambda: create_note(text_area)),
        ("Открыть", "lightblue", lambda: open_note(text_area)),
        ("Сохранить", "lightyellow", lambda: save_note(text_area)),
        ("Добавить", "lightgrey", lambda: add_text(text_area))
    ]

    layout.addWidget(QLabel("Текст заметки:"))
    layout.addWidget(text_area)
    
    for text, color, action in buttons:
        btn = QPushButton(text)
        btn.setStyleSheet(f"background-color: {color};")
        btn.clicked.connect(action)
        layout.addWidget(btn)

    win.setLayout(layout)
    return win

def create_note(editor):
    file, _ = QFileDialog.getSaveFileName(None, "Создать", "", "*.txt")
    if file:
        save_to_file(editor, file)

def open_note(editor):
    file, _ = QFileDialog.getOpenFileName(None, "Открыть", "", "*.txt")
    if file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                editor.setText(f.read())
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", str(e))

def save_note(editor):
    name, ok = QInputDialog.getText(None, "Сохранить", "Имя файла:")
    if ok and name:
        save_to_file(editor, f"{name}.txt")

def save_to_file(editor, file):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())
        QMessageBox.information(None, "Успех", "Сохранено!")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", str(e))

def add_text(editor):
    text, ok = QInputDialog.getText(None, "Добавить", "Текст:")
    if ok and text:
        editor.append(text)

if name == "__main__":
    app = QApplication([])
    window = setup_ui()
    window.show()
    app.exec_()
