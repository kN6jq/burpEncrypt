from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json

app = Flask(__name__)

key = b"2y111mf7811pbr1f"

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(encoded_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = base64.b64decode(encoded_text.encode('utf-8'))
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8').encode('utf-8')

@app.route('/encode', methods=['POST'])
def encode():
    text = request.form.get('dataBody')  # 获取  post 参数 必需  
    headers = request.form.get('dataHeaders')  # 获取  post 参数  可选  
    if not text:
        return jsonify({"error": "Missing 'str' parameter"}), 400
    encrypted_text = encrypt(text, key)
    return jsonify({"data": encrypted_text})

@app.route('/decode', methods=['POST'])
def decode():
    encrypted_text = request.form.get('dataBody')  # 获取  post 参数 必需
    # return encrypted_text  
    if not encrypted_text:
        return jsonify({"error": "Missing 'str' parameter"}), 400
    if "data" in encrypted_text:  
        encrypted_text = json.loads(encrypted_text)['data']  
        decrypted_text = decrypt(encrypted_text, key)
        return decrypted_text
    else:  
        return encrypted_text

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug  
    app.run(host="0.0.0.0",port="8888")
