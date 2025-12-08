
SELECT UserID, email, nationality, phoneNumber, countryID, cityID -- validating user from database based on user input
FROM [User]
WHERE ([User].passportNumber = '?'  OR [user].Email = '?')
  AND [user].[Password] = '?'; -- Error message displayed of "your account doesnt exist" when screen will be connected to python and validation fails

SELECT AdminID, username, email, position, phoneNumber  --validation same as user based on admin input
FROM Admin 
WHERE (admin.Username = '?' OR Admin.Email = '?') AND Admin.[Password] = '?';


-- Query 3: Check if User Account Exists
SELECT COUNT(*) as count
FROM [User]
WHERE passportNumber = '?' OR Email = '?';

-- Query 4: Check if Admin Account Exists
SELECT COUNT(*) as count
FROM Admin
WHERE Username = '?' OR Email = '?'