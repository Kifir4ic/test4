import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QMessageBox, QInputDialog, QHeaderView)

# DB setup
db = sqlite3.connect("notes.db")
cur = db.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        priority INTEGER
    )
""")

def setup_ui():
    win = QWidget()
    win.setWindowTitle("Заметки")
    win.resize(800, 500)

    layout = QVBoxLayout()
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["ID", "Текст", "Приоритет"])
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
    table.setColumnWidth(0, 50)
    table.setColumnWidth(2, 100)

    btn_layout = QHBoxLayout()
    buttons = [
        ("Добавить", self.add_note),
        ("Изменить", self.edit_note),
        ("Обновить", self.load_notes),
        ("Удалить", self.delete_note)
    ]

    for text, action in buttons:
        btn = QPushButton(text)
        btn.clicked.connect(action)
        btn_layout.addWidget(btn)

    layout.addWidget(table)
    layout.addLayout(btn_layout)
    win.setLayout(layout)

    # Привязка методов к виджетам
    win.table = table
    win.load_notes = load_notes
    win.add_note = add_note
    win.edit_note = edit_note
    win.delete_note = delete_note

    load_notes()
    return win

def load_notes():
    win = app.activeWindow()
    win.table.setRowCount(0)
    cur.execute("SELECT * FROM notes")
    for note in cur.fetchall():
        row = win.table.rowCount()
        win.table.insertRow(row)
        win.table.setItem(row, 0, QTableWidgetItem(str(note[0])))
        win.table.setItem(row, 1, QTableWidgetItem(note[1]))
        win.table.setItem(row, 2, QTableWidgetItem(str(note[2])))

def add_note():
    win = app.activeWindow()
    text, ok = QInputDialog.getText(win, "Добавить", "Текст заметки:")
    if ok and text:
        priority, ok = QInputDialog.getInt(win, "Приоритет", "1-5:", 1, 1, 5)
        if ok:
            cur.execute("INSERT INTO notes (text, priority) VALUES (?, ?)", (text, priority))
            db.commit()
            load_notes()

def edit_note():
    win = app.activeWindow()
    row = win.table.currentRow()
    if row == -1:
        QMessageBox.warning(win, "Ошибка", "Выберите заметку")
        return

    note_id = int(win.table.item(row, 0).text())
    old_text = win.table.item(row, 1).text()
    old_priority = int(win.table.item(row, 2).text())

    text, ok = QInputDialog.getText(win, "Изменить", "Текст:", text=old_text)
    if ok and text:
        priority, ok = QInputDialog.getInt(win, "Приоритет", "1-5:", old_priority, 1, 5)
        if ok:
            cur.execute("UPDATE notes SET text=?, priority=? WHERE id=?", (text, priority, note_id))
            db.commit()
            load_notes()

def delete_note():
    win = app.activeWindow()
    row = win.table.currentRow()
    if row == -1:
        QMessageBox.warning(win, "Ошибка", "Выберите заметку")
        return

    note_id = int(win.table.item(row, 0).text())
    cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
    db.commit()
    load_notes()

if name == "__main__":
    app = QApplication([])
    window = setup_ui()
    window.show()
    app.exec_()
