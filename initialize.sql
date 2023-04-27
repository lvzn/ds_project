drop table if exists users;
CREATE table person(
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
    foreign key (user) references person (id)
);
create table visualize_queue(
    id integer primary key autoincrement,
    user int not null,
    foreign key (user) references person (id)
);
insert into person
values (0, "admin", "admin")