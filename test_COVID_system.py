import unittest
import datetime
from data_access import PythonDataAccess
class TestCOVIDSystem(unittest.TestCase):
    def __init__(self,methodName) -> None:
        super().__init__(methodName=methodName)
        self.data_access=PythonDataAccess()

    def test_create_sick(self):
        """
        this function tests that a created sick is in the patients list
        """
        person=self.data_access.create_patient("052222222", "firstName", "surName", 1, datetime.datetime.now(),"e@.com", "Gaza","Gaz",14,14,102, True,  datetime.datetime.now())
        list_of_patients=self.data_access.read_list_of_patients()
        self.assertTrue(person in list_of_patients)

    def test_create_sick_in_site(self):
        self.data_access.create_patient("052222222", "firstName", "surName", 1, datetime.datetime.now(),"e@.com", "Gaza","Gaz",14,14,102, True,  datetime.datetime.now())
        # above is creating sick
        sick_in_site=self.data_access.create_sick_in_site(1,"Friend-Home",datetime.datetime.now(),"Gaza","Gas",3)
        print(sick_in_site.sick.firstName)
        list_of_sick_in_site=self.data_access.read_list_of_sick_in_site()
        self.assertTrue(sick_in_site in list_of_sick_in_site)

    def test_create_sick_encounter(self):
        self.data_access.create_patient("052222222", "firstName", "surName", 1, datetime.datetime.now(),"e@.com", "Gaza","Gaz",14,14,102, True,  datetime.datetime.now())
        sick_encounter=self.data_access.create_sick_encounter(1,"Gozal","Rahum","0524829321")
        list_of_patients=self.data_access.read_list_of_patients()
        self.assertTrue(sick_encounter in list_of_patients)

    def test_update_test_result(self):
        self.data_access.create_patient("052222222", "firstName", "surName", 1, datetime.datetime.now(),"e@.com", "Gaza","Gaz",14,14,102, True,  datetime.datetime.now())
        failed_update=self.data_access.update_test_result(1,1,4,datetime.datetime.now(),True) # with id of a non-existing person
        self.assertFalse(failed_update)
        success_update=self.data_access.update_test_result(1,1,1,datetime.datetime.now(),False) # with id of an existing person
        self.assertTrue(success_update)

    def test_update_sick_encounter_details(self):
        self.data_access.create_patient("052222222", "firstName", "surName", 1, datetime.datetime.now(),"e@.com", "Gaza","Gaz",14,14,102, True,  datetime.datetime.now())
        self.data_access.create_sick_encounter(1,"Gozal","Rahum","0524829321")
        updated_person=self.data_access.update_sick_encounter_details(1, 2,"first_name","sur_name",datetime.datetime.now(),"44444","mail@.com","city","street",4,3,2)
        list_of_patients=self.data_access.read_list_of_patients()
        self.assertTrue(updated_person in list_of_patients)



if __name__ == '__main__':
    unittest.main()