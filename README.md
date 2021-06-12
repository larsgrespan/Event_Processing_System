<p align="center">
  <h1 align="center"> Creating a data processing architecture for building and using machine learning models in quality management  </h1>
  <p align="center">
<br>
Bachelor Thesis
    <br/>
    <a href="https://github.com/larsgrespan/Event_Processing_System/tree/main/Thesis"><strong>Thesis paper »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/larsgrespan/Event_Processing_System/tree/main/Changestream_Implementation">MongoDB Change Streams</a>
    ·
    <a href="https://github.com/larsgrespan/Event_Processing_System/tree/main/REST_Implementation">REST</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

The project was developed as a bachelor's thesis for the Business Informatics course at Furtwangen University ([HFU](https://www.hs-furtwangen.de/)). 
This research work deals with the creation of a data processing architecture in the field of quality management. Machine learning models are used to predict product defects in a production environment. The input for the machine learning models is data generated at various quality testing stations within the production process. For the creation of the architecture, the creation of the models as well as the actual usage of the models in form of defect predictions must be included. Both the creation of the models and their usage by the error predictions require upstream data processing. The central research subject of this paper is the development of an architecture that implements a unified data processing for both the model creation and the model usage. 
<br>
Detailed information on the contributions and contents can be found in the  [Paper](https://github.com/larsgrespan/Event_Processing_System/tree/main/Thesis).


<!-- GETTING STARTED -->
## Getting Started

To get a local copy of the project running, follow the steps described here:

### Prerequisites

Within the scope of this research work, a [Virtuel Machine](https://www.virtualbox.org/) with the following specifications was used:

**Hardware** <br>
Architecture:		x86_64<br>
Model name:		Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz<br>
PU op-mode(s):		32-bit, 64-bit<br>
CPU(s):			4<br>
RAM:			8 GB<br>

**Distribution**<br>
Description:		Ubuntu 20.04.1 LTS<br>
Release:		20.04<br>
Codename:		focal<br>
	
**Kernel**<br>
5.4.0-53-generic<br>

You can find a corresponding Ubuntu Imagine here [here](https://www.osboxes.org/ubuntu/).

### Installation

1. It is recommended to perform the following steps within a Python virtual environment
   ```sh
   python3 -m venv <env-name>
   source <env-name>/bin/activate
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/placeholderGithubLink
   ```
3. Then run the following command to ensure that the required libraries are installed on your system:  
   ```sh
   pip install -r requirements.txt
   ```

### Install and Configure MongoDB

Refer to  <a href="https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/"><strong>Install MongoDB »</strong></a>
    

1. Import the public key used by the package management system

   From a terminal, issue the following command to import the MongoDB public GPG Key 
   from https://www.mongodb.org/static/pgp/server-4.4.asc:
   ``` sh
   wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
   ```

   The operation should respond with an OK.
   However, if you receive an error indicating that gnupg is not installed, you can:
   Install gnupg and its required libraries using the following command:
   ``` sh
   sudo apt-get install gnupg
   ```

   Once installed, retry importing the key:
   ``` sh
   wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
   ```

2. Create a list file for MongoDB

   Create the list file /etc/apt/sources.list.d/mongodb-org-4.4.list for your version of Ubuntu.
   Click on the appropriate tab for your version of Ubuntu. If you are unsure of what Ubuntu version the host is running, open a terminal or shell on the host and execute lsb_release -dc.
   The following instruction is for Ubuntu 20.04 (Focal).
   Create the /etc/apt/sources.list.d/mongodb-org-4.4.list file for Ubuntu 20.04 (Focal):
   ``` sh
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
   ```

3. Reload local package database

   Issue the following command to reload the local package database:
   ``` sh
   sudo apt-get update
   ```

4. Install the MongoDB packages

   You can install either the latest stable version of MongoDB or a specific version of MongoDB.
   To install the latest stable version, issue the following:
   ``` sh
   sudo apt-get install -y mongodb-org
   ```

   Optional. Although you can specify any available version of MongoDB, apt-get will upgrade the packages when a newer version becomes available. To prevent unintended upgrades, you can pin the package at the currently installed version:
   ``` sh
   echo "mongodb-org hold" | sudo dpkg --set-selections
   echo "mongodb-org-server hold" | sudo dpkg --set-selections
   echo "mongodb-org-shell hold" | sudo dpkg --set-selections
   echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
   echo "mongodb-org-tools hold" | sudo dpkg --set-selections
   ```

5. Start MongoDB

   You can start the mongod process by issuing the following command:
   ``` sh
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

6. Verify that MongoDB has started successfully

   ``` sh
   sudo systemctl status mongod
   ```

7. Stop MongoDB
   
   ``` sh
   As needed, you can stop the mongod process by issuing the following command:
   sudo systemctl stop mongod
   ```

### Convert a standalone mongod to a replicaSet 

Refer to  <a href="https://docs.mongodb.com/manual/tutorial/convert-standalone-to-replica-set/"><strong>Convert a standalone to a replicaSet »</strong></a>

1. Stop the MongoDB Server
    ``` sh
    service mongod stop
    ```

2. Restart the instance. Use the --replSet option to specify the name of the new replica set.For example, the following command starts a standalone instance as a member of a new replica set named rs0.

    ``` sh
    sudo mongod --port 27017 --dbpath /var/lib/mongodb --replSet rs1 --bind_ip localhost
    ```

    <br> Keep the terminal open in the background <br>

3. Open a new Terminal and start a new mongod service:
   
    ``` sh
    service start mongod
    ```

    Open mongodb shell
    ``` sh
    mongo
    ```

    Configure ReplicaSet
    ``` sh
    use admin
    ```

    ``` sh
    rs.initiate()
    ```

    Press Enter and close the Terminal

4. After shutting down the environment, the replSet command has to be executed again:
   ``` sh
   sudo mongod --port 27017 --dbpath /var/lib/mongodb --replSet rs1 --bind_ip localhost
   ```

   <br> Keep the terminal open in the background <br>

<!-- USAGE EXAMPLES -->
## Usage

Specific information on the implementation can be found in the README.md files in the subfolders <a href="https://github.com/larsgrespan/Event_Processing_System/blob/main/Changestream_Implementation/README.md">MongoDB Change Streams README.md</a> and <a href="https://github.com/larsgrespan/Event_Processing_System/blob/main/REST_Implementation/README.md">REST README.md</a>

<!-- CONTACT -->
## Contact

Lars Grespan - larsgrespan@gmail.com </br>
Project Link: [Event_Processing_System](https://github.com/larsgrespan/Event_Processing_System)



