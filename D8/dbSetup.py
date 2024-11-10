import sqlite3

conn = sqlite3.connect('dice.db')

cursor = conn.cursor()
#"""
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS rolls (
        rollNum INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        label INTEGER,
        confidence FLOAT,
        flagged BOOLEAN
    )
    '''
)
#"""
"""
inserts = [
    ('./images/PXL_20240806_223235913.MP.jpg', 0, 76.7, 0),
    ('./images/PXL_20240806_223237690.MP.jpg', 1, 40.5, 1),
    ('./images/PXL_20240806_223239233.MP.jpg', 1, 32.1, 1)
    ]
cursor.executemany(
    '''
    insert into rolls(path, label, confidence, flagged)
    values(?, ?, ?, ?)
    ''',
    inserts
)
"""
"""
cursor.execute('SELECT * FROM rolls')
rows = cursor.fetchall()

for row in rows:
    print(row)
""" 
conn.commit()
conn.close()