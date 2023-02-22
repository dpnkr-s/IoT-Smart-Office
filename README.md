## SensiSpace: IoT system for Smart Office

SensiSpace provides the perfect balance of comfort and efficiency in office spaces by utilizing Internet-of-Things (IoT) technologies which transforms any office room into an intelligent connected system.

This repository contains SensiSpace app demo, which realistically simulates sensors, actuators and environment factors for a *south oriented* office room of specific size located at coordinates: *45.05386N, 7.672202E* on *5th floor* of a building. 
All the necessary details and controls are available at an online dashboard which can be accessed on web browser.

SensiSpace is composed of three subsystems:

- Ventilation Control System
  + monitors and controls airflow, heating and Volatile Organic Compounds, ensuring optimal indoor air quality and maintaining thermal comfort throughout the winter season. 

- Shadow and Illumination Control System
  + an automated window blinds control system that shades all transparent surfaces wwith precision, adjusting to provide 70% shade in summer and 30% in winter.
  + controls office lighting after calculating the average daylight factor, optimizing the use of natural light to enhance the space, while conserving energy and reducing carbon footprint.

These systems exploit machine learning (ML) techniques (Python intyerface with Azure ML web service) to predict the number of people present in the room and adjust accordingly to reduce energy expenditures. IoT system guarantees a seamlessly smart and sustainable environment.

### Ventilation Control System

*ventilation and heating cloud monitoring dashboard*

<img width="700" alt="Screenshot 2023-02-23 at 2 28 40 AM" src="https://user-images.githubusercontent.com/25234772/220757762-574b4741-b3ca-461f-9b58-c89cb89d77eb.png">

System Features:

- designed to minimize total energy consumption by recirculating return air and increasing supply fan airflow rate to save energy spent on heating system, while satisfying minimum air changes demand

- saves energy by evaluating its new optimal state every 5 minutes, or unless interrupted by user input or changes in presence sensor, so system is not working at its full capacity all the time

- no need for parameter tuning to design ‘hard’ control systems as system exploits benefits of IoT technologies so efficient empirical control models can be obtained
  + monitoring user behaviour, sensor data and cloud computing enables computationally intensive algorithms like Neural Networks and multi-constraint optimization like Particle Swarm(PSO) to optimize system state



#### Demo office room parameters

- Length = 8.75m, Width = 6.25m, Height = 3.75m
- Room is occupied for 8 hours on an average per day
- Opaque to transparent wall surface ratio in room is greater than 65%
- Room volume = 205.078 m3
- Minimum required airflow rate per person(Qiaq)=39.6 m3/h

*estimation of VOCs and Air Changes Hour (ACH) for room*

<img width="700" alt="Screenshot 2023-02-23 at 2 38 13 AM" src="https://user-images.githubusercontent.com/25234772/220760065-0ab8cabe-edf0-4bb9-ad4a-08e658b32b8e.png">

#### System design

<img width="700" alt="Screenshot 2023-02-23 at 2 38 26 AM" src="https://user-images.githubusercontent.com/25234772/220760341-ec1b725a-8f59-4695-bd6a-a1168ff9babc.png">


### Shadow and Illumination Control System

1. Estimates average daylight factor from environment conditions, room dimension, surface materials.

<img width="400" alt="Screenshot 2023-02-23 at 2 14 29 AM" src="https://user-images.githubusercontent.com/25234772/220754931-c12c822b-3377-4d67-b69c-4cfdab46b0d7.png">

*window blinds' angle computed from solar radiation shown in dashboard below*

<img width="600" alt="Screenshot 2023-02-23 at 1 55 01 AM" src="https://user-images.githubusercontent.com/25234772/220755129-80b21e56-c538-4357-9152-f08086469661.png">

<img width="600" alt="Screenshot 2023-02-23 at 2 13 25 AM" src="https://user-images.githubusercontent.com/25234772/220755187-d5723133-6b77-4992-a880-3775ba77caac.png">

2. Calculates required luminous flux. 

<img width="400" alt="Screenshot 2023-02-23 at 2 03 26 AM" src="https://user-images.githubusercontent.com/25234772/220755642-6e3711df-8daf-441b-8f88-412411bd2375.png">

3. Divides room into sections and controls light intensity for each lamp individually according to occupancy and lighting needs

<img width="600" alt="Screenshot 2023-02-23 at 2 04 14 AM" src="https://user-images.githubusercontent.com/25234772/220756106-6a3242eb-b657-41c0-a42e-1ed8a52fc770.png">

<img width="600" alt="Screenshot 2023-02-23 at 2 04 34 AM" src="https://user-images.githubusercontent.com/25234772/220756167-c9287974-07b7-4269-ad3e-24cbc86fe8ac.png">

*dashboard shows lamps in three zones are switched ON with 80% intensity*

<img width="600" alt="Screenshot 2023-02-23 at 2 04 48 AM" src="https://user-images.githubusercontent.com/25234772/220756307-f6853747-e04e-4b62-8efa-91a5fe4ff0ca.png">

### Developers

Deepankar Sharma

Stefano Tisi

Daniel Gaiki
