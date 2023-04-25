from consolemenu import *
from consolemenu.items import *
from zero import ZeroClient
from datetime import date
import time


zero_client = ZeroClient("localhost", 8888)


class RpcClient:
    def __init__(self, zero_client: ZeroClient):
        self._zero_client = zero_client

    def read_data(self, username):
        return self._zero_client.call("read_from_db", username)

    def write_data(self, data):
        return self._zero_client.call("post_train_data", data)

    def register(self, credentials):
        return self._zero_client.call("create_new_user", credentials)

    def login(self, credentials):
        return self._zero_client.call("authenticate", credentials)

    def edit(self, data):
        return self._zero_client.call("edit_train_data", data)

    def delete(self, info):
        return self._zero_client.call('delete_data', info)


def add_data(id):
    data = {
        'user_id': id,
        'pushups': input("Give the number of pushups you want to record: ")
    }
    print(rpc_client.write_data(data))


def edit_data(id):
    pass


def read_data(id):
    pass


def delete_data(id):
    user_id = input(
        "ID of the user whose data will be deleted (leave empty if you want to delete your own): ")
    if user_id.strip() == '':
        print(rpc_client.delete({'identifier': id, 'type': 'user'}))
        time.sleep(2)
    else:
        print(rpc_client.delete({'identifier': user_id, 'type': 'user'}))
        time.sleep(2)


def main_menu(user_id):
    menu = ConsoleMenu("Database interface", exit_option_text='Back to login')
    menu.append_item(FunctionItem("Add data", add_data, [user_id]))
    menu.append_item(FunctionItem("Edit data", edit_data, [user_id]))
    menu.append_item(FunctionItem("Read data", read_data, [user_id]))
    menu.append_item(FunctionItem("Delete data", delete_data, [user_id]))
    menu.show()
    time.sleep(20)


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
    if res["status"] == 1:
        print(res["msg"])
        time.sleep(2)
        return
    print(res['msg'])
    time.sleep(2)
    main_menu(res['id'])


def login_menu():
    menu = ConsoleMenu("SportClient v999")
    menu.append_item(FunctionItem("Log in", login))
    menu.append_item(FunctionItem("Register", register))
    menu.show()


if __name__ == "__main__":
    rpc_client = RpcClient(zero_client)
    login_menu()
