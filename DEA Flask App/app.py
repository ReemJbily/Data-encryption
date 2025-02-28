import os
from flask import Flask, flash, request, redirect, render_template,request
from werkzeug.utils import secure_filename
from flask import jsonify
from werkzeug.exceptions import BadRequest
from flask_cors import CORS
import DEA

from DataBaseConnection import DataBase

app = Flask(__name__)
CORS(app)

#start cofiguration
app.secret_key = os.urandom(24)  # Generate a random 192-bit key
#end configuration



#database connection 
db=DataBase()


data = {"encrypted_file": "00000",
        "original_text":"no text"}  

def allowed_file(filename):
    return '.txt' in filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):            
            filename = secure_filename(file.filename)            
            db.insertValues(filename,file.read().decode('utf-8'))            
    return render_template('index.html')

#helper methods
def string_to_bytes(string):
    return bytes(string,'utf-8')

def byte_to_string(b):
    return b.decode('utf-8')

def ecryption_method(original_data):
    encryption_type = 'AES' 
    key_size = 256  # AES-256 for strong security, or RSA-2048/4096 for asymmetric encryption

    # Instantiate DEA with user-chosen encryption type
    dea = DEA.DEA(encryption_type=encryption_type, key_size=key_size)
    encrypted_data = dea.aes_encrypt(original_data)
    return encrypted_data
\


def optimize_method(original_data):
    encryption_type = 'RSA' 
    key_size = 1024  # AES-256 for strong security, or RSA-2048/4096 for asymmetric encryption

    # Instantiate DEA with user-chosen encryption type
    dea = DEA.DEA(encryption_type=encryption_type, key_size=key_size)
    opt_encrypted_data = dea.rsa_encrypt(original_data)
    return opt_encrypted_data    
#end 

@app.route('/send', methods=['GET'])
def encrypt(): 
    #this is the encryption method      
    data['original_text']=db.readFile()
    text=string_to_bytes(str(data['original_text']))
    encrypted_data=ecryption_method(text)
    enc_text=byte_to_string(encrypted_data)  
    data["encrypted_file"]=enc_text  
    db.deleteContent()
    return jsonify(data)


@app.route('/optimize', methods=['GET'])
def optimize():  
    #optimization method uses RSA as it is more efficient 
    text=string_to_bytes(str(data['original_text'])) 
    opt_encrypted_data=optimize_method(text)
    opt_enc_text=byte_to_string(opt_encrypted_data)  
    data["encrypted_file"]=opt_enc_text 
    return jsonify(data)




if __name__ == '__main__':   
    app.run(debug=True)
