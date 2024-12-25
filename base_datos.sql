
create database empresa;
use empresa

CREATE TABLE Constructoras (
    idConstructora VARCHAR(10) NOT NULL PRIMARY KEY,
    fono VARCHAR(15),
    email VARCHAR(30)
) ENGINE=InnoDB;

CREATE TABLE Obras (
    codigoObra VARCHAR(10) NOT NULL PRIMARY KEY,
    idConstructora VARCHAR(10) NOT NULL,
    descripcionObra VARCHAR(20),
    costo INT,
    fechaInicio DATE,
    FOREIGN KEY (idConstructora) REFERENCES Constructoras(idConstructora)
) ENGINE=InnoDB;

CREATE TABLE USUARIOS(
	nombre varchar(20),
	password varchar(32)
) ENGINE=InnoDB;


insert into Constructoras values('t100','+56912321579','inacap@gmail.com');
insert into Constructoras values('t200','+56965781689','carlitos@gmail.com');
insert into Constructoras values('t300','+56912454789','santamaria@gmail.com');

insert into Obras values('800','t100','Poblacion costanera',900000,'2023/8/20');
insert into Obras values('900','t200','Puente Llacolen',500000,'2023/8/24');
insert into Obras values('700','t300','Edificio Los Rios',600000,'2024/9/3');
