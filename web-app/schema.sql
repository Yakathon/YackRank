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

drop table if exists top_yaks;
create table top_yaks (
college_id integer primary key not null,
yak_text text not null
);

drop table if exists college_readability;
create table college_readability (
college_id integer primary key not null,
average_readability DOUBLE not null
);

drop table if exists college_grade_level;
create table college_grade_level (
college_id integer primary key not null,
average_grade_level DOUBLE
);

drop table if exists num_yaks;
create table num_yaks(
college_id integer primary key not null,
yaks integer not null);


drop table if exists times_swore;
create table times_swore (
college_id integer primary key not null,
times_swore DOUBLE not null
);
