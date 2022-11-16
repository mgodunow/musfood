import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('musfood.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(tip TEXT,cls TEXT, name TEXT PRIMARY KEY, '
                 'img TEXT, price TEXT, ingridients TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS drinks(tip TEXT,cls TEXT, name TEXT PRIMARY KEY, '
                 'img TEXT, price TEXT, ingridients TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS sale(img TEXT, name TEXT PRIMARY KEY, desc TEXT)')


async def menu_add_position(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def drinks_add_position(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO drinks VALUES(?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sale_add_position(state):
    async with state.proxy() as note:
        cur.execute('INSERT INTO sale VALUES(?, ?, ?)', tuple(note.values()))
        base.commit()


async def read_menu_class():
    return cur.execute('SELECT DISTINCT cls FROM menu').fetchall()


async def read_menu_list(data):
    return cur.execute('SELECT * FROM menu WHERE cls == ?', (data,))


async def read_drinks_class():
    return cur.execute('SELECT DISTINCT cls FROM drinks').fetchall()


async def read_drinks_list(data):
    return cur.execute('SELECT * FROM drinks WHERE cls == ?', (data,))


async def read_sale():
    return cur.execute('SELECT * FROM sale').fetchall()


async def delete_command_menu(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (str(data),))
    base.commit()


async def delete_command_sale(data):
    cur.execute('DELETE FROM sale WHERE name == ?', (str(data),))
    base.commit()


async def delete_command_drinks(data):
    cur.execute('DELETE FROM drinks WHERE name == ?', (str(data),))
    base.commit()
