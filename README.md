# Missing

- Data Collection to a DB
- Machine Learning

# What is done

- Reception of data from accelerometer
- Interpolation of such data
- Download of the data recieved
- Download of the Interpolated data
- Calculation of the Ressonant Frequencies
- Webservices to send the stuff back to the phone

# What does this mean functionally

An engineer can get the Frequency Analysis chart and make a decision if the bridge is safe or not. 
Basically this means that the project can already do what the normal systems do, yet using just a conventional smartphone. We are just missing the machine learning function to make the decisions for a human, so any person can actually go on a walk, measure a bridge and know if it's safe or not :)

# Database creation

The application requires an existing database called app4shm and a user app4shm with pass app4shm123

Here's the script to prepare this:

    create database app4shm;
    create user 'app4shm'@'localhost' identified by 'app4shm123';
    grant all privileges on app4shm.* to 'app4shm'@'localhost';