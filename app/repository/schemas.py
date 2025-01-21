from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    email:str
    username:str
    password:str
    image:str
    groups:list

class Group(BaseModel):
    id:int
    group_name:str
    image:str
    users:list

class Notification(BaseModel):
    notif_id:int
    user:User
    group:Group
    notif_date:datetime

class Payment(BaseModel):
    payment_id:int
    payer:str
    group:str
    payment_date:datetime
    payment_args:str

# CREATE TABLE `user`(
# 	email VARCHAR(255) PRIMARY KEY,
#     username VARCHAR(255) UNIQUE,
#     password VARCHAR(255) NOT NULL,
#     image VARCHAR(255) NOT NULL
# );
# 
# CREATE TABLE `group`(
# 	id INTEGER PRIMARY KEY AUTO_INCREMENT,
#     group_name VARCHAR(255) NOT NULL,
#     image VARCHAR(255) NOT NULL
# );
# 
# CREATE TABLE `user_group`(
# 	user_email VARCHAR(255) REFERENCES `user`(email)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     group_id VARCHAR(255) REFERENCES `group`(id)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     debt DOUBLE DEFAULT 0,
#     PRIMARY KEY(user_email, group_id)
# );
# 
# CREATE TABLE `notification`(
# 	notif_id INTEGER PRIMARY KEY AUTO_INCREMENT,
# 	user_email VARCHAR(255) REFERENCES `user`(email)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     group_id VARCHAR(255) REFERENCES `group`(id)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     notif_date DATE
# );
# 
# CREATE TABLE `payment`(
# 	payment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
#     payer_email VARCHAR(255) REFERENCES `user`(email)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     group_id VARCHAR(255) REFERENCES `group`(id)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     payment_date DATE,
#     payment_args VARCHAR(255)
# );
# 
# CREATE TABLE `user_payment`(
# 	payment_id INTEGER REFERENCES `payment`(id)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     user_email INTEGER REFERENCES `user`(email)
#     ON UPDATE CASCADE ON DELETE CASCADE,
#     quantity DOUBLE DEFAULT 0,
#     PRIMARY KEY(payment_id, user_email)
# );