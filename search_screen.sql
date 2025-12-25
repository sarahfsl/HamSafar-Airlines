-- =====================================================
-- GENERALIZED SQL QUERIES FOR FLIGHT SEARCH SYSTEM
-- =====================================================

-- =====================================================
-- 1. ONE-WAY FLIGHT SEARCH
-- =====================================================
-- Parameters needed: @from_city, @to_city, @departure_date, @class_name
-- Description: Searches for available one-way flights between two cities


-- Parameters: @from_airport_city, @to_airport_city, @departure_date, @class_name
-- Format: 'AirportName, CityName'

SELECT
    f.FlightID,
    fs.ScheduleID,

    CONCAT(a_dep.Name, ', ', c_dep.CityName) AS FromAirportCity,
    CONCAT(a_arr.Name, ', ', c_arr.CityName) AS ToAirportCity,

    fs.DepartureDate,
    fs.DepartureTime,
    fs.ArrivalDate,
    fs.ArrivalTime,

    cl.ClassID,
    cl.ClassName,

    f.BaseFare,
    (f.BaseFare * cl.ClassMultiplier) AS Price,

    a.Capacity - COUNT(b.BookingID) AS AvailableSeats

FROM Flight f
JOIN FlightSchedule fs ON f.FlightID = fs.FlightID

JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
JOIN Cities c_dep ON a_dep.CityID = c_dep.CityID

JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
JOIN Cities c_arr ON a_arr.CityID = c_arr.CityID

JOIN FlightClass fc ON f.FlightID = fc.FlightID
JOIN Class cl ON fc.ClassID = cl.ClassID

JOIN Aircraft a ON f.AircraftID = a.AircraftID

LEFT JOIN Booking b 
    ON b.ScheduleID = fs.ScheduleID
   AND b.ClassID = cl.ClassID
   AND b.Status <> 'cancelled'

WHERE
    CONCAT(a_dep.Name, ', ', c_dep.CityName) = '?'
    AND CONCAT(a_arr.Name, ', ', c_arr.CityName) = '?'
    AND fs.DepartureDate = '?'
    AND cl.ClassName = '?'
    AND fs.Status = 'scheduled'

GROUP BY
    f.FlightID, fs.ScheduleID,
    FromAirportCity, ToAirportCity,
    fs.DepartureDate, fs.DepartureTime,
    fs.ArrivalDate, fs.ArrivalTime,
    cl.ClassID, cl.ClassName,
    f.BaseFare, cl.ClassMultiplier,
    a.Capacity

HAVING
    a.Capacity - COUNT(b.BookingID) > 0

ORDER BY fs.DepartureTime;


-- =====================================================
-- 2. ROUND-TRIP FLIGHT SEARCH
-- =====================================================
-- Parameters needed: @from_city, @to_city, @outbound_date, @return_date, @class_name
-- Description: Searches for round-trip flights (outbound + return)
-- Parameters: @from_airport_city, @to_airport_city, @outbound_date, @return_date, @class_name
-- Format: 'AirportName, CityName'

SELECT
    -- Outbound
    f1.FlightID AS OutboundFlightID,
    fs1.ScheduleID AS OutboundScheduleID,
    CONCAT(d1.Name, ', ', c1.CityName) AS FromAirportCity,
    CONCAT(a1.Name, ', ', c2.CityName) AS ToAirportCity,
    fs1.DepartureDate AS OutDate,
    fs1.DepartureTime AS OutTime,

    -- Return
    f2.FlightID AS ReturnFlightID,
    fs2.ScheduleID AS ReturnScheduleID,
    fs2.DepartureDate AS ReturnDate,
    fs2.DepartureTime AS ReturnTime,

    cl.ClassName,

    (f1.BaseFare * cl.ClassMultiplier) AS OutPrice,
    (f2.BaseFare * cl.ClassMultiplier) AS ReturnPrice,
    (f1.BaseFare + f2.BaseFare) * cl.ClassMultiplier AS TotalPrice

FROM Flight f1
JOIN FlightSchedule fs1 ON f1.FlightID = fs1.FlightID
JOIN Airport d1 ON f1.DepartureAirportID = d1.AirportID
JOIN Cities c1 ON d1.CityID = c1.CityID
JOIN Airport a1 ON f1.ArrivalAirportID = a1.AirportID
JOIN Cities c2 ON a1.CityID = c2.CityID

JOIN Flight f2 
   ON f2.DepartureAirportID = a1.AirportID
  AND f2.ArrivalAirportID = d1.AirportID
JOIN FlightSchedule fs2 ON f2.FlightID = fs2.FlightID

