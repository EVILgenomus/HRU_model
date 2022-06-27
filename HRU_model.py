from array import ArrayType
from sys import argv
from time import sleep
import os
import hashlib as hl

main_fs=open("main_fs.txt", "r")
fs_name = main_fs.readline()
main_fs.close()
matr_f="matrix.txt"
hash_r=""

incorrect = "Incorrect login or password!!!"
# 1 - true
# 0 - not true


def main():
    try:
        if argv[1]=="help":
            help()
        if argv[1]=="init":
            init()
        if argv[1]=="change-fs":
            try: change_fs(argv[2])
            except: print("!!! Please, enter name of FS which must be activated !!!")
        if argv[1]=="create-user":
            try: create_user(argv[2], argv[3])
            except: print("Using: create-user <login> <password>")
        if argv[1]=="create-object":
            try: create_object(argv[2], argv[3])
            except: 
                try: create_object(argv[2])
                except: print("Using: create-object <name (without .TXT!)> <text or nothing>")
        if argv[1]=="read-object":
            try: read_object(argv[2])
            except: print("Using: read-object <name (without .TXT!)>")
        if argv[1]=="write-object":
            try: write_object(argv[2], argv[3])
            except: print("Using: write-object <name (without .TXT!)> <text>")
        if argv[1]=="remove-user":
            try: remove_user(argv[2])
            except: print("Using: remove-user <login>")
        if argv[1]=="remove-object":
            try: remove_object(argv[2])
            except: print("Using: remove-object <name (without .TXT!)>")
        if argv[1]=='change-rights':
            try: change_rights(argv[2], argv[3], argv[4])
            except: print("Using: remove-object <user> <file> <rights (r/w/o or combination)>")
    except: print("use this script with \"help\" as parametr:\n<somescript>.py help")    
            #create-user <login> <password>
    #create-object <name> <object-content>
    #read-object <name>
    #write-object <name> <object-content>
    #remove-user <login>
    #remove-object <name>

def init():
    fs_name = input(">: Let's give name for your new FS: ")
    while fs_name in os.listdir():
        fs_name = input(">: This FS already exists! You must to choose other name: ")
    os.mkdir(fs_name)
    main_fs = open("main_fs.txt", "w")
    main_fs.write(fs_name)
    main_fs.close()

    pswd = input(">: Password:")
    m_file = open(fs_name+"\\"+matr_f, "w")
    ufile = open(fs_name+"\\"+"root.txt", "w")
    sha_pass = hl.sha1(pswd.encode('utf-8'))

    ufile.write(sha_pass.hexdigest())
    m_file.write("root.txt;\nroot;r;")
    m_file.close()
    ufile.close()


def change_fs(fs_arg):
    main_fs = open("main_fs.txt", "w")
    main_fs.write(fs_arg)
    main_fs.close()


def authenticate(log, passwd):
    if log+".txt" in os.listdir(fs_name):
        file_pswd = open(fs_name+"\\"+log+".txt")
        line=file_pswd.readline()
        if  line == hl.sha1(passwd.encode('utf-8')).hexdigest():
            return 1
        else: return 0
    else: return 0


def obj_create_handle(name, inp_text=None):
    matrix=parse_matrix()
    if name not in matrix["fs_objects"]:
        matrix["fs_objects"].append(name+".txt")
        for x in matrix["fs_subjects"]:
            matrix["fs_subjects"][x].append(" ")
    save_matrix(matrix)
    new_file = open(fs_name+"\\"+name+".txt", "w")
    if inp_text!=None:
        new_file.write(inp_text)
    new_file.close()


def parse_matrix(): 
    m_file = open(fs_name + "\\"+ matr_f, "r")
    ctr=0
    list_users=[]
    lines=m_file.readlines()
    #print(lines)
    for i in range(len(lines)):
        lines[i]=lines[i].replace('\n', '')
        lines[i]=lines[i][:-1]
        if lines[i]!="":
            list_users.append(lines[i])
    m_file.close()
    matrix={"fs_objects" : list_users[0].split(";")}
    fs_subjects=list_users[1:]
    matrix["fs_subjects"]=dict()
    for x in fs_subjects:
        tmp=x.split(";")
        matrix["fs_subjects"][tmp[0]]=tmp[1:]
    #print(matrix)
    return matrix


def save_matrix(matrix):
    m_file = open(fs_name + "\\"+ matr_f, "r")
    m_file.close()
    m_file = open(fs_name + "\\"+ matr_f, "w")
    line=""
    for x in matrix["fs_objects"]:
        line+=x+";"
    #print(line)
    m_file.write(line+"\n")
    for x in matrix["fs_subjects"]:
        line=x+";"
        for y in matrix["fs_subjects"][x]:
            line+=y+';'
        #print(line)
        m_file.write(line+"\n")
    m_file.close()


