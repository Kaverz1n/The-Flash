TRUNCATE TABLE admins CASCADE;
TRUNCATE TABLE rates CASCADE;
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE order_statuses CASCADE;
TRUNCATE TABLE orders CASCADE;
TRUNCATE TABLE maintenance_mode CASCADE;
TRUNCATE TABLE tech_support CASCADE;

TRUNCATE TABLE admins RESTART IDENTITY;
TRUNCATE TABLE rates RESTART IDENTITY;
TRUNCATE TABLE users RESTART IDENTITY;
TRUNCATE TABLE order_statuses RESTART IDENTITY;
TRUNCATE TABLE orders RESTART IDENTITY;
TRUNCATE TABLE maintenance_mode RESTART IDENTITY;
TRUNCATE TABLE tech_support RESTART IDENTITY;