from flask import Flask, render_template,request
import sqlite3
data = sqlite3.connect("hospital.db",check_same_thread=False)
table = data.execute("select name from sqlite_master where type='table' and name= 'patient' ").fetchall()
if table!=[]:
    print("Table already exists")

else:
    data.execute('''create table patient(
                                    id integer primary key autoincrement,
                                    Name text,
                                    Mobnumber integer,
                                    age integer,
                                    address text,
                                    dob text,
                                    place text,
                                    pincode integer     
                                ); ''')
    print("Table created")
user = Flask(__name__)

@user.route('/')
def Dashboard():
    return render_template("login.html")

@user.route('/dashboard',methods=['GET','POST'])
def Register():
    if request.method == "POST":
        getName = request.form["name"]
        getMobile = request.form["number"]
        getAge = request.form["age"]
        getAddress = request.form["address"]
        getDob = request.form["dob"]
        getPlace = request.form["place"]
        getPincode = request.form["pincode"]
        try:
            data.execute("insert into patient(Name,Mobnumber,age,address,dob,place,pincode)\
                         values('"+getName+"',"+getMobile+","+getAge+",'"+getAddress+"','"+getDob+"','"+getPlace+"',"+getPincode+")")
            data.commit()
            print("Data inserted successfilly")
        except Exception as err:
            print("Exception occured",err)
    return render_template("newregister.html")

@user.route('/search')
def Search_patient():
    if request.method == "POST":
        getMobile = request.form["number"]
        cursor = data.cursor()
        count = cursor.execute("select * from patient where Mobnumber="+getMobile)

        result = cursor.fetchall()
        return render_template("view.html", details=result)

    return render_template("search.html")

@user.route('/delete')
def Delete_patient():
    if request.method =="POST":
        getMobile = request.form["number"]
        data.execute("delete from patient where Mobnumber="+getMobile)
        data.commit()
        print("Deleted Successfully")
    return render_template("delete.html")

@user.route('/viewall')
def View_patient():
    cursor = data.cursor()
    count = cursor.execute("select * from patient")

    result = cursor.fetchall()
    return render_template("view.html", details=result)

@user.route('/update')
def Update_patient():
    return render_template("update.html")

if __name__==("__main__"):
    user.run()