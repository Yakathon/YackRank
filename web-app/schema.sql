drop table if exists colleges;
create table colleges (
college_id integer primary key autoincrement,
latitude DOUBLE not null,
longitude DOUBLE not null,
name text not null
);

drop table if exists raw_yaks;
create table raw_yaks (
yak_id integer primary key autoincrement,
college_id integer not null,
yak_text text not null,
upvotes integer not null
);

drop table if exists most_valuable_words;
create table most_valuable_words (
college_id integer primary key not null,
word_text text not null
);