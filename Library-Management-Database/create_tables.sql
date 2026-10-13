CREATE TABLE Member (
MemberID int AUTO_INCREMENT PRIMARY KEY,
Member_Fname varchar(50) ,
Member_Lname varchar(50),
Member_Email varchar(50),
Member_Phone varchar(30),
Member_Type varchar(30)
) AUTO_INCREMENT = 100;

CREATE TABLE Staff (
StaffID int PRIMARY KEY,
Staff_Name varchar(100),
Staff_Email varchar(50);

CREATE TABLE EventType (
EventTypeID int PRIMARY KEY,
Description varchar(100) );

CREATE TABLE Room (
RoomID int PRIMARY KEY,
Room_Name varchar(50),
Room_Capacity int,
Hourly_Rate decimal(10,2),
Facilities varchar(200));

CREATE TABLE Event(
EventID int PRIMARY KEY,
Event_Name varchar(100),
EventTypeID int NOT NULL,
Event_Date date,
Event_Duration int CHECK (Event_Duration > 0),
RoomID int NOT NULL,
StaffID int NOT NULL,
MemberID int NOT NULL,
Ticket_Cost decimal(10,2),
FOREIGN KEY (EventTypeID) REFERENCES EventType(EventTypeID),
FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
FOREIGN KEY (MemberID) REFERENCES Member(MemberID));

CREATE TABLE EventBooking (
BookingID int PRIMARY KEY,
MemberID int NOT NULL,
EventID int NOT NULL,
Booking_Date date,
Booking_Status varchar(50),
FOREIGN KEY (EventID) REFERENCES Event(EventID),
FOREIGN KEY (MemberID) REFERENCES Member(MemberID));

CREATE TABLE RoomPayment (
PaymentID int AUTO_INCREMENT PRIMARY KEY,
EventID int NOT NULL,
MemberID int NOT NULL,
Payment_Date date,
Amount_Paid decimal(10,2),
Payment_Method varchar(30),
Payment_Status varchar(30),
FOREIGN KEY (EventID) REFERENCES Event(EventID),
FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
) AUTO_INCREMENT = 200;

CREATE TABLE Feedback (
FeedbackID int AUTO_INCREMENT PRIMARY KEY,
EventID int NOT NULL,
Feedback_Date date default(CURRENT_DATE),
Feedback_Rating int CHECK (Feedback_Rating BETWEEN 1 AND 5),
Feedback_Comments text,
FOREIGN KEY (EventID) REFERENCES Event(EventID)
) AUTO_INCREMENT = 500;





