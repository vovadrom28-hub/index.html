
from flask import Flask, render_template_string
import random

app = Flask(__name__)

# --- ГЕНЕРАЦИЯ 600 УЛЬТРА-ЯРКИХ ПРЕФИКСОВ ---
WORDS_1 = ["NEON", "CRYSTAL", "GHOST", "ALPHA", "TITAN", "SOLAR", "VOID", "ZENITH", "AURA", "GALAXY", "ELITE", "DRAGON", "PHANTOM", "OMEGA", "VORTEX", "ULTRA", "MYSTIC", "SHADOW"]
WORDS_2 = ["LORD", "KING", "SOUL", "CORE", "KNIGHT", "GOD", "BEAST", "STORM", "WOLF", "DEMON", "VIP", "BOSS", "HERO", "STRIKE", "BLADE", "FLAME", "ICE", "FORCE"]
STYLES = ["rainbow", "gradient-neon", "matte-vibrant", "glossy-glass", "fire-burn", "electric-pulse"]

ALL_PREFIXES = []
for i in range(600):
    w1 = random.choice(WORDS_1)
    w2 = random.choice(WORDS_2)
    st = random.choice(STYLES)
    c1 = f"hsl({random.randint(0, 360)}, 100%, 50%)"
    c2 = f"hsl({random.randint(0, 360)}, 100%, 50%)"
    ALL_PREFIXES.append({
        "id": i,
        "name": f"{w1} {w2}",
        "style": st,
        "price": random.randint(5000, 80000), 
        "color1": c1,
        "color2": c2
    })

