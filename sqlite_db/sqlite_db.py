import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('mosfood.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(cls TEXT, name TEXT PRIMARY KEY, '
                 'img TEXT, price TEXT, ingridients TEXT)')


async def menu_add_position(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()
