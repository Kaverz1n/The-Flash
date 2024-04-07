CREATE TABLE admins
(
	admin_id smallserial,
	admin_telegram_id int NOT NULL UNIQUE,
	admin_password varchar(15) NOT NULL,

	CONSTRAINT pk_admins_admin_id PRIMARY KEY (admin_id)
);

CREATE TABLE rates
(
	rate_id smallserial,
	rate_code varchar(3) NOT NULL UNIQUE,
	rate_value real NOT NULL,
	commission smallint NOT NULL,

	CONSTRAINT pk_rates_rate_id PRIMARY KEY (rate_id)
);

CREATE TABLE users
(
	user_id serial,
	user_telegram_id int NOT NULL UNIQUE,
	user_nickname varchar(32) NOT NULL,
	user_name varchar(20) NOT NULL,
	user_surname varchar(20) NOT NULL,
	user_patronymic varchar(20) NOT NULL,
	user_phone varchar(15) NOT NULL UNIQUE,
	delivery_address text NOT NULL,
	current_orders smallint NOT NULL,
	completed_orders smallint NOT NULL,
	canceled_orders smallint NOT NULL,

	CONSTRAINT pk_users_user_id PRIMARY KEY (user_id)
);

CREATE TABLE orders
(
	order_id serial,
	order_url varchar(35) NOT NULL,
	yuan_price int NOT NULL,
	rub_price int NOT NULL,
	order_photo_id text NOT NULL,
	order_size varchar(10) NOT NULL,
	user_id int NOT NULL,
	chat_telegram_id int NOT NULL,

	CONSTRAINT pk_orders_order_id PRIMARY KEY (order_id),
	CONSTRAINT fk_orders_user_id FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE maintenance_mode
(
	maintenance_mode_id serial,
	is_enabled boolean NOT NULL,

	CONSTRAINT pk_maintenance_mode_maintenance_mode_id PRIMARY KEY(maintenance_mode_id)
);