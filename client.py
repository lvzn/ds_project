from consolemenu import *
from consolemenu.items import *
from zero import ZeroClient


zero_client = ZeroClient("localhost", 8888)


class RpcClient:
    def __init__(self, zero_client: ZeroClient):
        self._zero_client = zero_client

    def read_data(self, username):
        return self._zero_client.call("read_from_db", username)

    def hello_world(self):
        return self._zero_client.call("hello_world", None)

    def register(self, credentials):
        return self._zero_client.call("create_new_user", credentials)

    def login(self, credentials):
        return self._zero_client.call("authenticate", credentials)


def main_menu(user_id):
    pass
    # TODO: main functionality


def register():
    username = input("Give desired username: ")
    password = input("Give desired password: ")
    credentials = [username, password]
    print(rpc_client.register(credentials))
    return


def login():
    credentials = {
        'username': input("Username: "),
        'password': input("Password: ")
    }
    res = rpc_client.login(credentials)
    print(res['msg'])
    main_menu(res['id'])


def login_menu():
    menu = ConsoleMenu("SportClient v999")
    menu.append_item(FunctionItem("Log in", login))
    menu.append_item(FunctionItem("Register", register))
    menu.show()


if __name__ == "__main__":
    rpc_client = RpcClient(zero_client)
    login_menu()
