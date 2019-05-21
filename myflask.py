from flask import Flask, render_template, request, jsonify
from Get_Data import get_data, build_connection, run_sql
import random
import string
#from OpenSSL import SSL

#First, create a flask class object we use to run our program
app = Flask(__name__)

##This section defiles my SSL certs so that I correctlty can run HTTPS on my site.

#context = SSL.Context(SSL.SSLv23_METHOD)
cer = 'fireanalytics-dev.crt'
key = 'testcert.key'

#set the route to the first place you go.  So when I go to the site http://0.0.0.0:500 I will render my Index.html template
@app.route('/')
def index():
    return render_template('Index.html')


### This is another page in my web application.  it will get used when some clicks the button in my application.
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=str)
    hashvalue = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    #r = test_1()
    #print r
    data = get_data(a, hashvalue)
    data = [tuple(x) for x in data.to_records(index=True)]
    cur, conn = build_connection();
    run_sql(cur, conn, data);
    print jsonify(result=hashvalue)
    return jsonify(result=hashvalue)



if __name__=="__main__":
	context = (cer,key)
	app.run() #, ssl_context=context)
#	app.run()
#	app.run(host='0.0.0.0', port=5000)
