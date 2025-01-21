DROP DATABASE IF EXISTS `P3_ANDROID_STUDIO`;
CREATE DATABASE `P3_ANDROID_STUDIO`;
USE `P3_ANDROID_STUDIO`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`(
	email VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    image VARCHAR(255) DEFAULT 'no_img'
);

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group`(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255) NOT NULL,
    image VARCHAR(255) DEFAULT 'no_img'
);

DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group`(
	user_email VARCHAR(255) REFERENCES `user`(email)
    ON UPDATE CASCADE ON DELETE CASCADE,
    group_id VARCHAR(255) REFERENCES `group`(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    debt DOUBLE DEFAULT 0,
    PRIMARY KEY(user_email, group_id)
);

DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification`(
	notif_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	user_email VARCHAR(255) REFERENCES `user`(email)
    ON UPDATE CASCADE ON DELETE CASCADE,
    group_id VARCHAR(255) REFERENCES `group`(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    notif_date DATE
);

DROP TABLE IF EXISTS `payment`;
CREATE TABLE `payment`(
	payment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    payer_email VARCHAR(255) REFERENCES `user`(email)
    ON UPDATE CASCADE ON DELETE CASCADE,
    group_id VARCHAR(255) REFERENCES `group`(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    payment_date DATE,
    payment_args VARCHAR(255) NOT NULL,
    total_payment DOUBLE NOT NULL
);

DROP TABLE IF EXISTS `user_payment`;
CREATE TABLE `user_payment`(
	payment_id INTEGER REFERENCES `payment`(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    user_email INTEGER REFERENCES `user`(email)
    ON UPDATE CASCADE ON DELETE CASCADE,
    quantity DOUBLE DEFAULT 0,
    paid BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(payment_id, user_email)
);

INSERT INTO `user`(email, username, password) values ('erik@gmail.com', 'ErikAT', sha2('erik', 256));
INSERT INTO `group`(group_name) values('Grupo de prueba');
INSERT INTO `user_group`(user_email, group_id) values ('erik@gmail.com', 1);