# COVID_system_MVC
Designed and Implemented in Python by Ram Rokach and Eden Nathan.
# MVC
This project was implemented with the MVC design-artitechtual pattern:
    1. M - Model: holds entity classes.
    2. V - View: holds the "UI" implementation.
    3. C - Controller: responsible of organizing and manipulating command flow.
This way we accmoplished a loosly-coupled and generic design for our system. This means we gain minimum dependency between the components. It allows fast-modification of one of the components with minimum changes on other components.For example, in order to change the View from Console to Web-App, all there's to do is to implement the View-Interface functions with a web app and change the main function. 
# Data Access Layer
This project was implemented with the Data Access Layer approach:
In order to seperate our data-management from our business-logic(Controller) and presentation code (View), we use DAL - this way, if we have to change data stores, we don't end up rewriting the whole system. For example, in order to change the Data-Management system from Python lists to MySQL, all we need to do is to implement the DAL interface as a MySql class and change the main function.

# UML

![UML](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

