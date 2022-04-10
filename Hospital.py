from flask import Flask, render_template,request
import sqlite3

from werkzeug.utils import redirect

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

@user.route('/',methods=['GET','POST'])
def Dashboard():
    if request.method == 'POST':
        getuname = request.form["urname"]
        getPass = request.form["pass"]
        if getuname == "admin" and getPass == "1234":
            return redirect("/dashboard")
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
            print("Data inserted successfully")
        except Exception as err:
            print("Exception occured",err)
    return render_template("newregister.html")

@user.route('/search',methods=['GET','POST'])
def Search_patient():
    if request.method == "POST":
        getMobile = request.form["number"]
        cursor = data.cursor()
        count = cursor.execute("select * from patient where Mobnumber="+getMobile)

        result = cursor.fetchall()
        if result is None:
            print("Mobile number is not registered")
        else:
            return render_template("search.html", search=result,status=True)
    else:
        return render_template("search.html",search=[],status=False)

@user.route('/delete',methods=['GET','POST'])
def Delete_patient():
    if request.method =="POST":
        getMobile = request.form["number"]
        data.execute("delete from patient where Mobnumber="+getMobile)
        data.commit()
        print("Deleted Successfully")
        return redirect("/viewall")
    return render_template("delete.html")

@user.route('/viewall')
def View_patient():
    cursor = data.cursor()
    count = cursor.execute("select * from patient")

    result = cursor.fetchall()
    return render_template("view.html", details=result)

@user.route('/update',methods=['GET','POST'])
def Update_patient():
    global getNmob
    if request.method == "POST":
        getNmob = request.form["unumber"]
        return redirect("/updatedetails")
    else:
        return render_template("update.html")

@user.route('/updatedetails',methods=['GET','POST'])
def Update_details():
    if request.method == "POST":
        getName = request.form["newname"]
        getAge = request.form["newage"]
        getAddress = request.form["newaddress"]
        getDob = request.form["newdob"]
        getPlace = request.form["newplace"]
        getPincode = request.form["newpincode"]
        try:
            data.execute("update patient set Name='"+getName+"',age="+getAge+",address='"+getAddress+"',\
            dob='"+getDob+"',place='"+getPlace+"',pincode="+getPincode+" where Mobnumber="+getNmob+" ")
            data.commit()
            print("Data updated successfully")
            return redirect('/viewall')
        except Exception as err:
            print("Exception occured",err)
        return redirect("/viewall")
    else:
        return render_template("updatedetails.html")

if __name__==("__main__"):
    user.run()