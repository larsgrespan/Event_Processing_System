<p align="center">
  <h1 align="center"> Implementation of a lambda architecture  </h1>
  <p align="center">
<br>
   Implementation of a lambda architecture based on the premise of identical data processing in the batch and speed layers.
    <br/>
    <a href="Placeholder_auf_GitHub_Ordner_Mit_Thesis"><strong>Thesis paper »</strong></a>
    <br/>
    <br/>
    <a href="Placeholder_auf_GitHub_Ordner_mit_ChangeStreams_Impl">MongoDB Change Streams</a>
    ·
    <a href="Placeholder_REST_IMPL">REST</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

Das Projekt wurde als Bachelorthesis des Studienganges Wirtschaftsinformatik der Hochschule Furtwangen University ([HFU](https://www.hs-furtwangen.de/)) entwickelt. 
Kurze Beschreibung für Thesis (Vllt Abstract)
<br>
Detaillierte Informationen zu den Beiträgen und Inhalten finden Sie im [Paper](Placeholder_Link_zu_Thesis_Ordner) zur Forschungsarbeit.


<!-- GETTING STARTED -->
## Getting Started

Um eine lokale Kopie des Projekts zum Laufen zu bringen, folgen Sie den hier beschriebenen Schritten:

### Prerequisites

Im Rahmen dieser Forschungsarbeit wurde eine [Virtuelle Maschine](https://www.virtualbox.org/) mit den folgenden Spezifikationen verwendet:

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

Ein entsprechendes Ubuntu-Imagine finden Sie u.a. [hier](https://www.osboxes.org/ubuntu/).

### Installation

1. Es wird empfohlen, die folgenden Schritte innerhalb einer virtuellen Python Umgebung durchzuführen.
   ```sh
   python3 -m venv <env-name>
   source <env-name>/bin/activate
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/placeholderGithubLink
   ```
3. Führen Sie anschließend den folgenden Befehl aus, um sicherzustellen, dass die erforderlichen Bibliotheken auf Ihrem System installiert sind: 
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

Spezifische Informationen zur Durchführung finden Sie in den README.md Dateien in den Unterordnern <a href="Placeholder_auf_Change_Stream_Readme">MongoDB Change Streams README.md</a> und <a href="Placeholder_auf_REST_Readme">REST README.md</a>

<!-- CONTACT -->
## Contact

Lars Grespan - larsgrespan@gmail.com </br>
Project Link: [Placeholder_Github_Link](https://github.com/placeholderlink)



