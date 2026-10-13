import socket
from flask import Flask, render_template_string, request, jsonify
from config import WORKERS, WEB_SERVER_PORT

app = Flask(__name__)

DASHBOARD_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Distributed Calculator</title>
    <style>
        body{background:#020617; margin:0; font-family:'Segoe UI',sans-serif; text-align:center; color:white;}
        .title{font-size:36px; font-weight:900; margin-top:30px;}
        .sub{color:#22d3ee; font-size:14px; margin-bottom:20px;}
        .card{background:linear-gradient(180deg, #1e3a5f 0%, #0f172a 100%); width:480px; margin:0 auto; border-radius:24px; padding:30px; border:1px solid #1e293b;}
        .nodes{display:flex; gap:10px; justify-content:center; margin-bottom:20px;}
        .pill{padding:6px 12px; font-size:11px; border-radius:20px; background:#0f172a; border:1px solid #334155; color:#94a3b8;}
        .pill.active{background:#052e16; color:#4ade80; border-color:#16a34a; box-shadow:0 0 10px #22c55e;}
        .inputs input{background:#020617; border:1px solid #1e293b; color:white; width:80%; padding:12px; border-radius:10px; font-size:20px; text-align:center; margin-bottom:10px; outline:none;}
        .btns{display:flex; gap:10px; justify-content:center; margin-top:10px;}
        .btns button{flex:1; padding:12px 0; border:none; border-radius:10px; font-weight:bold; cursor:pointer;}
        .b1{background:#4ade80;} .b2{background:#fb7185;} .b3{background:#22d3ee;} .b4{background:#fde047;}
        .result{background:white; border-radius:14px; padding:15px; color:black; margin-top:20px;}
        .live{background:black; color:#22c55e; font-size:11px; padding:4px 10px; border-radius:20px; display:inline-block;}
    </style>
</head>
<body>
    <div class="title">DISTRIBUTED CALCULATOR</div>
    <div class="sub">By Het & Vaishnavi | DC Practical Project</div>

    <div class="card">
        <div class="nodes">
            <span id="p_ADD" class="pill">WORKER :6001</span>
            <span id="p_SUB" class="pill">WORKER :6002</span>
            <span id="p_MUL" class="pill">WORKER :6003</span>
            <span id="p_DIV" class="pill">WORKER :6004</span>
        </div>

        <div class="inputs">
            <input id="num_a" type="number" placeholder="Value A">
            <input id="num_b" type="number" placeholder="Value B">
        </div>

        <div class="btns">
            <button class="b1" onclick="sendCalculation('ADD')">ADD</button>
            <button class="b2" onclick="sendCalculation('SUB')">SUB</button>
            <button class="b3" onclick="sendCalculation('MUL')">MUL</button>
            <button class="b4" onclick="sendCalculation('DIV')">DIV</button>
        </div>

        <div class="result">
            <div class="live" id="live_msg">SYSTEM IDLE</div>
            <h2 id="ans_box" style="margin:10px 0; font-size:32px;">0</h2>
        </div>
    </div>

    <script>
    async function sendCalculation(operation) {
        const a = document.getElementById('num_a').value;
        const b = document.getElementById('num_b').value;
        
        if(!a || !b) { alert('Pela number nakh!'); return; }

        document.querySelectorAll('.pill').forEach(el => el.classList.remove('active'));

        try {
            const response = await fetch('/compute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ op: operation, val_a: a, val_b: b })
            });
            const data = await response.json();
            
            if(data.error) {
                document.getElementById('ans_box').innerText = "Error";
                document.getElementById('live_msg').innerText = data.error;
            } else {
                document.getElementById('ans_box').innerText = data.result;
                document.getElementById('live_msg').innerText = "LIVE FROM WORKER PORT: " + data.port;
                document.getElementById('p_' + operation).classList.add('active');
            }
        } catch (err) {
            document.getElementById('live_msg').innerText = "Worker Node Connection Refused";
        }
    }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_UI)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    op = data.get("op")
    val_a = data.get("val_a")
    val_b = data.get("val_b")

    if op not in WORKERS:
        return jsonify({"error": "Invalid Operation"}), 400

    worker_host, worker_port = WORKERS[op]

    try:
        # True Network Socket Communication with Backend Worker Nodes
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect((worker_host, worker_port))
        
        # Send comma-separated numbers to the network port
        client.send(f"{val_a},{val_b}".encode())
        response = client.recv(1024).decode()
        client.close()
        
        return jsonify({"result": response, "port": worker_port})
    except Exception:
        return jsonify({"error": f"Worker Node on port {worker_port} is offline!"}), 500

if __name__ == "__main__":
    app.run(port=WEB_SERVER_PORT, debug=True)
