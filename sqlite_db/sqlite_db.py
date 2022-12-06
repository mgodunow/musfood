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
    base.execute('CREATE TABLE IF NOT EXISTS cart(user_id, product TEXT, price TEXT)')


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


async def select_cart(user_id):
    return cur.execute('SELECT product, price FROM cart WHERE user_id == ?', (user_id,)).fetchall()


async def select_price_cart(user_id, product):
    return cur.execute('SELECT price FROM cart WHERE user_id == ? and product == ?', [user_id, product])


async def to_cart(user_id, cart, price):
    cur.execute('INSERT INTO cart VALUES(?,?,?)', [user_id, cart, price])
    base.commit()


async def delete_user_cart(user_id, product):
    product = cur.execute('SELECT rowid FROM cart WHERE user_id == ? AND product == ? LIMIT 1', (int(user_id),
                                                                                                 product)).fetchall()
    print(product[0])
    cur.execute('DELETE FROM cart WHERE rowid == ?', product[0])
    base.commit()


async def delete_cart(user_id):
    cur.execute('DELETE FROM cart WHERE user_id == ?', (int(user_id),))
    base.commit()