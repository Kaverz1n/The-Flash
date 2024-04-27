# THE FLASH

## PROJECT DESCRIPTION

The Flash is a handy Telegram bot created specifically for users who want to purchase original
goods from POIZON (DEWU) marketplace with minimal effort and maximum comfort. It offers a simple
and fast checkout process for any product presented on the platform.

An important feature of the bot is its handy calculator, which allows users to easily and
accurately calculate the cost of goods in rubles, based on the prices in Chinese yuan.
This greatly simplifies shopping for Russian users by providing them with transparent
information about the cost of goods.

In addition, THE FLASH offers a unique profile feature that allows users to enter their
information just once. They can then easily use this information when placing orders,
without having to re-enter their data.

This project also includes a full-featured administration panel that provides administrators
with convenient order and user management, as well as technical support tools to ensure a
quick response to any queries or questions.

Extensive validation of all data entered by users is an integral part of the project.
It helps avoid unforeseen errors and ensures safety and security for everyone involved
in the purchasing process.
> Readme was translated in english by deepl.Tthere are may be grammatical mistakes.

## PROJECT FEATURES

1. **Convenient checkout and payment via bot**: Allows users to easily place orders by
   following the bot's prompts and make payments directly through messenger, making
   the shopping process as convenient and secure as possible.
2. **Profile checkout with checkout address verification**: Allows users to create a
   profile and enter their own details, including the address of the delivery point
   with verification of its authenticity, which ensures delivery to the correct address
   and enhances delivery security.
3. **Easy navigation between sections with automatic message deletion**:
   Provides users with easy navigation between different sections of the bot
   automatic deletion of previous messages, making bot navigation smoother and more efficient.
4. **Full-featured administrative panel for data and order management**: Provides
   administrators with access to a full-featured administrative panel where they
   can retrieve any data, manage users and orders, giving them complete control over the bot.
5. **Distribution of technical support among employees**: When a user contacts technical support,
   they are automatically routed to a random technical support employee, reducing the
   workload of an individual employee and increasing the efficiency of the support team.
6. **Extensive data validation**: All data entered by users and processed by the bot goes
   through an extensive validation system, including checking for format correctness and
   information integrity. This ensures high accuracy and reliability of information,
   improves user experience and ensures the safety of users and the bot as a whole.

## REQUIREMENTS FOR SETUP AND STARTUP

### PROJECT SETUP

1. **Creating an .env file**: Create a file named **.env** in the root directory of your project.
   In the **.env** file fill:
   ```text
    BOT_TOKEN=
    BOT_USERNAME=
    DATABASE_NAME=
    DATABASE_USERNAME=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=
    MAIN_PHOTO_ID=
    HOW_TO_ORDER_VIDEO_ID=
    FULL_LOGO_URL=
    CDEK_LOGIN=
    CDEK_PASSWORD=
    PAYMENT_PROVIDER_TOKEN=
    MAIN_ADMIN_TELEGRAM_ID=
   ```
2. **Activation the virtual environment**: Activate the virtual environment with the command:
    ```commandline
   poetry shell
   ```
3. **Installation python packages**: Install all python packages intended for the
   project using the command:
   ```commandline
   poetry install
   ```
2. **Changing bot content**: Change the content of messages sent by bots to your own.

### PROJECT STARTUP

To start the project it is necessary to run the executable file – **main.py**.

## ROLE ASSIGNMENT

1. **User**: These users have access to the basic functions of the bot. They can interact with the bot to make
   purchases and get necessary information.
2. **Administrator**: Administrators have all the functions of regular users, but also have access to a special
   administrative panel. They have advanced access rights and full control over the bot.
3. **Technical Support**: These users are specialists who provide help and support to regular bot users. Users can
   contact tech support with questions, problems, or requests for assistance.

### USER ROLE ASSIGNMENT

1. **Authorization in admin panel**: The main administrator needs to authorize in the admin panel of the bot using his
   credentials.
2. **Selecting the user type**: In the admin panel, the administrator selects the type of user to which the new role
   should be assigned: administrator or technical support specialist.
3. **Adding a user**: After selecting a user type, the administrator enters information about the user to whom the new
   role should be assigned. This can include a unique user ID (Telegram ID) and/or other necessary information.


## CONTACT

If you have any questions, suggestions or need support, feel free to contact me. I am available to help you with your
project and answer all your questions. You can reach me at the following contacts:

**E-mail**: dima.captan@yandex.ru

**Telegram**: @Kaverz1n.

## SPECIAL THANKS

I would like to express my sincere gratitude to you for using the project and for the trust you have shown me. Your
participation and support are invaluable to me and to the development of my application
>README WAS TRANSLATED IN ENGLISH BY DEEPL. THERE ARE MAY BE GRAMMATICAL MISTAKES
