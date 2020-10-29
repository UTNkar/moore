# Installing and setting up Postgresql

Postgresql is the database management system (DBMS) used by the registration system. Follow these instructions to set it up

## Installation

### MacOS

1. Install [homebrew](http://brew.sh)
2. Install postgres `brew install postgres`
3. Create a launch agents directory `mkdir -p ~/Library/LaunchAgents`
4. Create symlinks to LaunchAgents `ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents`
5. Run this command to start postgres automatically on startup `launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist`. 
**NOTE** the path `~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist` might be different on your computer! Dubblecheck if it is different!

You might have to add the following lines to your .zprofile
```
    export LDFLAGS="-L/usr/local/opt/openssl/lib"
    export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

### Ubuntu

Follow the installation instructions on [postgresql's website](https://www.postgresql.org/download/linux/ubuntu/)

## Creating a postgres user and database

1. Run the command `createuser -s -P name_of_user` to create a user with super-user privileges and with a password
2. Run the command `createdb -O name_of_user registrationsystem` to create a database called `registrationsystem` with the owner set to the user you created previously

You have now setup postgresql!
