
# Импорт нужных библиотек
from flask import Flask, render_template_string # Для создания веб-сервера и отображения HTML
import random # Для генерации случайных чисел (например, множителя ракеты)
import telebot # Библиотека для работы с Telegram Bot API
from threading import Thread # Для запуска бота в отдельном потоке, чтобы он не мешал веб-серверу
from telebot import types # Для работы с типами данных Telegram (кнопки, сообщения и т.д.)

# --- НАСТРОЙКИ ---
TOKEN = '8628554108:AAEVXaX9y0m3DRx9L4dJ1doLk644WRTfGTM' # Это токен твоего Telegram бота. Не меняй его, если не хочешь создавать нового бота.
WEB_APP_URL = "https://app-ru.onrender.com" # !!!ВАЖНО!!! Сюда нужно вставить ту ссылку, которую тебе даст Render.com после успешного деплоя. Игра будет работать по этой ссылке.
ADMIN_PASS = "BOSS-777-XYZ" # Это твой секретный код для доступа к админ-панели. Можешь изменить его на любую комбинацию букв и цифр.

bot = telebot.TeleBot(TOKEN) # Создаем объект бота, используя твой токен
app = Flask(__name__) # Создаем веб-приложение Flask

# HTML-код всей игры. Он большой, поэтому я его разбил на части для понятности.
HTML_TEMPLATE = """
<!DOCTYPE html><html lang="ru"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<title>NeoGift VIP: Evolution [CREATOR]</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@400;900&display=swap" rel="stylesheet">
<style>
/* Стили для оформления игры */
:root { --bg: #050508; --accent: #00f2ff; --red: #ff4757; --green: #2ed573; --purp: #7a00ff; --gold: #ffa502; }
body { margin: 0; background: var(--bg); color: #fff; font-family: 'Montserrat', sans-serif; overflow: hidden; }
.st-bar { padding: 10px 15px; background: #000; border-bottom: 1px solid #111; }
.st-line { height: 4px; background: #111; margin-top: 5px; border-radius: 2px; overflow: hidden; }
#st-fill { height: 100%; width: 100%; background: var(--green); transition: 0.1s linear; }
.header { padding: 15px; display: flex; justify-content: space-between; align-items: center; }
.op-name { font-family: 'Orbitron'; font-size: 16px; font-weight: 900; }
.bal { text-align: right; font-weight: 900; line-height: 1.2; font-size: 12px;}
#rank-box { font-size: 10px; color: var(--accent); font-family: 'Orbitron'; } /* Стиль для рейтинга */
.game-box { margin: 10px 15px; height: 180px; background: radial-gradient(circle, #161a25 0%, #050508 100%); border-radius: 20px; border: 1px solid #1a1a24; position: relative; display: flex; align-items: center; justify-content: center; }
#rx { font-family: 'Orbitron'; font-size: 45px; font-weight: 900; z-index: 5; }
#rocket { position: absolute; bottom: 20px; left: 20px; font-size: 35px; color: var(--accent); transform: rotate(-45deg); transition: 0.1s linear; }
.controls { padding: 0 15px; }
.input-group { background: #0d0d12; border: 1px solid #1a1a24; border-radius: 12px; display: flex; padding: 10px; margin-bottom: 10px; align-items: center;}
input, select { background: none; border: none; color: #fff; font-weight: 900; outline: none; width: 100%; }
.btn-main { width: 100%; height: 55px; border-radius: 15px; border: none; background: linear-gradient(90deg, #0088ff, var(--accent)); color: #fff; font-family: 'Orbitron'; font-weight: 900; font-size: 14px; }
.nav { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: #08080c; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #111; }
.nav-item { text-align: center; color: #333; font-size: 8px; font-family: 'Orbitron'; }
.nav-item.active { color: var(--accent); }
.page { display: none; height: calc(100vh - 220px); padding: 15px; overflow-y: auto; }
.active { display: block; }
/* Стили для админ-панели */
#creator-panel { display: none; background: #1a1500; border: 1px solid var(--gold); padding: 10px; border-radius: 10px; margin: 10px 15px; font-size: 10px; color: var(--gold); }
.adm-tool { margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
.adm-tool input { width: auto; flex-grow: 1; margin-left: 10px; border-bottom: 1px solid var(--gold); }
/* Стили для модального окна */
#modal { position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 2000; display: none; flex-direction: column; padding: 30px; overflow-y: auto; }
</style></head>
<body>
<div class="st-bar">
    <div style="display:flex;justify-content:space-between;font-family:'Orbitron';font-size:9px">
        <span>SYSTEM STABILITY</span><span id="st-perc">100%</span>
    </div>
    <div class="st-line"><div id="st-fill"></div></div>
</div>

<div class="header">
    <div>
        <div id="role-tag" style="color:var(--accent);font-size:9px;font-family:'Orbitron'">USER_LVL_1</div>
        <div class="op-name">{{name}}</div> <!-- Здесь будет имя игрока, которое передаст Telegram -->
        <div id="rank-box">RANK: 0 PTS</div> <!-- Место для отображения рейтинга -->
    </div>
    <div class="bal">
        <div id="g-bal">10000 💰</div> <!-- Отображение золотых монет -->
        <div id="b-bal" style="color:var(--accent)">500 💎</div> <!-- Отображение синих кристаллов -->
    </div>
</div>

<!-- Админ-панель. Скрыта по умолчанию -->
<div id="creator-panel">
    <div style="text-align:center;font-weight:900;margin-bottom:10px;">--- ПАНЕЛЬ УПРАВЛЕНИЯ [80 ПРАВ] ---</div>
    <div class="adm-tool">
        <span>СЛЕДУЮЩИЙ X (0 = авто):</span>
        <input type="number" id="forced-x" value="0" style="color:var(--gold);">
    </div>
    <div class="adm-tool">
        <span>СКОРОСТЬ ПОЛЕТА (0.015=норм):</span>
        <input type="range" id="adm-speed" min="0.005" max="0.1" step="0.005" value="0.015">
    </div>
    <div class="adm-tool">
        <span>МНОЖИТЕЛЬ НАГРАД:</span>
        <input type="number" id="adm-rew" value="1" step="0.1" style="color:var(--gold);">
    </div>
    <button onclick="g+=1000000;update()" style="font-size:8px;background:none;border:1px solid;color:orange;width:100%;">ДОБАВИТЬ 1М GOLD</button>
</div>

<!-- Экран игры "Ракета" -->
<div id="p-rocket" class="page active">
    <div id="hist" style="display:flex;gap:5px;margin-bottom:10px;height:25px;overflow:hidden"></div> <!-- История взрывов -->
    <div class="game-box">
        <div id="rx">10.0s</div> <!-- Отображение множителя или времени -->
        <i class="fa-solid fa-shuttle-space" id="rocket"></i> <!-- Иконка ракеты -->
    </div>
    <div class="controls">
        <div class="input-group">
            <input type="number" id="bet" value="100"> <!-- Поле для ставки -->
            <select id="curr" style="color:var(--accent);font-size:10px;"> <!-- Выбор валюты -->
                <option value="g">GOLD</option>
                <option value="b">BLUE</option>
            </select>
        </div>
        <button class="btn-main" id="btn" onclick="act()">УСТАНОВИТЬ СВЯЗЬ</button> <!-- Кнопка действия -->
    </div>
</div>

<!-- Экран промокодов -->
<div id="p-promo" class="page">
    <h3 style="font-family:'Orbitron'">АКТИВАЦИЯ ПРОМО</h3>
    <div class="input-group">
        <input type="text" id="promo-in" placeholder="Введите код...">
    </div>
    <button class="btn-main" onclick="usePromo()">ПРИМЕНИТЬ</button>
</div>

<!-- Модальное окно (для будущих уведомлений, если понадобится) -->
<div id="modal"></div>

<!-- Нижнее меню навигации -->
<div class="nav">
    <div class="nav-item active" onclick="tab('rocket',this)"><i class="fa-solid fa-rocket"></i><br>ИГРА</div>
    <div class="nav-item" onclick="tab('promo',this)"><i class="fa-solid fa-tags"></i><br>КОДЫ</div>
</div>

<!-- Подключение скрипта Telegram Web App -->
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
// --- Переменные игры ---
let g = 10000; // Начальное количество золотых монет
let b = 500;   // Начальное количество синих кристаллов
let bet = 0;   // Текущая ставка
let cur = 'g'; // Текущая выбранная валюта ('g' - gold, 'b' - blue)
let cash = false; // Флаг, получили ли мы выплату в текущем раунде
let st = 'WAIT'; // Состояние игры: 'WAIT' (ожидание), 'FLY' (полет), 'BOOM' (взрыв)
let rt = 10;   // Время до старта следующего раунда (в секундах)
let rx = 1;    // Текущий множитель в игре
let rc = 0;    // Множитель, на котором произойдет взрыв (crash point)
let pts = 0;   // Очки рейтинга

let isCreator = false; // Флаг, являемся ли мы создателем (админом)

// --- Список 30 промокодов ---
const promos = {
    'GIFT2024': {g:500,b:10}, 'NEO777': {g:1000,b:0}, 'START': {g:2000,b:5}, 'ROCKET': {g:100,b:50}, 'CRASH': {g:300,b:0},
    'GOLD': {g:5000,b:0}, 'BLUE': {g:0,b:100}, 'VIP': {g:1000,b:100}, 'MINE': {g:500,b:5}, 'POWER': {g:100,b:10},
    'FAST': {g:200,b:0}, 'SLOW': {g:200,b:0}, 'FLY': {g:777,b:7}, 'VOID': {g:100,b:1}, 'SPACE': {g:500,b:10},
    'GALAXY': {g:1000,b:20}, 'SHUTTLE': {g:150,b:15}, 'STAR': {g:100,b:100}, 'MOON': {g:50,b:50}, 'ORBIT': {g:400,b:4},
    'ASTRO': {g:600,b:6}, 'METEOR': {g:200,b:20}, 'COMET': {g:300,b:30}, 'SOLAR': {g:900,b:9}, 'LUNA': {g:150,b:0},
    'ATOM': {g:100,b:10}, 'CYBER': {g:500,b:50}, 'TECH': {g:250,b:25}, 'CHIP': {g:800,b:0}, 'DATA': {g:120,b:12}
};

// --- Функция обновления отображения баланса и рейтинга ---
function update(){
    // Расчет рейтинга: 1 очко за каждые 150 золота, 1 очко за каждые 100 синих кристаллов
    pts = Math.floor(g/150 + b/100);
    document.getElementById('g-bal').innerText = g + ' 💰';
    document.getElementById('b-bal').innerText = b + ' 💎';
    document.getElementById('rank-box').innerText = 'RANK: ' + pts + ' PTS'; // Обновляем отображение рейтинга
}

// --- Функция, вызываемая при нажатии кнопки "УСТАНОВИТЬ СВЯЗЬ" / "ЗАБРАТЬ" ---
function act(){
    if(st === 'WAIT' && bet === 0){ // Если игра в режиме ожидания и нет активной ставки
        let a = parseInt(document.getElementById('bet').value); // Получаем значение ставки из поля ввода
        cur = document.getElementById('curr').value; // Получаем выбранную валюту
        if(cur === 'g' && g >= a){ // Если выбрано золото и у игрока достаточно монет
            g -= a; // Вычитаем ставку из баланса
            bet = a; // Сохраняем ставку
            document.getElementById('btn').innerText = 'ОЖИДАНИЕ...'; // Меняем текст на кнопке
            document.getElementById('btn').disabled = true; // Делаем кнопку неактивной
        } else if(cur === 'b' && b >= a){ // Если выбраны кристаллы и у игрока достаточно
            b -= a; // Вычитаем ставку
            bet = a; // Сохраняем ставку
            document.getElementById('btn').innerText = 'ОЖИДАНИЕ...';
            document.getElementById('btn').disabled = true;
        } else { return; } // Если не хватает средств, ничего не делаем
    } else if(st === 'FLY' && bet > 0 && !cash){ // Если ракета летит, есть ставка и выплата еще не получена
        let rewMult = isCreator ? parseFloat(document.getElementById('adm-rew').value) : 1; // Берем множитель наград, если это админ
        let w = Math.floor(bet * rx * rewMult); // Рассчитываем выигрыш
        if(cur === 'g') g += w; else b += w; // Добавляем выигрыш к балансу
        cash = true; // Отмечаем, что выплата получена
        document.getElementById('btn').innerText = 'ВЗЯТО: ' + w; // Меняем текст кнопки на сумму выигрыша
        document.getElementById('btn').disabled = true; // Делаем кнопку неактивной
    }
    update(); // Обновляем отображение баланса и рейтинга
}

// --- Главный игровой цикл (запускается каждые 100 миллисекунд) ---
setInterval(() => {
    if(st === 'WAIT'){ // Если игра в режиме ожидания
        rt -= 0.1; // Уменьшаем время до старта
        let p = (rt / 10) * 100; // Рассчитываем процент заполнения полоски загрузки
        document.getElementById('st-fill').style.width = p + '%'; // Меняем ширину полоски
        document.getElementById('rx').innerText = Math.max(0, rt).toFixed(1) + 's'; // Показываем оставшееся время
        if(rt <= 0){ // Если время вышло
            st = 'FLY'; // Меняем состояние на "полет"
            let forced = parseFloat(document.getElementById('forced-x').value); // Получаем значение принудительного X из админ-панели
            // Если админ задал X > 0, используем его. Иначе генерируем случайный.
            rc = (isCreator && forced > 0) ? forced : (Math.random() * 5 + 1.1).toFixed(2);
        }
    } else if(st === 'FLY'){ // Если ракета летит
        let speed = isCreator ? parseFloat(document.getElementById('adm-speed').value) : 0.015; // Получаем скорость полета из админ-панели или используем стандартную
        rx += rx * speed; // Увеличиваем множитель (скорость роста)
        document.getElementById('rx').innerText = rx.toFixed(2) + 'x'; // Отображаем текущий множитель
        // Меняем позицию иконки ракеты, чтобы она "летела"
        document.getElementById('rocket').style.bottom = (20 + rx * 10) + 'px';
        document.getElementById('rocket').style.left = (20 + rx * 15) + 'px';

        if(bet > 0 && !cash){ // Если есть ставка и выплата еще не получена, делаем кнопку "Забрать" активной
            document.getElementById('btn').disabled = false;
            document.getElementById('btn').innerText = 'ЗАБРАТЬ ' + Math.floor(bet * rx);
        }
        if(rx >= rc){ // Если текущий множитель достиг или превысил множитель взрыва
            st = 'BOOM'; // Меняем состояние на "взрыв"
            document.getElementById('rx').innerText = 'CRASH!'; // Пишем "CRASH!"
            // Через 3 секунды начинаем новый раунд
            setTimeout(() => {
                st = 'WAIT'; // Возвращаем состояние в ожидание
                rt = 10;     // Сбрасываем время до старта
                rx = 1;      // Сбрасываем множитель
                bet = 0;     // Сбрасываем ставку
                cash = false;// Сбрасываем флаг выплаты
                update();    // Обновляем баланс и рейтинг
                // Возвращаем ракету в исходное положение
                document.getElementById('rocket').style.bottom = '20px';
                document.getElementById('rocket').style.left = '20px';
            }, 3000);
        }
    }
}, 100); // Интервал в 100 миллисекунд

// --- Функция активации промокода ---
function usePromo(){
    let c = document.getElementById('promo-in').value.toUpperCase(); // Получаем введенный код и переводим в верхний регистр
    if(c === '""" + ADMIN_PASS + """'){ // Проверяем, совпадает ли код с админским
        isCreator = true; // Устанавливаем флаг создателя
        document.body.style.background = '#0a0800'; // Меняем фон страницы (как в оригинале)
        document.getElementById('role-tag').innerText = '[CREATOR]'; // Меняем тэг роли
        document.getElementById('creator-panel').style.display = 'block'; // Показываем админ-панель
        alert('ДОСТУП ПОЛУЧЕН: 80 ФУНКЦИЙ АКТИВИРОВАНО'); // Сообщение об успехе
    } else if(promos[c]){ // Если код есть в списке промокодов
        g += promos[c].g; // Добавляем золотые монеты
        b += promos[c].b; // Добавляем синие кристаллы
        alert('АКТИВИРОВАНО: +' + promos[c].g + '💰, +' + promos[c].b + '💎'); // Сообщение о получении
        delete promos[c]; // Удаляем промокод из списка, чтобы его нельзя было использовать повторно
        update(); // Обновляем баланс и рейтинг
    } else {
        alert('НЕВЕРНЫЙ КОД'); // Сообщение об ошибке
    }
}

// --- Функция переключения между экранами (игра/промо) ---
function tab(p, e){
    // Скрываем все экраны
    document.querySelectorAll('.page').forEach(x => x.classList.remove('active'));
    // Убираем подсветку со всех кнопок навигации
    document.querySelectorAll('.nav-item').forEach(x => x.classList.remove('active'));
    // Показываем нужный экран
    document.getElementById('p-' + p).classList.add('active');
    // Подсвечиваем нажатую кнопку навигации
    e.classList.add('active');
}

update(); // Вызываем обновление при первой загрузке, чтобы показать начальный баланс и рейтинг
</script></body></html>
"""

