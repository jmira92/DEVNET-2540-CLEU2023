import warnings,api_handle,menu_draw

warnings.filterwarnings("ignore")

def menu():
    print(menu_draw.title('Demo 1'))
    print(menu_draw.entrie('1 - Service Provisioning','( Node 5 -> Node 4 )'))
    print(menu_draw.entrie('2 - Service Migration','\t( Node 4 -> Node 3 )'))
    print(menu_draw.last_entrie('3 - Service Maintenance','\t( Add Node 4 )\t'))
    print(menu_draw.title('Demo 2'))
    print(menu_draw.entrie('4 - Custom Service Provision','( NTP )\t\t'))
    print(menu_draw.entrie('5 - NTP Service Provision/Maint','( Dynamic Inputs)'))
    print(menu_draw.last_entrie('6 - L3VPN port Migration','( Dynamic Inputs)'))

    print(menu_draw.full_line())
    choice = input("Enter your choice: ")
    api_handle.call_option(choice)

if __name__ == "__main__":
    menu()