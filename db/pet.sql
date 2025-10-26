# 데이터베이스 사용
USE new_schema;

# PetOwners 테이블 생성
CREATE TABLE PetOwners(
	name VARCHAR(30) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    ownerID VARCHAR(45) PRIMARY KEY
);

# pets 테이블 생성
CREATE TABLE pets(
	name VARCHAR(15) NOT NULL,
    petID VARCHAR(45) PRIMARY KEY,
    species VARCHAR(20),
    breed VARCHAR(45) NOT NULL,
    ownerID VARCHAR(45),
    FOREIGN KEY (ownerID) REFERENCES PetOwners(ownerID)
);
    
# Rooms 테이블 생성
CREATE TABLE Rooms(
	roomID VARCHAR(30) PRIMARY KEY,
    roomNumber INT NOT NULL,
    roomType VARCHAR(45) NOT NULL,
    pricePerNight INT NOT NULL
);
    
# Reservations 테이블 생성
CREATE TABLE Reservations(
	reservationID VARCHAR(15) PRIMARY KEY,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    petID VARCHAR(45) NOT NULL,
    roomID VARCHAR(30) NOT NULL,
    FOREIGN KEY (petID) REFERENCES Pets(petID),
    FOREIGN KEY (roomID) REFERENCES Rooms(roomID)
);

# Services 테이블 생성
CREATE TABLE Services(
	serviceID VARCHAR(30) PRIMARY KEY,
    serviceName VARCHAR(45) NOT NULL,
    servicePrice INT NOT NULL,
    reservationID VARCHAR(15),
    FOREIGN KEY (reservationID) REFERENCES Reservations(reservationID)
);




















