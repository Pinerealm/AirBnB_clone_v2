-- This script will prepare a MySQL development server
-- Create a database named 'hbnb_dev_db'
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a database user named 'hbnb_dev' with password 'hbnb_dev_pwd'
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on database 'hbnb_dev_db' to user 'hbnb_dev'
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
 
-- Grant SELECT privilege on database 'performance_schema' to user 'hbnb_dev'
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';