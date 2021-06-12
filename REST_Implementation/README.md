<p align="center">
  <h1 align="center"> REST Implementation </h1>
  <p align="center">

<!-- ABOUT THE PROJECT -->
## About

The following describes the process of implementing REST. More specific information on the individual scripts, classes and methods can be found in Kapitel 4 - Implementierung in [Thesis](https://github.com/larsgrespan/Event_Processing_System/tree/main/Thesis) .

## Usage


### Clean Environment

In case you already executed this manual or you executed the MongoDB Change Stream Implementation manual before, a cleaning of the environment is required. 

1. Open a terminal and navigate to the <b> /REST_Implementation/Event_generation </b> directory. 

2. Run following command

   ```sh
   sudo python3 Delete_collections.py
   ```

### Test data generation

Since this project is a prototype and no real data is used, the data generation is simulated.

1. Open a terminal and navigate to the <b> /REST_Implementation/Event_Generation </b> directory. 

2. Run following commands:
   ```sh
   sudo python3 Start_data_generation.py teststation1.yaml 1000 teststation1.csv
   ```

   ```sh
   sudo python3 Start_data_generation.py teststation2.yaml 1000 teststation2.csv
   ```

   ```sh
   sudo python3 Start_data_generation.py teststation3.yaml 1000 teststation3.csv
   ```

3. Store the simulated files in a mongodb collection

   ```sh
   sudo python3 Store_Data.py
   ```

   If you want to execute this step again execute follwing command in advance:
   ```sh
   sudo python3 Delete_collections.py
   ```
    
### Execute Batch-Layer Training

In order to perform the Batch-Layer training execute following steps.

1. Open a terminal and navigate to the <b> /REST_Implementation/Model_training </b> directory.

2. Execute the Batch-Layer training script

   ```sh
   sudo python3 Start_batch_training.py All All
   ```

   Alternatively you can also train specific test stations or product types:
   Possilbe parameters for test stations are: All, T1 or T2
   Possible parameters for product types are: All, PT1 or PT2

   ```sh
   sudo python3 Start_batch_training.py T1 All
   ```

   ```sh
   sudo python3 Start_batch_training.py T1 PT1
   ```

   ```sh
   sudo python3 Start_batch_training.py T1 PT2
   ```

   ```sh
   sudo python3 Start_batch_training.py T2 PT1
   ```

   ```sh
   sudo python3 Start_batch_training.py T2 PT2
   ```

### Execute Speed-Layer Prediction

1. Change the directory to <b> /REST_Implementation/Processing_server </b>. 

2. Start the Server

   ```sh
   sudo python3 Start_REST_Server.py
   ```
   <br> Keep the terminal open in the background <br>


3. Open a new terminal and navigate to the <b> /REST_Implementation/Simulate_test_stations </b> directory. 

4. Simulate teststations

   In order to make predictions, events have to be sent to the REST-Server. Execute following script to simulate the event-sending process. 

   ```sh
   sudo python3 Start_sending_events.py All All
   ```

   Alternatively you can also make predictions for specific test stations or product types:
   Possilbe parameters for test stations are: All, T1 or T2
   Possible parameters for product types are: All, PT1 or PT2

   ```sh
   sudo python3 Start_sending_events.py T1 All
   ```

   ```sh
   sudo python3 Start_sending_events.py T1 PT1
   ```

   ```sh
   sudo python3 Start_sending_events.py T1 PT2
   ```
   
   ```sh
   sudo Start_sending_events.py T2 PT1
   ```

   ```sh
   sudo Start_sending_events.py T2 PT2
   ```


   The predictions for all data sample can take a while.
   In the webservice.py window you can follow the process. All positive classified events make print statements.

### Show Results

1. Open the browser and insert following link:
   ```sh
   http://127.0.0.1:5000/result
   ```
 