JOIN FlightClass fc ON f1.FlightID = fc.FlightID
JOIN Class cl ON fc.ClassID = cl.ClassID

WHERE
    CONCAT(d1.Name, ', ', c1.CityName) = '?'
    AND CONCAT(a1.Name, ', ', c2.CityName) = '?'
    AND fs1.DepartureDate = '?'
    AND fs2.DepartureDate = '?'
    AND cl.ClassName = '?'
    AND fs1.Status = 'scheduled'
    AND fs2.Status = 'scheduled';

-- =====================================================
-- 3. GET ALL CITIES (for dropdown population)
-- =====================================================
-- Description: Retrieves all unique cities that have airports

SELECT
    CONCAT(a.Name, ', ', c.CityName) AS AirportCity,
    a.AirportID
FROM Airport a
JOIN Cities c ON a.CityID = c.CityID
ORDER BY c.CityName, a.Name;


-- =====================================================
-- 4. GET ALL FLIGHT CLASSES (for dropdown population)
-- =====================================================
-- Description: Retrieves all available flight classes
SELECT
    ClassID,
    ClassName,
    ClassMultiplier
FROM Class
ORDER BY ClassMultiplier;


-- =====================================================
-- 5. ONE-WAY FLIGHT SEARCH WITH FLEXIBLE DATES
-- =====================================================
-- Parameters: @from_city, @to_city, @start_date, @end_date, @class_name
-- Description: Search flights within a date range

SELECT
    f.FlightID,
    fs.ScheduleID,
    c1.CityName AS FromCity,
    c2.CityName AS ToCity,
    fs.DepartureDate,
    fs.DepartureTime,
    cl.ClassName,
    (f.BaseFare * cl.ClassMultiplier) AS Price

FROM Flight f
JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
JOIN Airport a1 ON f.DepartureAirportID = a1.AirportID
JOIN Cities c1 ON a1.CityID = c1.CityID
JOIN Airport a2 ON f.ArrivalAirportID = a2.AirportID
JOIN Cities c2 ON a2.CityID = c2.CityID
JOIN FlightClass fc ON f.FlightID = fc.FlightID
JOIN Class cl ON fc.ClassID = cl.ClassID

WHERE
    c1.CityName = '?'
    AND c2.CityName = '?'
    AND fs.DepartureDate BETWEEN '?' AND '?'
    AND cl.ClassName = '?'
    AND fs.Status = 'scheduled'

ORDER BY fs.DepartureDate;


-- =====================================================
-- 6. SEARCH ALL CLASSES FOR ONE-WAY (Price Comparison)
-- =====================================================
-- Parameters: @from_city, @to_city, @departure_date
-- Description: Shows all available classes for the same flight

SELECT
    f.FlightID,
    fs.ScheduleID,
    cl.ClassName,
    (f.BaseFare * cl.ClassMultiplier) AS Price
FROM Flight f
JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
JOIN FlightClass fc ON f.FlightID = fc.FlightID
JOIN Class cl ON fc.ClassID = cl.ClassID
WHERE
    fs.ScheduleID = '?'
ORDER BY cl.ClassMultiplier;

-- =====================================================
-- 7. GET CHEAPEST FLIGHTS (One-Way)
-- =====================================================
-- Parameters: @from_city, @to_city, @departure_date
-- Description: Returns the cheapest available flight

SELECT TOP 1
    f.FlightID,
    fs.ScheduleID,
    cl.ClassName,
    (f.BaseFare * cl.ClassMultiplier) AS Price
FROM Flight f
JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
JOIN FlightClass fc ON f.FlightID = fc.FlightID
JOIN Class cl ON fc.ClassID = cl.ClassID
WHERE
    fs.DepartureDate = '?'
ORDER BY Price;

-- =====================================================
-- 8. CHECK SEAT AVAILABILITY
-- =====================================================
-- Parameters: @schedule_id, @class_id
-- Description: Checks available seats for a specific flight schedule and class
SELECT
    fs.ScheduleID,
    f.FlightID,
    cl.ClassName,
    a.Capacity,
    COUNT(b.BookingID) AS BookedSeats,
    a.Capacity - COUNT(b.BookingID) AS AvailableSeats

FROM FlightSchedule fs
JOIN Flight f ON fs.FlightID = f.FlightID
JOIN Aircraft a ON f.AircraftID = a.AircraftID
JOIN Class cl ON cl.ClassID = '?'
LEFT JOIN Booking b 
    ON b.ScheduleID = fs.ScheduleID
   AND b.ClassID = cl.ClassID
   AND b.Status <> 'cancelled'

WHERE fs.ScheduleID = '?'

GROUP BY
    fs.ScheduleID, f.FlightID, cl.ClassName, a.Capacity;
