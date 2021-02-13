from abc import ABC, abstractmethod

class Interface_View(ABC):
    """
    This interface's goal is to enable future view changes.
    Today we implement this interface as a console, but in the future it might want
    the UI to be a web app or even a mobile app.  
    """
    @abstractmethod
    def show_help():
        """
        display the command list and their format
        """
        pass

class ViewConsole(Interface_View):
    @staticmethod
    def show_help():
        print("""
        1.	Create-sick <id> <firstname> <lastname> <birthdate DD/MM/YYYY> phone mail city street house-number apartment house-residents
            if the same id used more than once, the details of the last run will override the previous one

        2.	Add-route-site <id> <birthdate DD/MM/YYYY> <time hh:mm> <sitename>
        
        3.	Add-route-address <id> <birthdate DD/MM/YYYY> <time hh:mm> <sitename> <city> <street> <number>

        4.	Add-sick-encounter <sick-id> <firstname> <lastname> <phone>

        5.	Show-sick-encounter
            show a list of encounters where the person  details were not inserted yet, in the following format:
            encounter-id, sick-id, sick-firstname, sick-lastname, firstname lastname phone

        6.	Update-sick-encounter-details <encounter-id> <personid> <firstname> <lastname> <birthdate DD/MM/YYYY> <phone> <mail> <city> <street> <house-number> <apartment> <house-residents>
            if the same encounter-id used more than once, the details of the last run will override the previous one

        7.	Update-lab-test <labid> <testid> <personid> <date> <result>
            if the same labid and testid pairs are used more than once, the details of the last run will override the previous one

        8.	Show-new-sick
            will display a list of all sick people who were added since the last run of this command in the following format:
            id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents

        9.	Show-stat <[List of stats separated by , ]>
            stats options – sicks, healed, isolated, sick-per-city
            each printed stat will be in a format:
            ** BEGIN STATNAME ** 
            stat value(s)
            ** END STATNAME **

        10.	Show-person <personid>
            will display the person details and whether he is sick or not together with all his/her lab tests in the following format:
            id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents, source-sick(0 if unknown)
            ** LAB RESULT BEGIN **
            date labid testid result
            ** LAB RESULT END **

        11.	Show-person-route <personid>

        12.	Show-sick 
            will display all the sick people in the system in this format per line:
            id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents, source-sick(0 if unknown)
            
        13.	Show-isolated
            will display all the people in the system that are in isolation (14 days since they were reported or healed) in this format per line:
            id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents
        """)

    @staticmethod
    def get_option_input():
        return input('Please use a command')
