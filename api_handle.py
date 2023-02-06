import requests,time,xml_manipulation

base_nso_url = "http://198.18.134.28:8080/restconf/data/"
base_url = "https://198.18.134.219:30603/crosswork"
base_proxy = "/proxy/nso/restconf/data"
header=""
cnc_token=""

def api_call(method,url,headers,payload_content,payload_option):
    if(payload_option=="file"): 
        payload=get_payload(payload_content)
    else: 
        payload=payload_content
    
    response = requests.request(method, url, headers=headers, data=payload,  verify=False)
    #print("API call status code: ", response.status_code,"",response.text)
    return response

def get_payload(filename):
    with open(filename+".xml", "r") as xml_file:
        xml_data = xml_file.read()
    return xml_data

def auth():
    print("Authentication in Progress!!!")
    url = base_url+"/sso/v1/tickets"
    payload = "username=admin&password=cRo55work!"
    headers = { 'Content-Type' : 'application/x-www-form-urlencoded','Accept' : 'text/plain'}
    cnc_ticket = api_call("POST",url,headers,payload,"embded")

    url = base_url+"/sso/v1/tickets" + "/" + str(cnc_ticket.text)
    payload = "service=https://198.18.134.219:30603/app-dashboard"
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    cnc_token = api_call("POST",url,headers,payload,"embded")
    print("Authentication Successfull!!!")

    global header
    header = {
    'Content-Type': 'application/yang-data+xml',
    'Accept': 'application/yang-data+xml',
    'Authorization': "Bearer "+cnc_token.text
    }
    return cnc_token

def call_option(choice):
    global cnc_token
    if(cnc_token==""):
        cnc_token = auth()
    if(choice=="1"): service_provisioning()
    if(choice=="2"): service_migration()
    if(choice=="3"): service_maintenance()
    if(choice=="4"): ntp_provision()
    if(choice=="5"): ntp_dynamic_provision_maintenance()
    if(choice=="6"): l3vpn_port_migration()

def ntp_dynamic_provision_maintenance():
    print("Provisioning NTP dynamic")
    choice_list,choice_values_list = xml_manipulation.get_multiple_inputs()    
    print("Provisioning NTP dynamic values")
    url = base_url+base_proxy
    payload = get_payload('prov-NTP')    
    payload= xml_manipulation.changeElements(payload,choice_list,choice_values_list)
    response = api_call("PATCH",url,header,payload,'dynamic')
    if response:
        print("NTP Provisioning is sucessfull !!!")
    else:
        print("NTP Provisioning failed !!!")

def l3vpn_port_migration():
    print("L3VPN port Migration")
    choice_list,choice_values_list = xml_manipulation.get_multiple_inputs()    
    print("Provisioning")
    url = base_url+base_proxy+"/ietf-l3vpn-ntw:l3vpn-ntw/vpn-services/vpn-service=vpn-101"
    
    payload = get_payload('mig-vpn-service')    
    payload= xml_manipulation.changeElements(payload,choice_list,choice_values_list)

    response = api_call("PUT",url,header,payload,'dynamic')
    if response:
        print("L3VPN Port Migration is sucessfull !!!")
    else:
        print("L3VPN Port Migration failed !!!")

def ntp_provision():
    print("Provisioning")
    url = base_url+base_proxy
    response = api_call("PATCH",url,header,'prov-NTP','file')
    if response:
        print("NTP Provisioning is sucessfull !!!")
    else:
        print("NTP Provisioning failed !!!")

def service_migration():
    print("Migrating the L3VPN Service from Node-4 to Node-3 " )

    url = base_url+base_proxy+"/ietf-l3vpn-ntw:l3vpn-ntw/vpn-services/vpn-service=vpn-101"
    response = api_call("PUT",url,header,'mig-vpn-service','file')

    if response:
        print("Migration of L3VPN Service from Node-4 to Node-3 is completed.")
    else:
        print("Migration Activity Failed")
        print("Reason :" + str(response.text))

def service_maintenance():
    print("Adding Node-4 to L3VPN Service : In Progress")

    url = base_url+base_proxy+"/ietf-l3vpn-ntw:l3vpn-ntw/vpn-services/vpn-service=vpn-101"
    response = api_call("PATCH",url,header,'maint-vpn-service','file')

    if response:
        print("Node-4 has been added to the L3VPN Service!!\nMaintainenace Activity Successfull")
    else:
        print("Maintainence Activity Failed")
        print("Reason :" + str(response.text))

def service_provisioning():
    print("On-Demand Next-Hop provisioning in Progress!!")
    
    url = base_url+base_proxy
    response = api_call("PATCH",url,header,'prov-1-sr-odn','file')

    if response:
        print("The Provisioning of On-Demand Next-Hop is complete!!")
        print("Provisioning a route-policy is in Progress!!")

        url = base_url+base_proxy
        response = api_call("POST",url,header,'prov-2-l3vpn-route-policy','file')

        if response:
            print("The Provisioning of Route-Policy is complete!!")
            ##3
            print("Creating a L3VPN Profile")

            url = base_url+base_proxy
            response = api_call("PATCH",url,header,'prov-3-l3vpn-ntw','file')

            if response:
                print("L3VPN Profile is created!!")
                print("Final step in L3VPN Provisioning has started!!")
                print("Provisioning L3VPN in between Node-5 and Node-4!!")

                url = base_url+base_proxy+"/ietf-l3vpn-ntw:l3vpn-ntw/vpn-services"
                response = api_call("POST",url,header,'prov-4-vpn-service','file')

                if response:
                    print("L3VPN Provisioning is Complete!!")
                else:
                    print("L3VPN Provisioning has Failed")
            else:
                print("Creating a L3VPN profile has Failed")    
        else:
            print("The  Provisioning of Route-Policy has Failed")
    else:
        print("The Provisioning of On-Demand Next-Hop has Failed")