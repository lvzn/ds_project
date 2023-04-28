from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
import sqlite3
import time
import os


class Visualizer:
    def __init__(self) -> None:
        self.count_of_rows = []
        pass

    def create_index(self):
        cursor.execute(
            'create index if not exists sports_user on sports_data(user)')
        cursor.execute(
            'create index if not exists person_user on person(username)')
        conn.commit()

    def create_folder(self):
        path = 'visualisations'
        if not os.path.exists(path):
            os.makedirs(path)

    def remove_index(self):
        cursor.execute('drop index sports_user')
        cursor.execute('drop index person_user')
        conn.commit()

    def check_updates(self):
        query = '''
            select distinct user from visualize_queue
        '''
        cursor.execute(query)
        users = cursor.fetchall()
        for user in users:
            cursor.execute(
                'delete from visualize_queue where user = ?', (user[0],))
        return users

    def visualize(self, user):
        pushups = []
        dates = []
        query = '''
            select pushups, submitdate from sports_data where user = ?
        '''
        cursor.execute(query, (user[0],))
        data = cursor.fetchall()
        for t in data:
            if t[1] in dates:
                pushups[len(pushups)-1] += t[0]
            else:
                pushups.append(t[0])
                dates.append(t[1])
        p = figure(x_range=dates, height=350, title="Pushups by date")
        p.vbar(x=dates, top=pushups, width=0.8)
        cursor.execute('select username from person where id = ?', (user[0],))
        username = cursor.fetchone()
        with open(f'visualisations/{username[0]}_graph.html', 'w') as f:
            f.write(
                file_html(p, CDN, f"user_{username[0]}_data"))

    def run(self):
        self.create_index()
        self.create_folder()
        updates = self.check_updates()
        if updates:
            for user in updates:
                self.visualize(user)
        self.remove_index()


if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    v = Visualizer()
    while True:
        v.run()
        time.sleep(15)
