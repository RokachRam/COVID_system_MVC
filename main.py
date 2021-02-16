from controller import Controller
from data_access import PythonDataAccess
from view import ViewConsole
import sys
# main
if __name__ == "__main__":
    """
    How to run from CLI: python main.py <commands_file_path>
    command file example:
        HelpTest.txt: [every line is an individual command]
            Show-help
            Create-sick 123 Foo Bar 2020-04-26 012-3456789 sick@corona.com NewYork MyStreet 1 2 3
            Add-route-site 123 2020-04-26 11:00 Ruppin-college
            Add-route-site 123 2020-04-26 11:30 Supermarket
            Show-new-sick
    """
    if len(sys.argv)<2:
        exit('no commands file in argv')
    commands_file_path=sys.argv[1]
    view=ViewConsole(commands_file_path)
    container=PythonDataAccess()
    controller=Controller(view,container)
    controller.start()
