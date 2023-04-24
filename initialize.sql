drop table if exists users;
CREATE table users(
    id integer primary key autoincrement,
    username text unique not null,
    password text --no authentication
);
DROP TABLE IF EXISTS sports_data;
CREATE TABLE sports_data(
    id integer primary key autoincrement,
    user int not null,
    pushups int not null,
    submitdate datetime not null,
    foreign key (user) references users (id)
);
insert into users
values (0, "admin", "admin")