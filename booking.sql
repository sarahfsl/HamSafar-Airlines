

select * from Booking
-- PARAMETERS: @FromCity, @ToCity, @OutDate, @ReturnDate, @ClassName
SELECT
    f1.FlightID AS OutboundFlightID,
    fs1.ScheduleID AS OutboundScheduleID,
    fs1.DepartureTime AS OutDepartureTime,
    fs1.ArrivalTime AS OutArrivalTime,
    f2.FlightID AS ReturnFlightID,
    fs2.ScheduleID AS ReturnScheduleID,
    fs2.DepartureTime AS ReturnDepartureTime,
    fs2.ArrivalTime AS ReturnArrivalTime,
    (f1.BaseFare + f2.BaseFare) * cl.ClassMultiplier AS TotalPrice,
    a1.Capacity - ISNULL(COUNT(b1.BookingID),0) AS OutAvailableSeats,
    a2.Capacity - ISNULL(COUNT(b2.BookingID),0) AS ReturnAvailableSeats
FROM Flight f1
JOIN FlightSchedule fs1 ON f1.FlightID = fs1.FlightID
JOIN Airport a_dep ON f1.DepartureAirportID = a_dep.AirportID
JOIN Cities c_dep ON a_dep.CityID = c_dep.CityID
JOIN Airport a_arr ON f1.ArrivalAirportID = a_arr.AirportID
JOIN Cities c_arr ON a_arr.CityID = c_arr.CityID
JOIN Flight f2 
    ON f2.DepartureAirportID = a_arr.AirportID
    AND f2.ArrivalAirportID = a_dep.AirportID
JOIN FlightSchedule fs2 ON f2.FlightID = fs2.FlightID
JOIN FlightClass fc1 ON f1.FlightID = fc1.FlightID
JOIN FlightClass fc2 ON f2.FlightID = fc2.FlightID
JOIN Class cl ON fc1.ClassID = cl.ClassID AND fc2.ClassID = cl.ClassID
JOIN Aircraft a1 ON f1.AircraftID = a1.AircraftID
JOIN Aircraft a2 ON f2.AircraftID = a2.AircraftID
LEFT JOIN Booking b1 ON b1.ScheduleID = fs1.ScheduleID AND b1.ClassID = cl.ClassID AND b1.Status <> 'cancelled'
LEFT JOIN Booking b2 ON b2.ScheduleID = fs2.ScheduleID AND b2.ClassID = cl.ClassID AND b2.Status <> 'cancelled'
WHERE
    CONCAT(a_dep.Name, ', ', c_dep.CityName) = '?'
    AND CONCAT(a_arr.Name, ', ', c_arr.CityName) = '?'
    AND fs1.DepartureDate = '?'
    AND fs2.DepartureDate = '?'
    AND cl.ClassName = '?'
    AND fs1.Status = 'scheduled'
    AND fs2.Status = 'scheduled'
GROUP BY
    f1.FlightID, fs1.ScheduleID, fs1.DepartureTime, fs1.ArrivalTime,
    f2.FlightID, fs2.ScheduleID, fs2.DepartureTime, fs2.ArrivalTime,
    f1.BaseFare, f2.BaseFare, cl.ClassMultiplier,
    a1.Capacity, a2.Capacity
HAVING
    (a1.Capacity - ISNULL(COUNT(b1.BookingID),0)) > 0
    AND (a2.Capacity - ISNULL(COUNT(b2.BookingID),0)) > 0
ORDER BY fs1.DepartureTime, fs2.DepartureTime;


SELECT 
    f.FlightID,
    fs.ScheduleID,
    fs.DepartureTime,
    fs.ArrivalTime,
    a_dep.Name + ' (' + a_dep.Code + ')' AS FromAirport,
    a_arr.Name + ' (' + a_arr.Code + ')' AS ToAirport,
    (f.BaseFare * cl.ClassMultiplier) AS Price,
    a.Capacity - ISNULL(COUNT(b.BookingID), 0) AS AvailableSeats,
    fs.Duration
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
WHERE fs.ScheduleID = '?' AND cl.ClassName = '?'
GROUP BY 
    f.FlightID, fs.ScheduleID, fs.DepartureTime, fs.ArrivalTime,
    a_dep.Name, a_dep.Code, a_arr.Name, a_arr.Code, f.BaseFare, cl.ClassMultiplier,
    a.Capacity, fs.Duration
