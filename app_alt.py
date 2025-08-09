from flask import Flask, render_template, session, jsonify, request
import random

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here' # Important for session management

# --- Word & Definition List ---
WORDS_AND_DEFS = {
    3: [
        {"word": "zam", "definition": "Bir şeyin fiyatını artırma, bindirim."},
        {"word": "uzi", "definition": "Kısa sürede birçok mermi atabilen, isabet oranı düşük, tek elle de kullanılabilen bir tür makineli tüfek."},
        {"word": "lal", "definition": "Dili tutulmuş, konuşamayan."},
        {"word": "mir", "definition": "Bey, emir, komutan."},
        {"word": "yel", "definition": "Rüzgâr."},
        {"word": "kıç", "definition": "Geminin arka kısmı."},
        {"word": "şom", "definition": "Uğursuz, kötü."}
    ],
    4: [
        {"word": "inci", "definition": "İstiridye gibi deniz hayvanlarından çıkan değerli, parlak süs tanesi."},
        {"word": "ahit", "definition": "Söz verme, antlaşma, yemin."},
        {"word": "kaşe", "definition": "Damga; mühür. Belirlenmiş sürelerde çalışanlara ödenen ücret."},
        {"word": "saka", "definition": "Evlere su taşıyan kimse; bir tür ötücü kuş."},
        {"word": "cenk", "definition": "Savaş, muharebe."},
        {"word": "şike", "definition": "Bir spor karşılaşmasının sonucunu değiştirmek için yapılan gizli anlaşma."},
        {"word": "amme", "definition": "Kamu."}
    ],
    5: [
        {"word": "janti", "definition": "Güzel, şık, havalı, gösterişli olan (kimse)."},
        {"word": "kuşak", "definition": "Bele sarılan uzun ve enli kumaş. Belli bir zaman diliminde doğmuş olan nesil."},
        {"word": "uçarı", "definition": "Hovarda, ele avuca sığmaz, çok haşarı (kimse)."},
        {"word": "zabıt", "definition": "Resmî olayların yazıldığı belge, tutanak."},
        {"word": "kahve", "definition": "Kök boyasıgillerden, sıcak iklimlerde yetişen bir ağaç. Bu ağacın meyvesinin çekirdeği. Bu çekirdeklerin kavrulup çekilmesiyle elde edilen toz. Bu tozla hazırlanan içecek."},
        {"word": "hafız", "definition": "Kur'an'ı bütünüyle ezbere bilen kimse."},
        {"word": "boran", "definition": "Sert rüzgâr, şimşek ve gök gürültüsü ile ortaya çıkan sağanak yağışlı hava olayı."}
    ],
    6: [
        {"word": "butlan", "definition": "Hukuki bir işlemin kurucu unsurlarında mevzuatta öngörülen şartlar sağlanmışken geçerlilik şartlarında yasada öngörülen zorunlu bir unsurun eksik olması durumu. Hukukî geçersizlik, hükümsüzlük."},
        {"word": "şakrak", "definition": "Neşeli ve canlı bir şekilde öten (kuş); canlı, hareketli (kimse)."},
        {"word": "bornoz", "definition": "Banyodan sonra kurulanmak için giyilen, havlu kumaşından yapılmış giysi."},
        {"word": "icazet", "definition": "İzin, onay, diploma."},
        {"word": "tasnif", "definition": "Sınıflandırma, bölümlere ayırma."},
        {"word": "levent", "definition": "Osmanlı donanmasında görevli deniz askeri."},
        {"word": "ecnebi", "definition": "Yabancı."}
    ],
    7: [
        {"word": "overlok", "definition": "Halı, kilim, yolluk, paspas kenarına; halıfleks kenarına makine ile yapılan sıkı, zikzaklı dikiş."},
        {"word": "çotanak", "definition": "Fındığın birden çok meyvesinin bir arada bulunduğu kabuklu durumu."},
        {"word": "taşeron", "definition": "Büyük bir işin bir bölümünü yapmayı, ana müteahhitten devralan diğer yüklenici."},
        {"word": "iptidai", "definition": "İlkel, basit."},
        {"word": "tekabül", "definition": "Karşılık olma, denk gelme, yerini tutma."},
        {"word": "rehavet", "definition": "Vücuttaki gevşeklik, ağırlık, tembellik."},
        {"word": "ihtilal", "definition": "Bir ülkenin siyasal, sosyal ve ekonomik yapısını veya yönetim düzenini değiştirmek amacıyla kanunlara uymaksızın cebir ve kuvvet kullanarak yapılan geniş halk hareketi; devrim."}
    ],
    8: [
        {"word": "öküzgözü", "definition": "Kaliteli, kendine özgü kokusu olan, şarap üretilen, orta kalın kabuklu, siyah renkli bir tür üzüm."},
        {"word": "kaymakam", "definition": "Bir ilçede devleti temsil eden en yetkili yönetim görevlisi."},
        {"word": "muhabbet", "definition": "Sevgi, yarenlik, söyleşi."},
        {"word": "mükerrer", "definition": "Tekrarlı, yinelenmiş."},
        {"word": "müsterih", "definition": "Bütün kaygılardan kurtulup gönlü rahata kavuşan, içi rahat olan."},
        {"word": "platonik", "definition": "Gerçekte var olmayan, karşılığı bulunmayan, hayalde yaşatılan, hep öyle kalması istenilen."},
        {"word": "pervasız", "definition": "Çekinmez, sakınmaz, korkusuz (kimse)"}
    ],
    9: [
        {"word": "teferruat", "definition": "Ayrıntı, detay."},
        {"word": "ciğerpare", "definition": "Çok sevilen kimse, can parçası."},
        {"word": "minnettar", "definition": "Birinden gördüğü iyiliğe karşı kendini borçlu sayan, gönül borcu olan kimse; gönül borçlusu."},
        {"word": "ehemmiyet", "definition": "Önem, değer."},
        {"word": "sansasyon", "definition": "Toplumda merak ve heyecan uyandıran olay."},
        {"word": "kondisyon", "definition": "Vücudun dayanıklılık ve zindelik durumu."},
        {"word": "fevkalade", "definition": "Olağanüstü, çok iyi, alışılmışın dışında."}
    ],
    10: [
        {"word": "bankamatik", "definition": "Para çekme, yatırma gibi işlemlerin yapıldığı otomat."},
        {"word": "kadirşinas", "definition": "Değer bilen, iyiliği unutmayan."},
        {"word": "müştemilat", "definition": "Bir ana yapının eklentisi olan ve ona hizmet eden yapılar."},
        {"word": "savsaklama", "definition": "Bir işi sürekli erteleme, ihmal etme."},
        {"word": "zincirleme", "definition": "Birbirine bağlı olarak art arda gelen."},
        {"word": "mevzubahis", "definition": "Söz konusu, hakkında konuşulan."},
        {"word": "soruşturma", "definition": "Bir sorunu açıklığa kavuşturmak amacıyla bir idari veya adli makamın yönettiği, ilgililerden ve tanıklardan bilgi toplama, konuyu inceleme işi; tahkik, tahkikat."}
    ]
}

