-- Write a script that prepares a MySQL server for the project:
-- A database hbnb_test_db
-- A new user hbnb_test (in localhost)

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS hbnb_test@localhost IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL ON hbnb_test_db.* TO hbnb_test@localhost;
USE performance_schema;
GRANT SELECT ON performance_schema.* TO hbnb_test_db@localhost;
FLUSH PRIVILEGES;
