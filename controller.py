from model import *
from view import Interface_View
import sys
debug=False
if "-d" in sys.argv:
    debug=True

class Controller:
    def __init__(self, view:Interface_View):
        self.view = view
        self.list_of_patients = list[Person]
        self.list_of_sick_in_Site = list[SickInSite]
        self.list_of_tests = list[Test]
        pass

    def start(self):
        while True:
            option:list = self.view.get_option_input().split() # ["Create-sick" "id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
            if option[0] == 'Create-sick':
                self.create_sick(option[1:])
                self.view.create_sick()
            elif option[0] == 'Add-route-site':
                self.add_route_site(option[1:])
                self.view.add_route_site()
            elif option[0] == 'Add-route-address':
                self.add_route_site(option[1:])
                self.view.add_route_address()
            elif option[0] == 'Add-sick-encounter':
                self.add_sick_encounter(option[1:])
                self.view.add_sick_encounter()
            elif option[0] == 'Show-sick-encounter':
                result = self.show_sick_encounter()
                self.view.show_sick_encounter(result)
            elif option[0] == 'Update-sick-encounter-details':
                if self.update_sick_encounter_details(option[1:]):
                    self.view.update_sick_encounter_details()
                else:
                    self.view.operation_failed("There is no such encounter / missing details")
            elif option[0] == 'Update-lab-test':
                if self.update_lab_test(option[1:]):
                    self.view.update_lab_test()
                else:
                    self.view.operation_failed("No such test / missing details")
            elif option[0] == 'Show-new-sick':
                self.advanced_search()
            elif option[0] == 'Show-stat':
                self.advanced_search()
            elif option[0] == 'Show-person':
                self.advanced_search()
            elif option[0] == 'Show-person-route':
                self.advanced_search()
            elif option[0] == 'Show-sick':
                self.advanced_search()
            elif option[0] == 'Show-isolated':
                self.advanced_search()
            else:
                self.view.operation_failed()

    def create_sick(self,args:list): # args: ["id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
        self.list_of_patients.remove(self.find_person_by_id(args[4])) #removes the person in case id is shown twice
        home=Home(args[6],args[7],args[8],args[9],args[10])
        person=Person(args[4],args[1],args[2],args[0],args[3],args[5],home,sick=True, interviewed=True,isolation_begin_date=datetime.datetime.now().date)
        self.list_of_patients.append(person)
        if debug:
            print(person.firstName,"added to list_of_patients")

    def find_person_by_id(self, id:int):
        for person in self.list_of_patients:
            if id is person.id:
                return person

    def find_suspect_by_encounter_id(self, encounter_id:int):  # used to update a suspect's details
        for suspect in self.list_of_patients:
            if hasattr(suspect, 'encounter_id'):
                if suspect.encounter_id == encounter_id:
                    return suspect

    def add_route_site(self, args:list): # args: ["id" "01/04/2020" "10:00" "sitename" optional: "city" "street" "number"]
        date_time = datetime.datetime.strptime(args[1] + args[2], '%Y/%m/%d%H:%M')
        if len(args) == 4 :
            site = Site(args[3])
        else:
            address = Address(args[4], args[5], args[6])
            site = Site(args[3], address)
        route_site = SickInSite(self.find_person_by_id(args[0]), site, date_time)
        self.list_of_sick_in_Site.append(route_site)

    def add_sick_encounter(self, args:list): # "sick-id" "firstname" "lastname" "phone"
        sick = self.find_person_by_id(args[0])
        if not sick:
            self.view.operation_failed("No infector, wrong encounter details")
            return
        suspect = Suspect(sick, args[3], args[1], args[2])
        self.list_of_patients.append(suspect)

    def show_sick_encounter(self): # encounter-id, sick-id, sick-firstname, sick-lastname, firstname lastname phone
        list_to_return = []
        suspects = [x for x in self.list_of_patients if x.id is None]
        for suspect in suspects:
            string = str(suspect.encounter_id) + " " + str(suspect.infector.id) + " " + suspect.infector.firstName +\
            " " + suspect.infector.surName + " " + suspect.firstName + " " + suspect.surName + " " + suspect.phone
            list_to_return.append(string)

        return list_to_return

    def update_sick_encounter_details(self, args:list): # encounter-id personid firstname lastname birthdate phone mail city street house-number apartment house-residents 
        encounter_id = args[0]
        suspect = self.find_suspect_by_encounter_id(encounter_id)
        if not suspect:
            return False
        suspect.id = args[1]
        suspect.firstName = args[2]
        suspect.surName = args[3]
        suspect.birthdate = args[4]
        suspect.phone = args[5]
        suspect.mail = args[6]
        suspect.home = Home(args[7], args[8], args[9], args[10], args[11])
        return True

    def update_lab_test(self, args:list): # labid testid personid date result 
        for lab_test in self.list_of_tests:
            if (lab_test.test_id == args[1] and lab_test.lab.lab_id == args[0] and lab_test.person.id == args[2]):
                lab_test.update_test_result(args[4], args[3])
                return True
        return False











    def get_active_suspect(self) -> list:
        """
        :return: a list of suspects who had no tests
        """
        return [x for x in self.list_of_patients if x.sick is None]
