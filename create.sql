drop table if exists Item;
drop table if exists User;
drop table if exists Bid;
drop table if exists ItemCategory;

create table Item(
   ItemID INT PRIMARY KEY,
   Name VARCHAR(100),
   Currently DECIMAL(10,2),
   Buy_Price DECIMAL(10,2),
   First_Bid DECIMAL(10,2),
   Number_of_Bids INT,
   Started TIMESTAMP,
   Ends TIMESTAMP,
   Description TEXT,
   SellerID VARCHAR(100),
   FOREIGN KEY (SellerID) REFERENCES User(UserID)
);

create table User(
   UserID VARCHAR(100) PRIMARY KEY,
   Rating INT,
   Location VARCHAR(100),
   Country VARCHAR(100),
   IsSeller BOOLEAN,
   IsBidder BOOLEAN
);

create table Bid(
   BidID INT PRIMARY KEY,
   Time TIMESTAMP,
   Amount DECIMAL(10,2),
   ItemID INT,
   UserID VARCHAR(100),
   FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
   FOREIGN KEY (UserID) REFERENCES User(UserID)
);

create table ItemCategory(
   ItemID INT,
   Category VARCHAR(100),
   PRIMARY KEY (ItemID, Category),
   FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