# --- ОСНОВНОЙ КОД ИНТЕРФЕЙСА ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEOGIFT EXTREME - BOSS MODE</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@300;700;900&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #00f2ff;
            --secondary: #7000ff;
            --bg: #050508;
            --card-bg: rgba(255, 255, 255, 0.07);
            --text: #ffffff;
            --gold: #ffd700;
            --danger: #ff0044;
            --success: #00ff88;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body {
            margin: 0; background: var(--bg); color: var(--text);
            font-family: 'Montserrat', sans-serif; overflow: hidden;
            height: 100vh;
        }

        #bg-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }

        header {
            height: 80px; padding: 0 15px; display: flex; justify-content: space-between;
            align-items: center; background: rgba(0,0,0,0.9);
            border-bottom: 2px solid var(--primary); position: fixed; top: 0; width: 100%; z-index: 1000;
            backdrop-filter: blur(20px);
        }

        .profile-trigger { display: flex; align-items: center; gap: 12px; cursor: pointer; }
        .avatar-box {
            width: 50px; height: 50px; border-radius: 50%; border: 2px solid var(--primary);
            box-shadow: 0 0 15px var(--primary); transition: 0.3s; overflow: hidden;
        }
        .avatar-box img { width: 100%; height: 100%; object-fit: cover; }

        .header-stats { text-align: right; font-family: 'Orbitron'; font-weight: 900; }
        .stat-g { color: var(--gold); text-shadow: 0 0 10px var(--gold); font-size: 14px; }
        .stat-d { color: var(--primary); text-shadow: 0 0 10px var(--primary); font-size: 14px; }

        nav {
            position: fixed; bottom: 0; width: 100%; height: 80px;
            background: rgba(0,0,0,0.95); border-top: 1px solid #222;
            display: flex; justify-content: space-around; align-items: center; z-index: 1000;
        }
        .nav-item {
            color: #555; text-align: center; font-size: 10px; font-weight: 900;
            transition: 0.3s; flex: 1; cursor: pointer;
        }
        .nav-item i { font-size: 24px; display: block; margin-bottom: 5px; }
        .nav-item.active { color: var(--primary); text-shadow: 0 0 15px var(--primary); transform: translateY(-5px); }

        .container {
            height: 100vh; padding: 100px 15px 100px 15px;
            overflow-y: auto; scroll-behavior: smooth;
        }
        .page { display: none; animation: fadeIn 0.4s ease-out forwards; }
        .page.active { display: block; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        .card {
            background: var(--card-bg); border-radius: 20px; padding: 20px;
            margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.05);
            backdrop-filter: blur(10px); position: relative; overflow: hidden;
        }

        .btn-main {
            background: var(--primary); color: #000; border: none; padding: 15px;
            border-radius: 12px; width: 100%; font-family: 'Orbitron'; font-weight: 900;
            text-transform: uppercase; cursor: pointer; transition: 0.2s;
            box-shadow: 0 5px 15px rgba(0, 242, 255, 0.3);
            margin-top: 10px;
        }
        .btn-main:disabled { background: #444; box-shadow: none; cursor: not-allowed; }

        /* ИГРА: CRASH */
        .crash-area { height: 200px; background: #000; border-radius: 15px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; border: 1px solid var(--primary); }
        .crash-mult { font-size: 50px; font-family: 'Orbitron'; font-weight: 900; z-index: 10; transition: 0.1s; }
        .crash-line { position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; background: var(--primary); transform-origin: left bottom; transition: 0.1s; }

        /* ИГРА: TOWER */
        .tower-grid { display: flex; flex-direction: column-reverse; gap: 5px; }
        .tower-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; opacity: 0.3; pointer-events: none; }
        .tower-row.active { opacity: 1; pointer-events: all; }
        .t-cell { height: 45px; background: #222; border-radius: 8px; border: 1px solid #444; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .t-cell.win { background: var(--success); color: #000; }
        .t-cell.lose { background: var(--danger); color: #fff; }

        /* ИГРА: SLOTS */
        .slots-container { display: flex; gap: 10px; justify-content: center; margin: 20px 0; }
        .slot-reel { width: 80px; height: 100px; background: #111; border: 2px solid var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 40px; }

        /* ПРЕФИКСЫ */
        .pref { padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 11px; text-transform: uppercase; color: #fff; }
        .rainbow { background: linear-gradient(90deg, red, orange, yellow, lime, cyan, blue, magenta, red); background-size: 300%; animation: rb 4s linear infinite; }
        @keyframes rb { to { background-position: 300%; } }
        .gradient-neon { background: linear-gradient(45deg, var(--c1), var(--c2)); box-shadow: 0 0 10px var(--c1); }
        .matte-vibrant { background: var(--c1); border: 1px solid rgba(255,255,255,0.5); }
        
        /* МОДАЛКИ И ПРОЧЕЕ */
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; display: none; padding: 20px; overflow-y: auto; }
        #notif-wrap { position: fixed; top: 90px; left: 50%; transform: translateX(-50%); z-index: 3000; width: 90%; }
        .notif { background: #fff; color: #000; padding: 15px; border-radius: 12px; margin-bottom: 10px; font-weight: 900; box-shadow: 0 10px 30px rgba(0,0,0,0.5); animation: notifIn 0.3s forwards; }
        @keyframes notifIn { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

        input, select { width: 100%; padding: 12px; background: #000; border: 1px solid #333; color: #fff; border-radius: 10px; margin-bottom: 10px; font-family: 'Orbitron'; }
    </style>
</head>
<body>

    <canvas id="bg-canvas"></canvas>
    <div id="notif-wrap"></div>

    <header>
        <div class="profile-trigger" onclick="openProfile()">
            <div class="avatar-box"><img id="ui-ava" src="https://api.dicebear.com/7.x/avataaars/svg?seed=Boss"></div>
            <div>
                <div style="font-weight:900; font-size:14px;"><span id="ui-pref"></span> <span id="ui-nick">Player</span></div>
                <div style="font-size:10px; color:var(--primary);">RANK: <span id="ui-rp">0</span> RP</div>
            </div>
        </div>
        <div class="header-stats">
            <div class="stat-g"><span id="ui-gold">0</span> 💰</div>
            <div class="stat-d"><span id="ui-gems">0</span> 💎</div>
        </div>
    </header>

    <div class="container">
        
        <!-- HUB PAGE -->
        <div id="page-hub" class="page active">
            <div class="bp-header" onclick="showPage('bp')">
                <div class="card" style="border: 1px solid var(--primary);">
                    <div style="display:flex; justify-content:space-between; font-family:'Orbitron'; font-size:12px;">
                        <b>BATTLE PASS</b>
                        <span>LVL <span id="bp-lvl">1</span></span>
                    </div>
                    <div style="background:#222; height:10px; border-radius:5px; margin:10px 0; overflow:hidden;">
                        <div id="bp-bar" style="background:var(--primary); height:100%; width:0%;"></div>
                    </div>
                    <small style="opacity:0.5;">Выполнено заданий: <span id="bp-done">0</span>/5</small>
                </div>
            </div>

            <h3 style="font-family:'Orbitron'; margin-top:25px;">ИГРОВЫЕ МОДУЛИ</h3>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                <div class="card" onclick="openGame('crash')"><i class="fa-solid fa-rocket" style="font-size:30px; color:var(--primary);"></i><br><br><b>CRASH</b></div>
                <div class="card" onclick="openGame('mines')"><i class="fa-solid fa-bomb" style="font-size:30px; color:var(--danger);"></i><br><br><b>MINES</b></div>
                <div class="card" onclick="openGame('tower')"><i class="fa-solid fa-layer-group" style="font-size:30px; color:#ffaa00;"></i><br><br><b>TOWER</b></div>
                <div class="card" onclick="openGame('slots')"><i class="fa-solid fa-republican" style="font-size:30px; color:var(--success);"></i><br><br><b>SLOTS</b></div>
            </div>
        </div>

        <!-- CRASH PAGE -->
        <div id="page-crash" class="page">
            <div class="card">
                <div class="crash-area">
                    <div id="crash-val" class="crash-mult">1.00x</div>
                    <div id="crash-line" class="crash-line"></div>
                </div>
                <input type="number" id="crash-bet" value="100">
                <select id="crash-cur">
                    <option value="gold">ЗОЛОТО 💰</option>
                    <option value="gems">ГЕМЫ 💎</option>
                </select>
                <button id="crash-btn" class="btn-main" onclick="crashStart()">СТАВКА</button>
            </div>
            <button class="btn-main" style="background:#222; color:#fff;" onclick="showPage('hub')">НАЗАД</button>
        </div>

        <!-- MINES PAGE -->
        <div id="page-mines" class="page">
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 id="m-x" style="font-family:'Orbitron'; color:var(--primary); margin:0;">1.00x</h2>
                    <button class="btn-main" style="width:auto; padding:10px 20px;" onclick="minesCashout()">ЗАБРАТЬ</button>
                </div>
                <div id="m-grid" style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin:15px 0;"></div>
                <select id="m-cur">
                    <option value="gold">ЗОЛОТО 💰</option>
                    <option value="gems">ГЕМЫ 💎</option>
                </select>
                <input type="number" id="m-bet" value="100">
                <button class="btn-main" onclick="minesStart()">СТАРТ</button>
            </div>
            <button class="btn-main" style="background:#222; color:#fff;" onclick="showPage('hub')">НАЗАД</button>
        </div>

        <!-- TOWER PAGE -->
        <div id="page-tower" class="page">
            <div class="card">
                <div style="text-align:center; font-family:'Orbitron'; margin-bottom:10px;">
                    <h2 id="t-x" style="color:var(--gold);">x1.00</h2>
                </div>
                <div id="t-grid" class="tower-grid"></div>
                <input type="number" id="t-bet" value="100" style="margin-top:15px;">
                <button id="t-start-btn" class="btn-main" onclick="towerStart()">ИГРАТЬ</button>
                <button id="t-cash-btn" class="btn-main" style="display:none; background:var(--success);" onclick="towerCashout()">ЗАБРАТЬ</button>
            </div>
            <button class="btn-main" style="background:#222; color:#fff;" onclick="showPage('hub')">НАЗАД</button>
        </div>

        <!-- SLOTS PAGE -->
        <div id="page-slots" class="page">
            <div class="card">
                <div class="slots-container">
                    <div id="s-1" class="slot-reel">🎰</div>
                    <div id="s-2" class="slot-reel">🎰</div>
                    <div id="s-3" class="slot-reel">🎰</div>
                </div>
                <input type="number" id="s-bet" value="50">
                <button class="btn-main" onclick="slotsSpin()">КРУТИТЬ</button>
                <div style="font-size:10px; opacity:0.6; margin-top:10px; text-align:center;">
                    💎💎💎 = x50 | 🍋🍋🍋 = x10 | 🍒🍒🍒 = x5
                </div>
            </div>
            <button class="btn-main" style="background:#222; color:#fff;" onclick="showPage('hub')">НАЗАД</button>
        </div>

        <!-- SHOP PAGE -->
        <div id="page-shop" class="page">
            <h2 style="font-family:'Orbitron';">МАГАЗИН</h2>
            <div id="shop-list"></div>
        </div>

        <!-- PETS PAGE -->
        <div id="page-pets" class="page">
            <div class="card" style="background:var(--gold); color:#000; text-align:center;" onclick="buyPetCase()">
                <h2 style="margin:0;">КЕЙС ПИТОМЦЕВ</h2>
                <b>10,000 ГЕМОВ</b>
            </div>
            <div id="pets-list"></div>
        </div>

        <!-- RANK PAGE -->
        <div id="page-rank" class="page">
            <h2 style="font-family:'Orbitron';">ТОП ИГРОКОВ</h2>
            <div id="rank-list"></div>
        </div>

        <!-- BATTLE PASS PAGE -->
        <div id="page-bp" class="page">
            <h2 style="font-family:'Orbitron';">ЗАДАНИЯ</h2>
            <div id="bp-tasks"></div>
        </div>

    </div>

    <!-- PROFILE MODAL -->
    <div id="modal-profile" class="modal">
        <h2 style="font-family:'Orbitron';">ПРОФИЛЬ</h2>
        <div class="card">
            <label>НИКНЕЙМ:</label>
            <input type="text" id="in-nick" oninput="updateProfile()">
            <label>ПРОМОКОД:</label>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in-promo" placeholder="ВВЕДИТЕ КОД...">
                <button class="btn-main" style="width:auto; margin-top:0;" onclick="applyPromo()">OK</button>
            </div>
            <label>АВАТАР (Seed):</label>
            <input type="text" id="in-ava" oninput="updateProfile()">
            <label>ЦВЕТ UI:</label>
            <input type="color" id="in-color" style="height:50px;" oninput="updateProfile()">
            <button class="btn-main" style="margin-top:15px;" onclick="closeProfile()">ЗАКРЫТЬ</button>
        </div>
    </div>

    <nav>
        <div class="nav-item active" id="n-hub" onclick="showPage('hub')"><i class="fa-solid fa-house"></i>HUB</div>
        <div class="nav-item" id="n-shop" onclick="showPage('shop')"><i class="fa-solid fa-shop"></i>SHOP</div>
        <div class="nav-item" id="n-pets" onclick="showPage('pets')"><i class="fa-solid fa-paw"></i>PETS</div>
        <div class="nav-item" id="n-rank" onclick="showPage('rank')"><i class="fa-solid fa-trophy"></i>RANK</div>
    </nav>

    <script>
        let gold = 5000, gems = 500, rp = 0;
        let nick = "BossPlayer", avaSeed = "Boss", activePref = -1, uiColor = "#00f2ff";
        let pets = [], activePet = null;
        let bpExp = 0, bpTasksDone = 0;
        let usedPromos = [];

        const allPrefixes = {{ ALL_PREFIXES | tojson }};
        
        const promoData = {
            "MEGA_BOOST_2026": { gold: 2000, gems: 500, pet: true },
            "GHOST_RIDER": { gold: 0, gems: 1000, pet: false },
            "NEO_GIFT": { gold: 1500, gems: 0, pet: false },
            "ALPHA_PET": { gold: 0, gems: 0, pet: true },
            "CRYSTAL_VOID": { gold: 0, gems: 2000, pet: false },
            "TITAN_POWER": { gold: 1000, gems: 1000, pet: false },
            "SOLAR_RAY": { gold: 500, gems: 500, pet: false },
            "VOID_DRAGON": { gold: 2000, gems: 0, pet: false },
            "ZENITH_KING": { gold: 0, gems: 1200, pet: true },
            "ELITE_SQUAD": { gold: 0, gems: 800, pet: false },
            "SHADOW_WIN": { gold: 0, gems: 1500, pet: false },
            "OMEGA_STRIKE": { gold: 1900, gems: 0, pet: false },
            "VORTEX_GIFT": { gold: 777, gems: 777, pet: false },
            "MYSTIC_SOUL": { gold: 1000, gems: 0, pet: true },
            "ULTRA_MODE": { gold: 2000, gems: 2000, pet: false }
        };

        const petsData = {
            miki: { n: "Мики", d: "Удача x1.5", icon: "🐭" },
            belle: { n: "Бель", d: "Награда x1.3", icon: "🦊" },
            leo: { n: "Лео", d: "Скидка 20%", icon: "🦁" },
            nita: { n: "Нита", d: "Бонус к RP", icon: "🐻" },
            spike: { n: "Спайк", d: "Бог Рандома x2", icon: "🌵" }
        };

        function notify(msg) {
            const wrap = document.getElementById('notif-wrap');
            const div = document.createElement('div');
            div.className = 'notif'; div.innerText = msg;
            wrap.appendChild(div);
            setTimeout(() => div.remove(), 3000);
        }

        function updateUI() {
            document.getElementById('ui-gold').innerText = Math.floor(gold);
            document.getElementById('ui-gems').innerText = Math.floor(gems);
            document.getElementById('ui-nick').innerText = nick;
            document.getElementById('ui-ava').src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${avaSeed}`;
            rp = Math.floor(gold/50 + gems/5 + bpExp);
            document.getElementById('ui-rp').innerText = rp;
            
            let pTag = document.getElementById('ui-pref');
            if(activePref !== -1) {
                let p = allPrefixes[activePref];
                pTag.innerText = p.name; pTag.className = "pref " + p.style;
                pTag.style.setProperty('--c1', p.color1); pTag.style.setProperty('--c2', p.color2);
                pTag.style.display = 'inline-block';
            }
            document.documentElement.style.setProperty('--primary', uiColor);
            document.getElementById('bp-bar').style.width = (bpExp % 100) + "%";
            document.getElementById('bp-lvl').innerText = Math.floor(bpExp/100) + 1;
        }

        function showPage(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('page-'+id).classList.add('active');
            if(document.getElementById('n-'+id)) document.getElementById('n-'+id).classList.add('active');
            if(id === 'shop') renderShop();
            if(id === 'pets') renderPets();
        }

        function applyPromo() {
            let code = document.getElementById('in-promo').value.toUpperCase();
            if(usedPromos.includes(code)) return notify("Код уже использован!");
            if(promoData[code]) {
                let d = promoData[code];
                gold += d.gold; gems += d.gems;
                if(d.pet) {
                    let pKeys = Object.keys(petsData);
                    let rp = pKeys[Math.floor(Math.random()*pKeys.length)];
                    if(!pets.includes(rp)) pets.push(rp);
                }
                usedPromos.push(code);
                notify("УСПЕШНО! Бонусы начислены.");
                updateUI();
            } else notify("Неверный код!");
        }

        // --- CRASH LOGIC ---
        let crashInterval, crashMult = 1.0, crashRunning = false;
        function crashStart() {
            if(crashRunning) {
                // Cashout
                let bet = parseInt(document.getElementById('crash-bet').value);
                let cur = document.getElementById('crash-cur').value;
                let win = Math.floor(bet * crashMult);
                if(cur === 'gold') gold += win; else gems += win;
                notify("ВЫИГРАНО: " + win);
                resetCrash();
                return;
            }
            let bet = parseInt(document.getElementById('crash-bet').value);
            let cur = document.getElementById('crash-cur').value;
            if((cur === 'gold' && gold < bet) || (cur === 'gems' && gems < bet)) return notify("Мало средств!");
            
            if(cur === 'gold') gold -= bet; else gems -= bet;
            crashRunning = true;
            crashMult = 1.0;
            document.getElementById('crash-btn').innerText = "ЗАБРАТЬ";
            document.getElementById('crash-val').style.color = "white";
            
            let crashPoint = Math.random() * 5 + 1.1; // Рандомный момент краша
            
            crashInterval = setInterval(() => {
                crashMult += 0.01;
                document.getElementById('crash-val').innerText = crashMult.toFixed(2) + "x";
                if(crashMult >= crashPoint) {
                    clearInterval(crashInterval);
                    document.getElementById('crash-val').innerText = "CRASHED!";
                    document.getElementById('crash-val').style.color = "var(--danger)";
                    setTimeout(resetCrash, 2000);
                }
            }, 100);
            updateUI();
        }
        function resetCrash() {
            clearInterval(crashInterval);
            crashRunning = false;
            document.getElementById('crash-btn').innerText = "СТАВКА";
            document.getElementById('crash-val').innerText = "1.00x";
            updateUI();
        }

        // --- TOWER LOGIC ---
        let towerActive = false, towerFloor = 0, towerBet = 0, towerX = 1.0;
        function towerStart() {
            towerBet = parseInt(document.getElementById('t-bet').value);
            if(gold < towerBet) return notify("Мало золота!");
            gold -= towerBet;
            towerActive = true; towerFloor = 0; towerX = 1.0;
            document.getElementById('t-start-btn').style.display = 'none';
            document.getElementById('t-cash-btn').style.display = 'block';
            renderTower();
            updateUI();
        }
        function renderTower() {
            const grid = document.getElementById('t-grid');
            grid.innerHTML = '';
            for(let i=0; i<10; i++) {
                let row = document.createElement('div');
                row.className = 'tower-row' + (i === towerFloor ? ' active' : '');
                row.id = 't-row-' + i;
                for(let j=0; j<3; j++) {
                    let cell = document.createElement('div');
                    cell.className = 't-cell';
                    cell.innerHTML = '❓';
                    cell.onclick = () => towerStep(i, j);
                    row.appendChild(cell);
                }
                grid.appendChild(row);
            }
        }
        function towerStep(r, c) {
            if(!towerActive || r !== towerFloor) return;
            let trap = Math.floor(Math.random() * 3);
            let cells = document.getElementById('t-row-'+r).children;
            if(c === trap) {
                cells[c].innerHTML = '💥'; cells[c].classList.add('lose');
                towerActive = false;
                notify("БАБАХ! Вы проиграли.");
                setTimeout(() => {
                    document.getElementById('t-start-btn').style.display = 'block';
                    document.getElementById('t-cash-btn').style.display = 'none';
                    grid.innerHTML = '';
                }, 1500);
            } else {
                cells[c].innerHTML = '💎'; cells[c].classList.add('win');
                towerX *= 1.8;
                towerFloor++;
                document.getElementById('t-x').innerText = 'x' + towerX.toFixed(2);
                if(towerFloor > 9) towerCashout();
                else renderTower();
            }
        }
        function towerCashout() {
            if(!towerActive) return;
            let win = Math.floor(towerBet * towerX);
            gold += win;
            notify("ЗАБРАНО: " + win);
            towerActive = false;
            document.getElementById('t-start-btn').style.display = 'block';
            document.getElementById('t-cash-btn').style.display = 'none';
            updateUI();
        }

        // --- SLOTS LOGIC ---
        function slotsSpin() {
            let bet = parseInt(document.getElementById('s-bet').value);
            if(gold < bet) return notify("Мало золота!");
            gold -= bet;
            const icons = ['🍒', '🍋', '💎', '7️⃣', '🔔'];
            let r1 = icons[Math.floor(Math.random()*icons.length)];
            let r2 = icons[Math.floor(Math.random()*icons.length)];
            let r3 = icons[Math.floor(Math.random()*icons.length)];
            
            document.getElementById('s-1').innerText = r1;
            document.getElementById('s-2').innerText = r2;
            document.getElementById('s-3').innerText = r3;
            
            if(r1 === r2 && r2 === r3) {
                let mult = r1 === '💎' ? 50 : (r1 === '🍋' ? 10 : 5);
                let win = bet * mult;
                gold += win;
                notify("JACKPOT! " + win);
            }
            updateUI();
        }

        // --- MINES (FIXED) ---
        let mActive = false, mBet = 0, mX = 1.0, mData = [], mCur = 'gold';
        function minesStart() {
            mBet = parseInt(document.getElementById('m-bet').value);
            mCur = document.getElementById('m-cur').value;
            let bal = mCur === 'gold' ? gold : gems;
            if(bal < mBet) return notify("Мало средств!");
            if(mCur === 'gold') gold -= mBet; else gems -= mBet;
            
            mActive = true; mX = 1.0;
            mData = Array(25).fill('g');
            for(let i=0; i<4; i++) {
                let pos = Math.floor(Math.random()*25);
                mData[pos] = 'b';
            }
            
            const grid = document.getElementById('m-grid'); grid.innerHTML = '';
            for(let i=0; i<25; i++) {
                let c = document.createElement('div');
                c.className = 't-cell';
                c.onclick = () => {
                    if(!mActive || c.innerHTML !== '❓') return;
                    if(mData[i] === 'b') {
                        c.innerHTML = '💣'; c.style.background = 'red';
                        mActive = false; notify("МИНА!");
                    } else {
                        c.innerHTML = '💎'; c.style.background = 'var(--primary)';
                        mX *= 1.25;
                        document.getElementById('m-x').innerText = mX.toFixed(2) + "x";
                    }
                };
                c.innerHTML = '❓';
                grid.appendChild(c);
            }
            updateUI();
        }
        function minesCashout() {
            if(!mActive) return;
            let win = Math.floor(mBet * mX);
            if(mCur === 'gold') gold += win; else gems += win;
            mActive = false; notify("ВЫИГРАНО: " + win);
            updateUI();
        }

        function openGame(g) { showPage(g); }
        function openProfile() { document.getElementById('modal-profile').style.display = 'block'; }
        function closeProfile() { document.getElementById('modal-profile').style.display = 'none'; }
        
        function updateProfile() {
            nick = document.getElementById('in-nick').value || "Player";
            avaSeed = document.getElementById('in-ava').value || "Boss";
            uiColor = document.getElementById('in-color').value;
            updateUI();
        }

        function renderShop() {
            const list = document.getElementById('shop-list'); list.innerHTML = '';
            allPrefixes.slice(0, 50).forEach(p => {
                list.innerHTML += `<div class="card" style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="pref ${p.style}" style="--c1:${p.color1}; --c2:${p.color2}">${p.name}</span>
                    <button class="btn-main" style="width:auto; padding:5px 15px;" onclick="buyPref(${p.id}, ${p.price})">${p.price} 💎</button>
                </div>`;
            });
        }
        function buyPref(id, pr) {
            if(gems >= pr) { gems -= pr; activePref = id; notify("Куплено!"); updateUI(); }
            else notify("Мало гемов!");
        }

        function renderPets() {
            const list = document.getElementById('pets-list'); list.innerHTML = '<h3>МОИ ПИТОМЦЫ</h3>';
            pets.forEach(p => {
                let d = petsData[p];
                list.innerHTML += `<div class="card" onclick="activePet='${p}'; notify('Активен: ${d.n}')" style="${activePet===p?'border:2px solid var(--primary)':''}">
                    <span style="font-size:30px;">${d.icon}</span> <b>${d.n}</b><br><small>${d.d}</small>
                </div>`;
            });
        }

        // КАНВАС ФОНА
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        for(let i=0; i<50; i++) particles.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*2, dx: Math.random()-0.5, dy: Math.random()-0.5});
        function drawBg() {
            ctx.clearRect(0,0,canvas.width, canvas.height);
            ctx.fillStyle = uiColor; ctx.globalAlpha = 0.2;
            particles.forEach(p => {
                ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                p.x += p.dx; p.y += p.dy;
                if(p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if(p.y < 0 || p.y > canvas.height) p.dy *= -1;
            });
            requestAnimationFrame(drawBg);
        }
        drawBg();
        window.onload = updateUI;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, ALL_PREFIXES=ALL_PREFIXES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