def create_user(ulogin, upswd):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        obj_create_handle(ulogin, hl.sha1(upswd.encode('utf-8')).hexdigest())
        matrix=parse_matrix()
        if ulogin not in matrix["fs_subjects"]:
            matrix["fs_subjects"][ulogin]=[" " for x in matrix["fs_objects"]]
            matrix["fs_subjects"][ulogin][len(matrix["fs_subjects"][ulogin])-1]="r"
            matrix["fs_subjects"][log][len(matrix["fs_subjects"][ulogin])-1]="rwo"
            matrix["fs_subjects"]["root"][len(matrix["fs_subjects"][ulogin])-1]="rwo"
        else: print("Object already exists!")
        save_matrix(matrix)
    else: 
        print(incorrect)
    

def create_object(name, content=None):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        obj_create_handle(name, content)
        matrix=parse_matrix()
        if name+".txt" not in matrix["fs_objects"]:
            matrix["fs_subjects"][log][len(matrix["fs_subjects"][log])-1]="rwo"
            matrix["fs_subjects"]["root"][len(matrix["fs_subjects"]["root"])-1]="rwo"
        else: print("Object already exists!")
        save_matrix(matrix)
    else: 
        print(incorrect)


def read_object(name):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        matrix=parse_matrix()
        if name+".txt" in matrix["fs_objects"]:
            if "r" in matrix["fs_subjects"][log][matrix["fs_objects"].index(name+".txt")]:
                ufile=open(fs_name+"\\"+name+".txt", "r")
                print(">===")
                print(*ufile.readlines())
                print(">===")
                ufile.close()
            else: print("You don't have permission!")
        else: print("Object not exists!")
    else: 
        print(incorrect)

def write_object(name, content):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        matrix=parse_matrix()
        if name+".txt" in matrix["fs_objects"]:
            if "w" in matrix["fs_subjects"][log][matrix["fs_objects"].index(name+".txt")]:
                ufile=open(fs_name+"\\"+name+".txt", "w")
                ufile.write(content)
                ufile.close()
                print("SUCCESS!")
            else: print("You don't have permission!")
        else: print("Object not exists!")
    else: 
        print(incorrect)


def remove_user(ulogin):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        matrix=parse_matrix()
        if ulogin+".txt" in matrix["fs_objects"]:
            if "o" in matrix["fs_subjects"][log][matrix["fs_objects"].index(ulogin+".txt")]:
                del matrix["fs_subjects"][ulogin]
                for x in matrix["fs_subjects"]:
                    del matrix["fs_subjects"][x][matrix["fs_objects"].index(ulogin+".txt")]
                del matrix["fs_objects"][matrix["fs_objects"].index(ulogin+".txt")]
                os.remove(fs_name+"\\"+ulogin+".txt")
                print("SUCCESS!")
            else: print("You don't have permission!")
        else: print("User not exists!")
        save_matrix(matrix)
    else: 
        print(incorrect)

def remove_object(name):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        matrix=parse_matrix()
        if name+".txt" in matrix["fs_objects"]:
            if "o" in matrix["fs_subjects"][log][matrix["fs_objects"].index(name+".txt")]:
                for x in matrix["fs_subjects"]:
                    del matrix["fs_subjects"][x][matrix["fs_objects"].index(name+".txt")]
                del matrix["fs_objects"][matrix["fs_objects"].index(name+".txt")]
                os.remove(fs_name+"\\"+name+".txt")
                print("SUCCESS!")
            else: print("You don't have permission!")
        else: print("Object not exists!")
        save_matrix(matrix)
    else: 
        print(incorrect)


def change_rights(login, name, rights):
    log = input("Login: ")
    passwd = input("Password: ")
    if authenticate(log, passwd):
        matrix=parse_matrix()
        ###
        if name+".txt" in matrix["fs_objects"]:
            if "o" in matrix["fs_subjects"][log][matrix["fs_objects"].index(name+".txt")]:
                matrix["fs_subjects"][login][matrix["fs_objects"].index(name+".txt")]=rights
                print("SUCCESS!")
            else: print("You don't have permission!")
        ###
        else: print("Object not exists!")
        save_matrix(matrix)
    else: 
        print(incorrect)

def help():
    print("> init")
    print("\tFor creating new file system with base user \"root\"")
    print("> change-fs <name of FS>")
    print("\tchanging FS to other")
    print("> create-user <login> <password>")
    print("\tFor creating a new user in your fs with login and password")
    print("> create-object <name (without .TXT!)> <text or nothing>")
    print("\tFor creating a new object in your fs with name and some content (optionally)")
    print("> read-object <name (without .TXT!)>")
    print("\tFor reading from file in your fs with name")
    print("> write-object <name (without .TXT!)> <text>")
    print("\tFor writing to object in your fs with name and some content")
    print("> remove-user <login>")
    print("\tFor deleting user and data about him")
    print("> remove-object <name (without .TXT!)>")
    print("\tFor deleting object and data about this")
    print("> change-rights <user> <file> <rights (r/w/o or combination)>")
    print("\tFor changing rights for access by user to object for owning, reading or writing")

main()


# - create-object <name> <object-content>
# - read-object <name>
#write-object <name> <object-content>
#remove-user <login>
#remove-object <name>



#print(parse_matrix())
#save_matrix(parse_matrix())