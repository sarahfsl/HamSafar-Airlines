USE test;
GO


----------------------------------------------------
-- COUNTRIES
----------------------------------------------------

SET IDENTITY_INSERT Countries ON;
INSERT INTO Countries (CountryID, CountryName) VALUES
(1, 'Pakistan'),
(2, 'UAE'),
(3, 'Turkey'),
(4, 'Saudi Arabia'),
(5, 'United Kingdom'),
(6, 'France'),
(7, 'Spain'),
(8, 'United States'),
(9, 'China'),
(10, 'Italy'),
(11, 'Mexico'),
(12, 'Thailand'),
(13, 'Germany'),
(14, 'Japan'),
(15, 'Austria'),
(16, 'Greece'),
(17, 'Malaysia'),
(18, 'Russia'),
(19, 'Portugal'),
(20, 'Canada'),
(21, 'Netherlands'),
(22, 'Poland'),
(23, 'South Korea'),
(24, 'Croatia'),
(25, 'India'),
(26, 'Vietnam'),
(27, 'Hungary');
SET IDENTITY_INSERT Countries OFF;
----------------------------------------------------
-- CITIES
----------------------------------------------------
SET IDENTITY_INSERT Cities ON;
INSERT INTO Cities (CityID, CityName, CountryID) VALUES
(1, 'Karachi', 1),
(2, 'Lahore', 1),
(3, 'Dubai', 2),
(4, 'Istanbul', 3),
(5, 'Riyadh', 4),
(6, 'Jeddah', 4),
(7, 'London', 5),
(8, 'Manchester', 5),
(9, 'Sharjah', 2),
(10, 'Ankara', 3);
SET IDENTITY_INSERT Cities OFF;
----------------------------------------------------
-- AIRPORTS
----------------------------------------------------
SET IDENTITY_INSERT Airport ON;
INSERT INTO Airport (AirportID, Name, CityID, Code) VALUES
(1, 'Jinnah International Airport', 1, 'KHI'),
(2, 'Allama Iqbal Airport', 2, 'LHE'),
(3, 'Dubai International Airport', 3, 'DXB'),
(4, 'Istanbul Airport', 4, 'IST'),
(5, 'King Khalid Airport', 5, 'RUH'),
(6, 'King Abdulaziz Airport', 6, 'JED'),
(7, 'Heathrow Airport', 7, 'LHR'),
(8, 'Manchester Airport', 8, 'MAN'),
(9, 'Sharjah International Airport', 9, 'SHJ'),
(10, 'Esenboga Airport', 10, 'ESB');
SET IDENTITY_INSERT Airport OFF;
----------------------------------------------------
-- AIRCRAFT
----------------------------------------------------
SET IDENTITY_INSERT Aircraft ON;
INSERT INTO Aircraft (AircraftID, AircraftName, Capacity, Status) VALUES
(1, 'Boeing 777', 300, 'ongoing'),
(2, 'Airbus A320', 180, 'ongoing'),
(3, 'Boeing 787', 250, 'cancelled'),
(4, 'Airbus A350', 280, 'ongoing'),
(5, 'Boeing 737', 160, 'ongoing'),
(6, 'Airbus A321', 200, 'ongoing'),
(7, 'Boeing 767', 220, 'ongoing'),
(8, 'Boeing 747', 400, 'ongoing'),
(9, 'Airbus A330', 260, 'ongoing'),
(10, 'Boeing 757', 210, 'ongoing');
SET IDENTITY_INSERT Aircraft OFF;
----------------------------------------------------
-- FLIGHTS (10 Routes)
----------------------------------------------------
SET IDENTITY_INSERT Flight ON;
INSERT INTO Flight (FlightID, FlightNumber, AircraftID, DepartureAirportID, ArrivalAirportID, BaseFare) VALUES
(1, 'PK201', 1, 1, 2, 150.00),   -- Karachi to Lahore
(2, 'PK202', 2, 1, 3, 300.00),   -- Karachi to Dubai
(3, 'PK203', 3, 2, 3, 280.00),   -- Lahore to Dubai
(4, 'PK204', 4, 3, 4, 400.00),   -- Dubai to Istanbul
(5, 'PK205', 5, 4, 5, 350.00),   -- Istanbul to Riyadh
(6, 'PK206', 6, 5, 6, 120.00),   -- Riyadh to Jeddah
(7, 'PK207', 7, 6, 7, 500.00),   -- Jeddah to London
(8, 'PK208', 8, 7, 8, 100.00),   -- London to Manchester
(9, 'PK209', 9, 8, 9, 450.00),   -- Manchester to Sharjah
(10, 'PK210', 10, 9, 10, 250.00); -- Sharjah to Ankara
SET IDENTITY_INSERT Flight OFF;
----------------------------------------------------
-- FLIGHT SCHEDULE (10 Schedules)
----------------------------------------------------
SET IDENTITY_INSERT FlightSchedule ON;
INSERT INTO FlightSchedule (ScheduleID, FlightID, DepartureDate, DepartureTime, ArrivalDate, ArrivalTime, Duration, Status) VALUES
(1, 1, '2025-11-15', '08:00', '2025-11-15', '09:15', 75, 'scheduled'),
(2, 2, '2025-11-15', '12:00', '2025-11-15', '14:30', 150, 'scheduled'),
(3, 3, '2025-11-15', '16:00', '2025-11-15', '18:15', 135, 'scheduled'),
(4, 4, '2025-11-16', '07:30', '2025-11-16', '10:15', 165, 'scheduled'),
(5, 5, '2025-11-16', '13:00', '2025-11-16', '15:30', 150, 'scheduled'),
(6, 6, '2025-11-17', '10:00', '2025-11-17', '11:20', 80, 'scheduled'),
(7, 7, '2025-11-17', '17:45', '2025-11-17', '21:15', 210, 'scheduled'),
(8, 8, '2025-11-18', '09:00', '2025-11-18', '10:10', 70, 'scheduled'),
(9, 9, '2025-11-18', '14:20', '2025-11-18', '16:50', 150, 'scheduled'),
(10, 10, '2025-11-19', '19:00', '2025-11-19', '21:10', 130, 'scheduled');
SET IDENTITY_INSERT FlightSchedule OFF;
----------------------------------------------------
-- ADMINS
----------------------------------------------------
SET IDENTITY_INSERT Admin ON;
INSERT INTO Admin (AdminID, Username, [Password], Email, PhoneNumber, Position) VALUES
(1, 'admin01', 'pass01', 'admin01@flightsystem.com', '03001234567', 'Manager'),
(2, 'admin02', 'pass02', 'admin02@flightsystem.com', '03007654321', 'Supervisor');
SET IDENTITY_INSERT Admin OFF;
----------------------------------------------------
-- FLIGHT STATUS LOG
----------------------------------------------------
SET IDENTITY_INSERT FlightStatusLog ON;
INSERT INTO FlightStatusLog (LogID, ScheduleID, AdminID, OldStatus, NewStatus, UpdatedAt, Remarks) VALUES
(1, 1, 1, 'scheduled', 'scheduled', GETDATE(), 'Initial entry'),
(2, 2, 1, 'scheduled', 'scheduled', GETDATE(), 'Initial entry'),
(3, 5, 2, 'scheduled', 'scheduled', GETDATE(), 'Initial entry');
SET IDENTITY_INSERT FlightStatusLog OFF;
----------------------------------------------------
-- USERS
----------------------------------------------------
SET IDENTITY_INSERT [User] ON;
INSERT INTO [User] (UserID, [Password], Gender, PassportNumber, Email, PostalAddress, CountryID, CityID, Nationality, Age, PhoneNumber) VALUES
(1, 'user01', 'M', 'P12345', 'user1@email.com', 'Street 12 Karachi', 1, 1, 'Pakistani', 28, '03001122334'),
(2, 'user02', 'F', 'P54321', 'user2@email.com', 'Model Town Lahore', 1, 2, 'Pakistani', 25, '03004455667'),
(3, 'user03', 'M', 'U11223', 'user3@email.com', 'Dubai Marina', 2, 3, 'Emirati', 32, '0501234567'),
(4, 'user04', 'F', 'T44556', 'user4@email.com', 'Besiktas Istanbul', 3, 4, 'Turkish', 30, '05321234567'),
(5, 'user05', 'M', 'S77889', 'user5@email.com', 'Riyadh Center', 4, 5, 'Saudi', 35, '0551234567');
SET IDENTITY_INSERT [User] OFF;
----------------------------------------------------
-- CLASS
----------------------------------------------------
SET IDENTITY_INSERT Class ON;
INSERT INTO Class (ClassID, ClassName, ClassMultiplier) VALUES
(1, 'Economy', 1.0),
(2, 'Business', 1.5),
(3, 'First', 2.0);
SET IDENTITY_INSERT Class OFF;
----------------------------------------------------
-- SEAT TYPE
----------------------------------------------------
SET IDENTITY_INSERT SeatType ON;
INSERT INTO SeatType (SeatTypeID, SeatTypeName, ExtraCost) VALUES
(1, 'Window', 20),
(2, 'Aisle', 10),
(3, 'Middle', 0);
SET IDENTITY_INSERT SeatType OFF;
----------------------------------------------------
-- MEAL TYPE
----------------------------------------------------
SET IDENTITY_INSERT MealType ON;
INSERT INTO MealType (MealTypeID, MealTypeName, ExtraCost) VALUES
(1, 'Standard', 0),
(2, 'Vegetarian', 10),
(3, 'Halal', 15);
SET IDENTITY_INSERT MealType OFF;
----------------------------------------------------
-- FLIGHT TYPE
----------------------------------------------------
SET IDENTITY_INSERT FlightType ON;
INSERT INTO FlightType (FlightTypeID, FlightTypeName) VALUES
(1, 'Domestic'),
(2, 'International');
SET IDENTITY_INSERT FlightType OFF;
----------------------------------------------------
-- FC OPTIONS
----------------------------------------------------
SET IDENTITY_INSERT FCOption ON;
INSERT INTO FCOption (FCOptionID, FCOptionName, Description, ExtraCost) VALUES
(1, 'Extra Luggage', 'Additional 10kg luggage', 30),
(2, 'Priority Boarding', 'Skip the queue', 20),
(3, 'Wi-Fi Access', 'In-flight Wi-Fi', 15),
(4, 'Lounge Access', 'Airport lounge access', 40);
SET IDENTITY_INSERT FCOption OFF;
----------------------------------------------------
-- BOOKINGS
----------------------------------------------------
SET IDENTITY_INSERT Booking ON;
INSERT INTO Booking (BookingID, UserID, ScheduleID, ClassID, FlightTypeID, SeatTypeID, MealTypeID, BookingDate, TotalPrice, Status) VALUES
(1, 1, 1, 1, 1, 1, 1, GETDATE(), 170.00, 'confirmed'),     -- Economy + Window
(2, 2, 2, 2, 2, 2, 3, GETDATE(), 475.00, 'confirmed'),     -- Business + Aisle + Halal
(3, 3, 3, 3, 2, 1, 2, GETDATE(), 590.00, 'pending'),       -- First + Window + Veg
(4, 4, 4, 2, 2, 1, 3, GETDATE(), 635.00, 'confirmed'),     -- Business + Window + Halal
(5, 5, 6, 1, 1, 3, 1, GETDATE(), 120.00, 'confirmed'),     -- Economy + Middle
(6, 1, 7, 3, 2, 1, 3, GETDATE(), 1035.00, 'pending'),      -- First + Window + Halal
(7, 2, 9, 2, 2, 2, 2, GETDATE(), 685.00, 'confirmed');     -- Business + Aisle + Veg
SET IDENTITY_INSERT Booking OFF;
----------------------------------------------------
-- BOOKING FC OPTIONS
----------------------------------------------------
--SET IDENTITY_INSERT BookingFCOption ON;
INSERT INTO BookingFCOption (BookingID, FCOptionID) VALUES
(1, 1),  -- Booking 1: Extra Luggage
(2, 2),  -- Booking 2: Priority Boarding
(3, 3),  -- Booking 3: Wi-Fi
(4, 1),  -- Booking 4: Extra Luggage
(4, 2),  -- Booking 4: Priority Boarding
(6, 4),  -- Booking 6: Lounge Access
(7, 3);  -- Booking 7: Wi-Fi
--SET IDENTITY_INSERT BookingFCOption OFF;
----------------------------------------------------
-- FLIGHT CLASS (Which classes available on each flight)
----------------------------------------------------
--SET IDENTITY_INSERT FlightClass ON;
INSERT INTO FlightClass (FlightID, ClassID) VALUES
(1, 1), (1, 2),           -- Flight 1: Economy, Business
(2, 1), (2, 2), (2, 3),   -- Flight 2: All classes
(3, 1), (3, 2), (3, 3),   -- Flight 3: All classes
(4, 2), (4, 3),           -- Flight 4: Business, First
(5, 1), (5, 2),           -- Flight 5: Economy, Business
(6, 1),                   -- Flight 6: Economy only
(7, 1), (7, 2), (7, 3),   -- Flight 7: All classes
(8, 1), (8, 2),           -- Flight 8: Economy, Business
(9, 2), (9, 3),           -- Flight 9: Business, First
(10, 1), (10, 2);         -- Flight 10: Economy, Business
--SET IDENTITY_INSERT FlightClass OFF;
----------------------------------------------------
-- ADMIN FLIGHT CONTROL
----------------------------------------------------
--SET IDENTITY_INSERT AdminFlightControl ON;
INSERT INTO AdminFlightControl (AdminID, FlightID) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10);
--SET IDENTITY_INSERT AdminFlightControl OFF;
----------------------------------------------------
-- LAYOVER (Connecting flights)
----------------------------------------------------
SET IDENTITY_INSERT LayOver ON;
INSERT INTO LayOver (LayoverID, FlightID_1, FlightID_2, LayoverCityID, LayoverDuration) VALUES
(1, 1, 2, 2, 120),   -- Karachi->Lahore->Dubai (layover in Lahore)
(2, 2, 4, 3, 90),    -- Karachi->Dubai->Istanbul (layover in Dubai)
(3, 4, 5, 4, 150);   -- Dubai->Istanbul->Riyadh (layover in Istanbul)
SET IDENTITY_INSERT LayOver OFF;
----------------------------------------------------
-- COMMIT or ROLLBACK
----------------------------------------------------
-- Use COMMIT to save data permanently
-- Use ROLLBACK to test without saving

-- COMMIT TRANSACTION;