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
                self.display_locations_with_more_than_one_category()
            elif option[0] == 'Show-sick-encounter':
                self.advanced_search()
            elif option[0] == 'Update-sick-encounter-details':
                self.advanced_search()
            elif option[0] == 'Update-lab-test':
                self.advanced_search()
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

    def find_person_by_id(self, id:int): # used to override person in case of repetition
        for person in self.list_of_patients:
            if id is person.id:
                return person

    def add_route_site(self, args:list): # args: ["id" "01/04/2020" "10:00" "sitename" optional: "city" "street" "number"]
        date_time = datetime.datetime.strptime(args[1] + args[2], '%Y/%m/%d%H:%M')
        if len(args) == 4 :
            site = Site(args[3])
        else:
            address = Address(args[4], args[5], args[6])
            site = Site(args[3], address)
        route_site = SickInSite(self.find_person_by_id(args[0]), site, date_time)
        self.list_of_sick_in_Site.append(route_site)


    def get_active_suspect(self) -> list:
        """
        :return: a list of suspects who had no tests
        """
        return [x for x in self.list_of_patients if x.sick is None]
