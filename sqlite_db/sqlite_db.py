import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('mosfood.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(tip TEXT,cls TEXT, name TEXT PRIMARY KEY, '
                 'img TEXT, price TEXT, ingridients TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS drinks(tip TEXT,cls TEXT, name TEXT PRIMARY KEY, '
                 'img TEXT, price TEXT, ingridients TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS sale(img TEXT, name TEXT PRIMARY KEY)')


async def menu_add_position(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Здесб должна быть read1
async def read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
