import re,xml.etree.ElementTree as ET

def get_multiple_inputs():
    number = input("How Many XML inputs you want to choose: ")
    i=0
    choice_list=[]
    choice_values_list=[]
    while i<int(number):
        choice = input("Enter the XML Element Name: ")
        choice_value = input("Enter the new Value: ")
        choice_list.append(choice)
        choice_values_list.append(choice_value)
        i+=1
    return choice_list, choice_values_list

def changeElements(payload,elements,new_values):
    i=0
    while i<len(elements):
        payload=re.sub(rf'<{elements[i]}>(.*?)</{elements[i]}>',f'<{elements[i]}>{new_values[i]}</{elements[i]}>',payload)
        i+=1
    return payload
    # Use a regular expression to find the element
    #return re.sub(rf'<{element}>(.*?)</{element}>',f'<{element}>{new_value}</{element}>',payload)
    #return re.sub(r'<SERVER-ADDRESS>(.*?)</SERVER-ADDRESS>','<SERVER-ADDRESS>5.6.7.8</SERVER-ADDRESS>',payload)