# Kwiat Group's Flask App
[![Website http://quantumtomo.web.illinois.edu/](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://quantumtomo.web.illinois.edu/)
[![Generic badge](https://img.shields.io/badge/Python_version-3.8-blue.svg)](https://pypi.org/project/Quantum-Tomography/)

This is a website is to provide various plots of specific quantum states.
The site is available here: [quantumtomo.web.illinois.edu](http://quantumtomo.web.illinois.edu/)

## Setup
This python application is built,tested, and hosted around python 3.8. 
For best results [install this version of python](https://www.python.org/downloads/). 

1. **Clone** the repo to your local computer

2. Open **command line as administrator** 
   - if you go to the repo location using file explorer you can type in 'cmd' in the file address bar 
   and this will pop up the command line at that location.
   - Or Navigate to the repo using the command _cd C:/path/to/local/repo_ 

3. **Create a virtual environment** by typing the following in the command prompt. Make sure you are at the top most level of the repo.

         py -m venv venv
4. **Activate virtual environment**

        venv\Scripts\activate.bat

5. Install the **requirements**. Don't upgrade pip, this might cause an error and you'll be left without pip. If this happens then just delete the venv folder and start over

         pip install -r requirements.txt
         
6. Clone the Quantum-Tomography python library into the resources folder
        
        cd C:/path/to/local/repo/resources
        git clone (Quantum-Tomography HTTPS link) your_folder_name

## Note
- The *main* branch of this repository is for use on the server and might not work perfectly on all IDEs. To run this application from an IDE, use the *development* branch

## Troubleshooting

- *'py' is not recognized*. 
  - Depending on how you downloaded python your PATH variable for python (the _py_ in this walkthrough) may be diffrent.
Other common names are _python_ or _python3_. Its whatever you type into the command prompt in order to start python. 
  Replace the _py_ with whatever your PATH variable for python is. Follow [this tutorial](https://www.educative.io/edpresso/how-to-add-python-to-path-variable-in-window) 
  if you can't figure out your python's PATH variable and you know for certain python is installed.

- *'pip' is not recognized*. 
  - pip is not defined as a PATH variable. Instead of just using *pip*
use *py -m pip*. It is rare but if you downloaded python in a weird way you may not have pip installed. You'll have to search for how to install pip on your computer.
  The process differs depending on if you're using PC/mac/ubuntu.
