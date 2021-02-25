# COVID_system_MVC
This system was built to assist nurses and laborants by manipulating and controlling COVID-19's: {Sick, Sick-Encounters and Tests}.
Main funcionallity:
    1.The nurse can add sick people to the system, as well as sick encounters.
    2.The laborant can update test results and assosiate it to a person.
    3.Every system user can view sick, isolated, healed, and sick-per-city statistics.

The system was designed and implemented in Python by Ram Rokach and Eden Nathan in 2021.
# MVC
This project was implemented with the MVC design-artitechtual pattern:
    1. M - Model: holds entity classes.
    2. V - View: holds the "UI" implementation.
    3. C - Controller: responsible of organizing and manipulating command flow.
This way we accmoplished a loosly-coupled and generic design for our system. This means we gain minimum dependency between the components. It allows fast-modification of one of the components with minimum changes on other components.For example, in order to change the View from Console to Web-App, all there's to do is to implement the View-Interface functions with a web app and change the main function. 
# Data Access Layer
This project was implemented with the Data Access Layer approach:
In order to seperate our data-management from our business-logic(Controller) and presentation code (View), we use DAL - this way, if we have to change data stores, we don't end up rewriting the whole system. For example, in order to change the Data-Management system from Python lists to MySQL, all we need to do is to implement the DAL interface as a MySql class and change the main function.

# How to run?
Run the main file from the CLI, and give it a commands-file.txt (see HelpTest.txt for example): python main.py HelpTest.txt

# UML

![UML](https://github.com/dndn10/COVID_system_MVC/blob/main/githubUmlPic.png?raw=true)

