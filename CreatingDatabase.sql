CREATE DATABASE FlightReservationSystem;
GO
    
USE FlightReservationSystem;
GO

----------------------------------------------------
-- COUNTRIES
----------------------------------------------------
CREATE TABLE Countries (
    CountryID INT IDENTITY PRIMARY KEY,
    CountryName VARCHAR(100) NOT NULL
);

----------------------------------------------------
-- CITIES
----------------------------------------------------
CREATE TABLE Cities (
    CityID INT IDENTITY PRIMARY KEY,
    CityName VARCHAR(100) NOT NULL,
    CountryID INT NOT NULL,
    FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
);

----------------------------------------------------
-- AIRPORT
----------------------------------------------------
CREATE TABLE Airport (
    AirportID INT IDENTITY PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    CityID INT NOT NULL,
    Code CHAR(3) NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID)
);

----------------------------------------------------
-- AIRCRAFT
----------------------------------------------------
CREATE TABLE Aircraft (
    AircraftID INT IDENTITY PRIMARY KEY,
    AircraftName VARCHAR(100),
    Capacity INT,
    Status VARCHAR(20)
);

----------------------------------------------------
-- FLIGHT
----------------------------------------------------
CREATE TABLE Flight (
    FlightID INT IDENTITY PRIMARY KEY,
    FlightNumber VARCHAR(20) NOT NULL,
    AircraftID INT NOT NULL,
    DepartureAirportID INT NOT NULL,
    ArrivalAirportID INT NOT NULL,
    BaseFare DECIMAL(10,2),
    FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID),
    FOREIGN KEY (DepartureAirportID) REFERENCES Airport(AirportID),
    FOREIGN KEY (ArrivalAirportID) REFERENCES Airport(AirportID)
);

----------------------------------------------------
-- FLIGHT SCHEDULE
----------------------------------------------------
CREATE TABLE FlightSchedule (
    ScheduleID INT IDENTITY PRIMARY KEY,
    FlightID INT NOT NULL,
    DepartureDate DATE,
    DepartureTime TIME,
    ArrivalDate DATE,
    ArrivalTime TIME,
    Duration INT,
    Status VARCHAR(20),
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
);

----------------------------------------------------
-- ADMIN
----------------------------------------------------
CREATE TABLE Admin (
    AdminID INT IDENTITY PRIMARY KEY,
    Username VARCHAR(50),
    [Password] VARCHAR(50),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Position VARCHAR(50)
);

----------------------------------------------------
-- FLIGHT STATUS LOG
----------------------------------------------------
CREATE TABLE FlightStatusLog (
    LogID INT IDENTITY PRIMARY KEY,
    ScheduleID INT,
    AdminID INT,
    OldStatus VARCHAR(20),
    NewStatus VARCHAR(20),
    UpdatedAt DATETIME,
    Remarks VARCHAR(255),
    FOREIGN KEY (ScheduleID) REFERENCES FlightSchedule(ScheduleID),
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
);

----------------------------------------------------
-- USER
----------------------------------------------------
CREATE TABLE [User] (
    UserID INT IDENTITY PRIMARY KEY,
    [Password] VARCHAR(50),
    Gender CHAR(1),
    PassportNumber VARCHAR(20),
    Email VARCHAR(100),
    PostalAddress VARCHAR(255),
    CountryID INT,
    CityID INT,
    Nationality VARCHAR(50),
    Age INT,
    PhoneNumber VARCHAR(20),
    FOREIGN KEY (CountryID) REFERENCES Countries(CountryID),
    FOREIGN KEY (CityID) REFERENCES Cities(CityID)
);

----------------------------------------------------
-- CLASS
----------------------------------------------------
CREATE TABLE Class (
    ClassID INT IDENTITY PRIMARY KEY,
    ClassName VARCHAR(50),
    ClassMultiplier DECIMAL(4,2)
);

----------------------------------------------------
-- SEAT TYPE
----------------------------------------------------
CREATE TABLE SeatType (
    SeatTypeID INT IDENTITY PRIMARY KEY,
    SeatTypeName VARCHAR(50),
    ExtraCost DECIMAL(10,2)
);

----------------------------------------------------
-- MEAL TYPE
----------------------------------------------------
CREATE TABLE MealType (
    MealTypeID INT IDENTITY PRIMARY KEY,
    MealTypeName VARCHAR(50),
    ExtraCost DECIMAL(10,2)
);

----------------------------------------------------
-- FLIGHT TYPE
----------------------------------------------------
CREATE TABLE FlightType (
    FlightTypeID INT IDENTITY PRIMARY KEY,
    FlightTypeName VARCHAR(50)
);

----------------------------------------------------
-- FC OPTION
----------------------------------------------------
CREATE TABLE FCOption (
    FCOptionID INT IDENTITY PRIMARY KEY,
    FCOptionName VARCHAR(100),
    Description VARCHAR(255),
    ExtraCost DECIMAL(10,2)
);

----------------------------------------------------
-- BOOKING
----------------------------------------------------
CREATE TABLE Booking (
    BookingID INT IDENTITY PRIMARY KEY,
    UserID INT,
    ScheduleID INT,
    ClassID INT,
    FlightTypeID INT,
    SeatTypeID INT,
    MealTypeID INT,
    BookingDate DATETIME,
    TotalPrice DECIMAL(10,2),
    Status VARCHAR(20),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (ScheduleID) REFERENCES FlightSchedule(ScheduleID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID),
    FOREIGN KEY (FlightTypeID) REFERENCES FlightType(FlightTypeID),
    FOREIGN KEY (SeatTypeID) REFERENCES SeatType(SeatTypeID),
    FOREIGN KEY (MealTypeID) REFERENCES MealType(MealTypeID)
);

----------------------------------------------------
-- BOOKING FC OPTION (JUNCTION)
----------------------------------------------------
CREATE TABLE BookingFCOption (
    BookingID INT,
    FCOptionID INT,
    PRIMARY KEY (BookingID, FCOptionID),
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
    FOREIGN KEY (FCOptionID) REFERENCES FCOption(FCOptionID)
);

----------------------------------------------------
-- FLIGHT CLASS (JUNCTION)
----------------------------------------------------
CREATE TABLE FlightClass (
    FlightID INT,
    ClassID INT,
    PRIMARY KEY (FlightID, ClassID),
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

----------------------------------------------------
-- ADMIN FLIGHT CONTROL
----------------------------------------------------
CREATE TABLE AdminFlightControl (
    AdminID INT,
    FlightID INT,
    PRIMARY KEY (AdminID, FlightID),
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID),
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
);

----------------------------------------------------
-- LAYOVER
----------------------------------------------------
CREATE TABLE LayOver (
    LayoverID INT IDENTITY PRIMARY KEY,
    FlightID_1 INT,
    FlightID_2 INT,
    LayoverCityID INT,
    LayoverDuration INT,
    FOREIGN KEY (FlightID_1) REFERENCES Flight(FlightID),
    FOREIGN KEY (FlightID_2) REFERENCES Flight(FlightID),
    FOREIGN KEY (LayoverCityID) REFERENCES Cities(CityID)
);

