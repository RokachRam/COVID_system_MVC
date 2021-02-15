from model import *
from view import Interface_View

class Controller:
    def __init__(self, view:Interface_View):
        self.view = view
        self.list_of_patients = list[Person]
        self.list_of_sick_in_address = list[SickInAddress]
        self.list_of_tests = list[Test]
        pass

    def start(self):
        while True:
            option = self.view.get_option_input()
            if option == 'Create-sick':
                self.list_statistics()
            elif option == 'Add-route-site':
                self.display_three_cities_with_longest_names()
            elif option == 'Add-route-address':
                self.display_county_with_max_communities()
            elif option == 'Add-sick-encounter':
                self.display_locations_with_more_than_one_category()
            elif option == 'Show-sick-encounter':
                self.advanced_search()
            elif option == 'Update-sick-encounter-details':
                self.advanced_search()
            elif option == 'Update-lab-test':
                self.advanced_search()
             elif option == 'Show-new-sick':
                self.advanced_search()
            elif option == 'Show-stat':
                self.advanced_search()
            elif option == 'Show-person':
                self.advanced_search()
            elif option == 'Show-person-route':
                self.advanced_search()
            elif option == 'Show-sick':
                self.advanced_search()
            elif option == 'Show-isolated':
                self.advanced_search()
            else:
                self.view.operation_failed()


    def get_active_suspect(self) -> list:
        """
        :return: a list of suspects who had no tests
        """
        return [x for x in self.list_of_patients if x.sick is None]
