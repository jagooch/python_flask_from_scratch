import sqlite3

posts = [
    {
        'author': 'Dova Kin',
        'title': 'First Post',
        'content': 'First post.',
        'date_posted': '20200301'
    },
    {
        'author': 'Angi\'s Cabin',
        'title': 'Second Post',
        'content': 'Second post.',
        'date_posted': '20200302'
    },
    {
        'author': 'Lydia Doorblocker',
        'title': 'Third Post',
        'content': 'I am sworn to carry your burdens.',
        'date_posted': '20200302'
    }
]

deletedb = """drop table if exists posts"""

createdb = """create table if not exists posts ( 
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date_posted TEXT NOT NULL
)
"""

insertdb = """ 
    insert into posts ( author, title, content, date_posted) values ( :author, :title, :content, :date_posted )
""" 

with sqlite3.connect("posts.db") as conn:
# with sqlite3.connect(":memory:") as conn:
    cursor = conn.cursor()
    cursor.execute( deletedb )
    cursor.execute( createdb )
    conn.commit()
    cursor.executemany( insertdb, posts   )
    conn.commit()
    cursor.execute("select * from posts")
    print(cursor.fetchall())

