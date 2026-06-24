from pathlib import Path
import os



def createfile():
    try:
        name=input("please tell name of the file :-")
        path=Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data=input("what you want to write :-")
                fs.write(data)
            print("file created successfully")
        else:
            print("file already exists")
    except Exception as err:
        print("an error occured as {err}")

def readfile():
    try:
        name=input("please tell your file name :-")
        path=Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content=fs.read()
                print(f"your file content is \n {content}")
        else:
            print("error no such file exists")
    except Exception as err:
        print("an error occured as {err}")

def writefile():
    pass

def deletefile():
    pass    

print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for writing to a file")
print("press 4 for deleting a file")

a=int(input("\ntell your response :-"))
if a==1:
    createfile()
if a==2:
    readfile()
if a==3:
    writefile()
if a==4:
    deletefile()