# Create a single, ordered list of all word/definition entries.
ALL_ENTRIES = []
for length in sorted(WORDS_AND_DEFS.keys()):
    ALL_ENTRIES.extend(WORDS_AND_DEFS[length])

# --- Helper Functions ---
def setup_new_word():
    """Sets up a new word and its definition for the game session."""
    if 'current_word_index' not in session or session['current_word_index'] >= len(ALL_ENTRIES) - 1:
        session['current_word_index'] = 0 # Loop back to the first word
    else:
        session['current_word_index'] += 1

    current_entry = ALL_ENTRIES[session['current_word_index']]
    session['current_word'] = current_entry['word']
    session['current_definition'] = current_entry['definition']
    session['displayed_letters'] = ['_'] * len(current_entry['word'])

# --- MODIFICATION START ---
def get_game_state_json():
    """Helper to create the JSON response for the current game state."""
    # The condition to check if the word is revealed has been REMOVED.
    # The definition is now sent with every game state update, right from the start.
    return {
        'slots': session.get('displayed_letters', []),
        'definition': session.get('current_definition', "Tanım yükleniyor..."),
    }
# --- MODIFICATION END ---

# --- Routes ---
@app.route('/')
def index():
    if 'current_word' not in session:
        session['current_word_index'] = -1
        setup_new_word()
    return render_template('index.html')

@app.route('/get_current_word_state', methods=['GET'])
def get_current_word_state():
    if 'current_word' not in session:
        session['current_word_index'] = -1
        setup_new_word()
    response = get_game_state_json()
    response['message'] = "Oyun Yüklendi."
    return jsonify(response)

@app.route('/next_word', methods=['POST'])
def next_word():
    setup_new_word()
    response = get_game_state_json()
    response['message'] = "Yeni kelime hazır!"
    return jsonify(response)

@app.route('/reveal_letter', methods=['POST'])
def reveal_letter():
    if 'current_word' not in session:
        return jsonify({'error': 'No active word'}), 400

    current_word = session['current_word']
    displayed_letters = list(session['displayed_letters'])
    unrevealed_indices = [i for i, char in enumerate(displayed_letters) if char == '_']

    if not unrevealed_indices:
        return jsonify({'message': "Bütün harfler zaten açık!", **get_game_state_json()})

    random_index = random.choice(unrevealed_indices)
    revealed_char = current_word[random_index]
    displayed_letters[random_index] = revealed_char
    session['displayed_letters'] = displayed_letters

    response = get_game_state_json()
    response['message'] = f"İpucu Harf: '{revealed_char}'"
    if all(slot != '_' for slot in response['slots']):
        response['message'] += " - Kelime açıklandı!"

    return jsonify(response)

@app.route('/reveal_word', methods=['POST'])
def reveal_word():
    if 'current_word' not in session:
        return jsonify({'error': 'No active word'}), 400
    session['displayed_letters'] = list(session['current_word'])
    response = get_game_state_json()
    response['message'] = "Kelime açıklandı!"
    return jsonify(response)

@app.route('/reveal_letter_at_index', methods=['POST'])
def reveal_letter_at_index():
    if 'current_word' not in session:
        return jsonify({'error': 'No active word'}), 400

    data = request.get_json()
    index = data.get('index')
    if index is None or not isinstance(index, int):
        return jsonify({'error': 'Invalid index provided'}), 400

    current_word = session['current_word']
    displayed_letters = list(session['displayed_letters'])

    if not (0 <= index < len(current_word)):
        return jsonify({'error': 'Index out of bounds'}), 400
    
    if displayed_letters[index] != '_':
        response = get_game_state_json()
        response['message'] = "Bu harf zaten açık."
        return jsonify(response)

    revealed_char = current_word[index]
    displayed_letters[index] = revealed_char
    session['displayed_letters'] = displayed_letters
    
    response = get_game_state_json()
    response['message'] = f"Harf açıklandı: '{revealed_char}'"
    if all(slot != '_' for slot in response['slots']):
        response['message'] += " - Kelime açıklandı!"
        
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
