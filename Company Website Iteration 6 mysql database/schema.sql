
--creating and adding sales to the sales table as well as the queries needed for this assignment
---------------------------------------------------------------------------------------------------------
create table sales (
    id int auto_increment,
    startTime timestamp not null default CURRENT_TIMESTAMP,
    content text not null,
    endTime timestamp default null,
    primary key (id)
);


----------------------------------------------------------------------------------------------------------



--creating a table for contacts
----------------------------------------------------------------------------------------------------------
create table contacts (
    id int auto_increment,
    username text not null,
    email text not null,
    birthday text not null,
    news text not null, 
    rumors Boolean default false,
    primary key (id)
);

----------------------------------------------------------------------------------------------------------