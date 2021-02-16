from abc import ABC, abstractmethod
from model import *
from typing import List
debug=True
class IDataAccess:
    """
    "DLA" == data layer access
    "CRUD"== Create, Read, Update and Delete
    This interface class is responsible of containing the different modules.
    it can be implemented using different databases (python,MySQL, MSSQL,etc..)
    """
    @abstractmethod
    def read_list_of_patients(self) -> list:
        pass
    @abstractmethod
    def read_list_of_sick_in_site(self)-> list:
        pass
    @abstractmethod
    def read_list_of_tests(self)-> list:
        pass
    
    @abstractmethod
    def get_suspect_by_encounter_id(self, encounter_id: int) -> Suspect:
        pass

    @abstractmethod
    def get_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int):
        pass

    @abstractmethod
    def create_patient(self, person:Person) -> bool:
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def create_sick_in_site(self,sick_in_site:SickInSite)-> bool:
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def create_test(self,test:Test)-> bool:
        """
        return True if success, else False
        """
        pass

    @abstractmethod
    def delete_patient_by_id(self, person_id) -> bool:
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def delete_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int)-> bool:
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def get_person_by_id(self, id: int) -> Person:
        pass


    


class PythonDataAccess(IDataAccess):
    def __init__(self) -> None:
        self.list_of_patients: List[Person] = [] 
        self.list_of_sick_in_Site : List[SickInSite]=[]
        self.list_of_tests : List[Test]=[]
    
    
    def create_patient(self, person:Person):
        if isinstance(person,Person):
            self.list_of_patients.append(person)
            return True
        return False
        
    def create_sick_in_site(self,sick_in_site:SickInSite):
        if isinstance(sick_in_site,SickInSite):
            self.list_of_sick_in_Site.append(sick_in_site)
            return True
        return False

    def create_test(self,test:Test):
        if isinstance(test,Test):
            self.list_of_tests.append(test)
            return True
        return False

    def read_list_of_patients(self):
        return self.list_of_patients

    def read_list_of_sick_in_site(self):
        return self.list_of_sick_in_Site

    def read_list_of_tests(self):
        return self.list_of_tests


    def delete_patient_by_id(self, person_id) -> bool:
        for person in self.list_of_patients:
            if person.id == person_id:
                self.list_of_patients.remove(person)
        return True 

    def delete_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int)-> bool:
        for test in self.list_of_tests:
            if test.test_id == test_id and test.lab_id == lab_id:
                self.read_list_of_tests.remove(test)
        return True

    def get_person_by_id(self, id: int) -> Person:
        for person in self.list_of_patients:
            if id == person.id:
                return person

    def get_suspect_by_encounter_id(self, encounter_id: int) -> Suspect:
        for suspect in self.list_of_patients:
            if hasattr(suspect, 'encounter_id'):
                if suspect.encounter_id == encounter_id:
                    return suspect

    def get_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int):
        for test in self.list_of_tests:
            if test.test_id == test_id and test.lab_id == lab_id:
                return test