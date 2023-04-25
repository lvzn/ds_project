from zero import ZeroServer
import sqlite3

# no hashing or salting lol


async def create_new_user(credentials: list[str]) -> str:
    query = 'insert into person (id, username, password) values(?,?,?)'
    cursor.execute(query, (None, credentials[0], credentials[1]))
    conn.commit()
    return 'Registering successful'


async def authenticate(credentials: list[str]) -> int:
    query = 'select id, username, password from person where username = ?'
    cursor.execute(query, (credentials['username']))
    data = cursor.fetchall()
    if data[2] == credentials['password']:
        return data[0]  # user id


async def post_train_data(data: list[str | int]) -> str:
    query = '''insert into sports_data values (?, ?, ?, ?)'''
    cursor.execute(
        query, (None, data['user_id'], data['pushups'], data['date']))
    conn.commit()
    return 'Data added'


async def read_from_db(username: str) -> list[str | int]:

    query = '''select pushups, submitdate
    from sports_data 
    where user = (
        select id from person where username = ?
    );
    '''
    cursor.execute(query, (username, ))
    data = cursor.fetchone()
    return data


def connect() -> sqlite3.Connection:
    return sqlite3.connect('database.db')


if __name__ == "__main__":
    app = ZeroServer(port=8888)
    conn = connect()
    cursor = conn.cursor()

    app.register_rpc(post_train_data)
    app.register_rpc(create_new_user)
    app.register_rpc(read_from_db)
    app.register_rpc(authenticate)
    app.run()
