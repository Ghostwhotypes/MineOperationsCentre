from flask import Flask,render_template,request
import subprocess,platform

app=Flask(__name__)

def ping(host):
    flag='-n' if platform.system().lower()=='windows' else '-c'
    return subprocess.run(['ping',flag,'1',host],capture_output=True).returncode==0

@app.route('/',methods=['GET','POST'])
def index():
    rows=[{'ip':'','status':None}]
    if request.method=='POST':
        ips=request.form.getlist('ip')
        rows=[]
        for ip in ips:
            ip=ip.strip()
            st=None
            if ip:
                st=ping(ip)
            rows.append({'ip':ip,'status':st})
        if 'add' in request.form:
            rows.append({'ip':'','status':None})
    return render_template('index.html',rows=rows)

if __name__=='__main__':
    app.run(debug=True)
