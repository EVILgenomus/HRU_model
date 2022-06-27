# HRU_model
Simple HRU-model of object-subject access which ralized on Python 3

Call HRU_model.py with params from console.
main_fs.txt - there are main FS which can be choosen

Params: 

init

  For creating new file system with base user "root"

change-fs <name of FS

  changing FS to other

create-user <login> <password>

  For creating a new user in your fs with login and password

create-object <name (without .TXT!)> <text or nothing>

  For creating a new object in your fs with name and some content (optionally)

read-object <name (without .TXT!)>

  For reading from file in your fs with name

write-object <name (without .TXT!)> <text>

  For writing to object in your fs with name and some content

remove-user <login>

  For deleting user and data about him

remove-object <name (without .TXT!)>

  For deleting object and data about this

change-rights <user> <file> <rights (r/w/o or combination)>

  For changing rights for access by user to object for owning, reading or writing
