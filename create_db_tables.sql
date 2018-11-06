use c4g;
create table cell (cellid int Not Null PRIMARY KEY AUTO_INCREMENT, x int Not Null, y int Not Null, z int Not Null, has_streetsign int, is_street int);
create table streetsign (cellid int Not Null, timestep int Not Null, open int, CONSTRAINT PK_streetsign PRIMARY KEY (cellid, timestep), CONSTRAINT FK_sign_cellid FOREIGN KEY (cellid) REFERENCES cell(cellid));
create table celldata (cellid int NOT NULL, timestep int NOT NULL, light decimal(15,4), noise decimal(15,4), number_of_cars int, CONSTRAINT PK_celldata PRIMARY KEY(cellid, timestep), CONSTRAINT FK_data_cellid FOREIGN KEY(cellid) REFERENCES cell(cellid));
