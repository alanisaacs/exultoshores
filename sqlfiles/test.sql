CREATE TABLE backlog (
    id serial PRIMARY KEY,
    category VARCHAR (255),
    title VARCHAR (255),
    notes VARCHAR (1023),
    rank INT,
    severity INT,
    priority INT,
    status VARCHAR (40)
);