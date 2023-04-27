from zero import ZeroServer
import sqlite3

# no hashing or salting lol


async def create_new_user(credentials: list[str]) -> str:
    query = 'insert into person (id, username, password) values(?,?,?)'
    try:
        cursor.execute(query, (None, credentials[0], credentials[1]))
        conn.commit()
        return 'Registering successful'
    except:
        return 'An error occured'


async def authenticate(credentials: list[str]) -> int:
    query = 'select id, username, password from person where username = ?'
    cursor.execute(query, (credentials['username'],))
    data = cursor.fetchone()
    if data[2] == credentials['password']:
        return {
            "msg": "Login successful",
            "id": data[0],
            "status": 0
        }
    else:
        return {
            "msg": "Authentication failed, please try again",
            "id": None,
            "status": 1
        }


async def post_train_data(data: dict[str | int]) -> str:
    query = '''insert into sports_data values (?, ?, ?, date())'''
    try:
        cursor.execute(
            query, (None, data['user_id'], data['pushups']))
        # conn.commit()
        cursor.execute(
            'insert into visualize_queue values (?, ?)', (None, data['user_id']))
        conn.commit()
        return 'Data added'
    except:
        return 'Data addition failed'


async def edit_train_data(data: dict[str | int]) -> str:
    query = '''
    update sports_data
    set pushups = ?
    where id = ?
    '''
    cursor.execute(query, (data['pushups'], data['id']))
    conn.commit()
    cursor.execute('select changes()')
    rows = cursor.fetchone()
    cursor.execute(
        'insert into visualize_queue values (?, ?)', (None, data['user_id']))
    conn.commit()
    return f'Data update successful, {rows[0]} rows affected'


async def read_from_db(username: str) -> list[str | int] or str:

    query = '''select pushups, submitdate
    from sports_data 
    where user = (
        select id from person where username = ?
    );
    '''
    try:
        cursor.execute(query, (username, ))
        data = cursor.fetchall()
        return data
    except:
        return 'Fetching data failed'


async def delete_data(data_info: dict[str | int]) -> str:
    query_type = data_info['type']
    queries = {
        'user': """
            delete from sports_data
            where user = ?
        """,
        'row': """
            delete from sports_data
            where id = ?
        """
    }
    try:
        cursor.execute(queries[query_type], (data_info['identifier'],))
        conn.commit()
        cursor.execute('select changes()')
        rows = cursor.fetchone()
        return f'{rows[0]} row(s) deleted successfully'
    except Exception as e:
        print(e.with_traceback())
        return 'Deletion failed'


if __name__ == "__main__":
    app = ZeroServer(port=8888)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    app.register_rpc(post_train_data)
    app.register_rpc(create_new_user)
    app.register_rpc(read_from_db)
    app.register_rpc(authenticate)
    app.register_rpc(delete_data)
    app.register_rpc(edit_train_data)
    app.run()
