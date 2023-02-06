def new_line():
    return '|\t\t\t\t\t\t\t\t|'

def full_line():
    return '-----------------------------------------------------------------'

def entrie(choice,description):
    return '|\t'+choice+'\t'+description+'\t|'

def last_entrie(choice,description):
    return entrie(choice,description)+'\n'+new_line()

def title(name):
    total = full_line()
    total+='\n|\t\t\t\t'+name+'\t\t\t\t|\n'
    total+=new_line()
    return total