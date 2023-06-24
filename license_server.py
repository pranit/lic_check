from flask import Flask, request, send_file
import hashlib
from datetime import datetime

app = Flask(__name__)

def read_strings_from_file(file_path):
    with open(file_path, 'r') as file:
        strings = file.read().splitlines()
    return strings

@app.route('/validate', methods=['POST'])
def validate_string():
    input_string = request.form.get('input_string')
    if input_string is None:
        return "Missing input string", 400
    
    #Log IP address and request 
    ip_address = request.remote_addr
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = '/tmp/license.log'
    with open(filename, 'a') as file:
        file.write("Time: {}\nReqeuster_IP: {}\nInput: {}\n\n".format(current_time, ip_address, input_string))

    # Read strings from the file
    file_path = 'license_string.txt'
    strings = read_strings_from_file(file_path)

    # Check if the input string is present in the file
    if input_string not in strings:
        return "Input string not found in the file", 400

    # Calculate SHA256 hash
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

    # Create a file containing the hash
    filename = 'hash.txt'
    with open(filename, 'w') as file:
        file.write(sha256_hash)

    return send_file(filename, attachment_filename='hash.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