# --- Маршрут для главной страницы (игра) ---
@app.route('/')
def index():
    # Отдаем HTML-шаблон, передавая в него имя пользователя (придет из Telegram)
    return render_template_string(HTML_TEMPLATE, name="Cyber_Master") # "Cyber_Master" - это просто пример имени, Telegram передаст настоящее

# --- Обработчик команды /start для Telegram бота ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создаем клавиатуру с кнопками
    # Кнопка, которая откроет Web App (твою игру)
    markup.add(types.KeyboardButton("🚀 ИГРАТЬ", web_app=types.WebAppInfo(WEB_APP_URL)))
    bot.send_message(message.chat.id, "Добро пожаловать в NeoGift Evolution!", reply_markup=markup) # Отправляем приветственное сообщение с кнопкой

# --- Функция для запуска Telegram бота ---
def run_bot():
    bot.infinity_polling() # Запускает бота и слушает новые сообщения

# --- Основной блок запуска ---
if __name__ == '__main__':
    # Запускаем функцию бота в отдельном потоке, чтобы она не блокировала веб-сервер
    Thread(target=run_bot).start()
    # Запускаем веб-сервер Flask. Он будет работать на порту 5000.
    # host='0.0.0.0' означает, что сервер будет доступен извне (важно для Render)
    app.run(host='0.0.0.0', port=5000)

