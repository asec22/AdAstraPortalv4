import csv
from csv import DictReader
from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def readFile(file,index):
    file_dict={}
    file_path="/pythonprograms/testapp4/static/"+file
    x=0
    with open(file_path, 'r') as f:
        dict_reader = DictReader(f)
        data_dict= list(dict_reader)    
    for items in data_dict:
        aname=data_dict[x].get(index)
        file_dict[aname]=items
        x+=1
    return [file_dict,data_dict,file_path,file]

def writeFile(dnary,file):
    new_dict=dnary
    headers=list(new_dict[0].keys())
    dpath=file
    with open(dpath,'w',newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(new_dict)
    return dpath

credentials=readFile('credentials.csv','uname')

@app.route("/")
def index():
    user=session.get("name")
    password=session.get('password')
    pass_check=credentials[0].get(user,{}).get('pd')
    rol=credentials[0].get(user,{}).get('Role')
    if not user:
        return redirect(url_for('login'))
    return render_template('index.html',usr=user,pwd=pass_check,rl=rol)

@app.route("/login", methods=["POST", "GET"])
def login():
    user=session.get("name")
    password=session.get('password')
    if request.method == "POST":
        session['name'] = request.form.get('uname')
        session['password']=request.form.get('passwd')
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    user=session.get("name")
    password=session.get('password')
    session["name"] = None
    session['password']= None
    pass_check = "Logout"
    rol= None
    return redirect(url_for('index',usr=user,pwd=pass_check,rl=rol))

@app.route("/portal", methods=["POST", "GET"])
def portal():
    if request.method == "POST":
        patient=request.form["pnumber"]
        return redirect(url_for("patient",pat=patient))
    else:
        return render_template("portal.html")

@app.route("/<pat>")
def patient(pat):
    mypatients=readFile('patientlist.csv','PatientID')
    patient_id=pat
    patient_name=mypatients[0].get(patient_id,{}).get("Name")
    patient_age=mypatients[0].get(patient_id,{}).get("Age")
    patient_gender=mypatients[0].get(patient_id,{}).get("Gender")
    return render_template("patient.html",pname=patient_name, page=patient_age, pgender=patient_gender,npat=False)       

@app.route('/newpatient', methods=["POST","GET"])
def newpatient():
    mypatients=readFile('patientlist.csv','PatientID')
    if request.method=="POST":
        df1=mypatients[1]
        d_file=mypatients[3]
        f_path=mypatients[2]
        user=session.get("name")
        y=len(df1)
        pat_string="Patient"+str(y+1)
        p_name=request.form['pat_name']
        p_age=request.form['pat_age']
        p_gender=request.form['pat_gender']
        p_notes=request.form['pat_notes']
        newpatient={"PatientID":pat_string,"Name":p_name,"Age":p_age,"Gender":p_gender,"Notes":p_notes,"Doctor":user}
        df1.append(newpatient)    
        filestr=writeFile(df1,f_path)
        return render_template("patient.html",patid=pat_string,pname=p_name,page=p_age,pgender=p_gender,npat=True)
    else:
        return render_template("newpatient.html")
        
if __name__=="__main__":
    app.run(debug=True)