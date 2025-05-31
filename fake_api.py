from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/odeme", methods=["POST"])
def odeme():
    data = request.json
    if all(k in data for k in ("kart", "skt", "cvc", "tutar")):
        return jsonify({"durum": "başarılı", "mesaj": f"{data['tutar']} TL tutarında ödeme alındı(sahte)."})
    return jsonify({"durum": "hata", "mesaj": "Eksik veya hatalı veri."}), 400

app.run(port=5000)
    