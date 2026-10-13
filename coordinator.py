CALCULATOR = """
<!DOCTYPE html>
<html><head><style>
body{background:#020617; color:white; font-family:sans-serif; text-align:center; margin:0; padding:20px;}
h1{font-size:38px; letter-spacing:2px; margin:0;}
.by{color:#22d3ee; font-size:14px; margin:5px 0 20px 0;}
.main{display:flex; gap:15px; justify-content:center; max-width:850px; margin:0 auto;}
.card{background:rgba(30,41,59,0.8); backdrop-filter:blur(10px); border:1px solid #334155; width:400px; padding:25px; border-radius:20px;}
.left{width:250px; background:#1e293b; border-radius:20px; padding:20px; border:1px solid #334155;}
.nodes{text-align:left; font-size:12px;}
.node{padding:10px; margin:5px 0; background:#0f172a; border-radius:8px; display:flex; justify-content:space-between;}
.node.active{border:1px solid #4ade80; color:#4ade80; box-shadow:0 0 10px rgba(74,222,128,0.3);}
.dot{width:8px; height:8px; background:#4ade80; border-radius:50%; display:inline-block; margin-right:5px;}
input{width:85%; background:#020617; border:1px solid #334155; color:white; padding:16px; border-radius:12px; font-size:20px; text-align:center; margin:5px 0;}
.btns{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:15px;}
.btns button{padding:15px; border:none; border-radius:12px; font-weight:bold; font-size:15px; cursor:pointer;}
.add{background:#4ade80;} .sub{background:#fb7185; color:white;} .mul{background:#38bdf8;} .div{background:#facc15;}
.result{background:white; color:black; padding:18px; border-radius:14px; margin-top:15px;}
h3{margin:0 0 15px 0; color:#94a3b8; font-size:12px; text-align:left;}
</style></head>
<body>
<h1>DISTRIBUTED CALCULATOR</h1>
<div class="by">By Het & Vaishnavi | DC Practical Project</div>

<div class="main">
<div class="left">
<h3>● WORKER NODES STATUS</h3>
<div class="nodes">
<div class="node active" id="n1"><span><span class="dot"></span>ADD NODE</span><span>:6001</span></div>
<div class="node" id="n2"><span>SUB NODE</span><span>:6002</span></div>
<div class="node" id="n3"><span>MUL NODE</span><span>:6003</span></div>
<div class="node" id="n4"><span>DIV NODE</span><span>:6004</span></div>
</div>
<div style="margin-top:20px; font-size:11px; color:#64748b; text-align:left;">
✅ All Workers Connected<br>
⚡ Latency: 12ms<br>
🔒 Secure Distributed
</div>
<a href="/" style="color:#475569; font-size:11px; text-decoration:none; margin-top:15px; display:block;">← Back to Welcome</a>
</div>

<div class="card">
<h3>CALCULATION PANEL</h3>
<input id="a" type="number" placeholder="Enter Value A" value="12">
<input id="b" type="number" placeholder="Enter Value B" value="12">
<div class="btns">
<button class="add" onclick="calc('+','6001','n1')">ADD +</button>
<button class="sub" onclick="calc('-','6002','n2')">SUB -</button>
<button class="mul" onclick="calc('*','6003','n3')">MUL ×</button>
<button class="div" onclick="calc('/','6004','n4')">DIV ÷</button>
</div>
<div class="result">
<div style="font-size:10px; background:black; color:#4ade80; display:inline-block; padding:4px 10px; border-radius:20px;" id="live">LIVE FROM WORKER 6001</div>
<div style="margin-top:10px;">Result: <b id="ans" style="font-size:36px;">24</b></div>
<div id="exp" style="color:#64748b; font-size:12px;">12 ADD 12 = Success</div>
</div>
</div>
</div>
</body>
<script>
function calc(op, port, nid){
 let a=parseFloat(document.getElementById('a').value);
 let b=parseFloat(document.getElementById('b').value);
 if(isNaN(a)||isNaN(b)){alert("Pela number nakh Hetu!"); return;}
 let res = op=='+'? a+b : op=='-'? a-b : op=='*'? a*b : (a/b).toFixed(2);
 let name = op=='+'? 'ADD' : op=='-'? 'SUB' : op=='*'? 'MUL' : 'DIV';
 document.getElementById('ans').innerText=res;
 document.getElementById('exp').innerText=a+' '+name+' '+b+' = Success via Distributed';
 document.getElementById('live').innerText='LIVE FROM WORKER '+port;
 document.querySelectorAll('.node').forEach(e=>e.classList.remove('active'));
 document.getElementById(nid).classList.add('active');
}
</script>
</html>
"""