-- This script will prepare a MySQL test server
-- Create a database named 'hbnb_test_db'
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a database user named 'hbnb_test' with password 'hbnb_test_pwd'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on database 'hbnb_test_db' to user 'hbnb_test'
GRANT ALL ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on database 'performance_schema' to user 'hbnb_test'
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
