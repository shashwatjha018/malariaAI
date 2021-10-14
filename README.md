# malariaAI- Malaria Detection Web Application

<span>
 <img src = 'https://img.shields.io/badge/Made%20with-Python-1f425f.svg'>
 <img src = 'https://img.shields.io/badge/License-GPL%20v3-yellow.svg'>
 <img src = 'https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white'>
 <img src = 'https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white'>
 <img src = 'https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white'>
 <img src = 'https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white'>
</span>


-  A web application where user can upload their blood smear image to check whether they have malaria or not.

- Tensorflow, Keras InceptionV3 model and concept of Transfer Learning has been used.

<p align="center">
  <img src="https://user-images.githubusercontent.com/68782027/137221095-1d9732e9-6d7d-4d2d-aa4d-6017fa2d8b2a.png">
</p>


## Table of Content

 - [Objective](https://github.com/shashwatjha018/malariaAI/new/master?readme=1#objective)
 - [Features](https://github.com/shashwatjha018/malariaAI/new/master?readme=1#features)
 - [Tech Stack](https://github.com/shashwatjha018/malariaAI/new/master?readme=1#tech-stack)
 - [Installation](https://github.com/shashwatjha018/malariaAI/new/master?readme=1#installation)
 - [Few Screenshots](https://github.com/shashwatjha018/malariaAI/new/master?readme=1#few-screenshots)

  
    
    
## Objective

The main objectives of this project is to **give patients instant result whether they have malaria or not**. Our product is easy to use and does not require any medical knowledge therefore can be used by anyone. **_It will also ensure contactless check up during this pandemic and reduce some workload of the doctors_**.

## Features

- Login/Signup with user validations.
- Payment gateway for a user to pay a one time fee.
- Image upload section where user can upload their blood smear image and fill all the necessary details.
- Depending on the result, this application will show what steps the user need to take.
    - If the result is positive, symtomps of Malaria will be displayed.
    - If the result is negative, precautions to avoid Malaria will be displayed.
- User can get their result by downloading thier report or via email.


## Tech Stack

- **FRONTEND** 
    - **LANGUAGE:** HTML5, CSS3, Javascript
    - **FRAMEWORK:** Bootstrap 4, Jquery
- **BACKEND**
    - **LANGUAGE:** Python
    - **FRAMEWORK:** Flask, Jinja2, Tensorflow, Keras
    - **DATABASE:** MongoDB

  

## Installation

*To run the application in your local WINDOWS OS*

1. Download and install **Python** in your local system from [here](https://www.python.org/downloads/).
2. Download and install **MongoDB** from [here](https://www.mongodb.com/try/download/community).
3. Download and install **MongoDB Compass** from [here](https://www.mongodb.com/try/download/compass). As the GUI for MongoDB, MongoDB Compass allows you to make smarter decisions about document structure, querying, indexing, document validation, and more. Commercial subscriptions include technical support for MongoDB Compass.
4. Download the **code repository** from above.
5. Open your command prompt and **make a new virtual environment** directory/folder by using the below command.

  ```bash
  py -m venv <directory_name>
  Eg: py -m venv example_dir

  ```
6. Copy all the files inside the downloaded directory/folder from this repository and paste it in the virtual environment directory/folder you just made.
7. **Activate the virtual environment** by using the below command.
  ```bash
  <directory_name>\Scripts\activate
  Eg: example_dir\Scripts\activate
  ```
8. Enter the directory/folder by using the below command.
  ```bash
  cd <directory_name>
  Eg: cd example_dir
  ```
9. Install the required external packages/modules in order to run the program by using the below command.
  ```bash
  pip install -r requirements.txt
  ```
10. **Open the MongoDB Compass** and start the `localhost:27017` server.

11. To run and deploy the application in your local server, use the below commands step by step.
  ```bash
  set FLASK_APP = app.py 
  flask run 
  ```
12. To run and deploy the application in your local server in _debug mode_, use the below commands step by step.
  ```bash
  set FLASK_DEBUG = 1 
  py run.py
  ```    
  
  ## Few Screenshots

**Home Page**

![image](https://user-images.githubusercontent.com/68782027/137228115-3fb60200-9464-44ee-9048-298a8e025b56.png)

**Login/Signup**

![image](https://user-images.githubusercontent.com/68782027/137228226-9b5fec11-90bb-4573-b7fd-618b2d5605ff.png)

![image](https://user-images.githubusercontent.com/68782027/137228322-5498fbec-84ca-41d2-b753-03bd7c2516a2.png)

**Payment Page**

![image](https://user-images.githubusercontent.com/68782027/137229232-420b4b68-59b0-4b4f-a5dc-124cbe730ef3.png)

![image](https://user-images.githubusercontent.com/68782027/137229261-10a94e87-2010-4ba3-a7af-5a16542d09ba.png)

**Image Upload Page**

![image](https://user-images.githubusercontent.com/68782027/137228528-9fccd3a3-d0cf-4c47-9101-ab0426097712.png)

**Result Page**

![image](https://user-images.githubusercontent.com/68782027/137228652-66a9e652-1c12-42d9-b649-4bc7601c8a88.png)

![image](https://user-images.githubusercontent.com/68782027/137228735-fa88c5c7-8be4-4a00-8c1b-e27987024411.png)

**Report via email**

![image](https://user-images.githubusercontent.com/68782027/137229020-15476866-275b-4877-b5e0-3c3f43602883.png)

**Report via downloadable report**

![image](https://user-images.githubusercontent.com/68782027/137229140-bd07217a-1590-4a5c-8f92-36a308e92b03.png)


## Made By

- [@shashwatjha018](https://github.com/shashwatjha018)

  
