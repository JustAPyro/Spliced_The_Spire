import sqlite3
from enum import Enum


class STATUS(Enum):
    UNHANDLED = 0


class BugType(Enum):
    UNIMPLEMENTED = 0


class BugArea(Enum):
    MONSTER = 0


class BugTracker:
    def __init__(self, db: str):
        self.connection = sqlite3.connect(db)
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS bugs (status TEXT, type TEXT, area TEXT, detail TEXT, lastoccurance TIME)")

        self.connection.commit()
        rows = cursor.execute("SELECT * FROM bugs").fetchall()
        cursor.close()
        print(rows)

    def file(self, type, area, name):
        cursor = self.connection.cursor()
        rows = cursor.execute(
            "SELECT * FROM bugs WHERE type = ? AND area = ?",
            ('UNIMPLEMENTED', 'MONSTER'),
        ).fetchall()

        print(len(rows))
        if len(rows) == 0:
            cursor.execute("INSERT INTO bugs VALUES ('UNHANDLED', ?, ?, ?)",
                           (str(type), str(area), name))
        self.connection.commit()


bt = BugTracker('bd.db')
bt.file(BugType.UNIMPLEMENTED, BugArea.MONSTER, 'Acid Slime (S)')
bt.file(BugType.UNIMPLEMENTED, BugArea.MONSTER, 'Spike Slime (M)')
