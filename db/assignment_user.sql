CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	firstname TEXT NOT NULL,
	lastname TEXT NOT NULL,
	password TEXT NOT NULL,
	isadmin INT NOT NULL
);

INSERT INTO user VALUES (1, 'admin', 'John', 'Boss', 'e1dd6b3db97fed88ae4d9d8677852a4bbe27c84ddabd402c1bd97d21332b2882', 1);
INSERT INTO user VALUES (2, 'user1', 'Frodo', 'Baggins', '28574419aaeb29e61f6d41aed6262bb570609f1986fab4b997336c00542f1d57', 0);
INSERT INTO user VALUES (3, 'user2', 'Samwise', 'Gamgee', '8be161003a99df42ba1a6a090ce0f278500087f8386ee798a200dc4c6be9b49d', 0);
