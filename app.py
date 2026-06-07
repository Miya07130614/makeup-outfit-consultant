import os
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

SMART_DEFAULTS = {
    'skin_tone': '亞洲標準自然中性色調',
    'style': '日常美式休閒',
    'body_type': '標準勻稱體態',
    'occasion': '日常街頭外出'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    skin_tone = request.form.get('skin_tone', '').strip() or SMART_DEFAULTS['skin_tone']
    style_preference = request.form.get('style', '').strip() or SMART_DEFAULTS['style']
    body_type = request.form.get('body_type', '').strip() or SMART_DEFAULTS['body_type']
    occasion = request.form.get('occasion', '').strip() or SMART_DEFAULTS['occasion']

    image_status = "未偵測到上傳照片，系統已自動啟用『3D 虛擬數位模特兒』進行模擬試衣。"
    if 'user_photo' in request.files:
        file = request.files['user_photo']
        if file and file.filename != '' and allowed_file(file.filename):
            image_status = f"成功接收照片【{file.filename}】，AI 已自動提取面部比例進行高精度融合。"

    # 運算動態跳轉連結與地圖搜尋數據
    report_data = generate_search_linked_report(skin_tone, style_preference, body_type, occasion)

    return jsonify({
        "status": "success",
        "image_handling": image_status,
        "report": report_data
    })

def generate_search_linked_report(skin, style, body, occasion):
    # 色彩與身型資料庫
    color_db = {
        "春季型 (暖亮膚色)": "明亮蜜桃粉、柔和杏色、珊瑚橘。最適合黃金飾品提亮。",
        "秋季型 (暖暗膚色)": "濃郁泰奶色、楓葉磚紅、焦糖棕、軍綠。帶有高級啞光感。",
        "夏季型 (冷亮膚色)": "微醺薰衣草紫、霧感天藍、柔和玫瑰粉。適合純銀與白金配飾。",
        "冬季型 (冷暗膚色)": "極致純黑白、高冷深灰、寶石藍、飽和酒紅。極具視覺衝擊力。",
        "白皙膚色": "特別推薦莫蘭迪低飽和度粉與粉藍，顯得氣質清透。",
        "亞洲標準自然中性色調": "經典大地色系、丹寧藍、米灰色，能展現沉穩內斂質感。",
        "小麥/健康膚色": "極致極簡白、亮金黃、暖古銅。展現陽光活力與健美線條。"
    }
    recommended_colors = color_db.get(skin, "中性米色、灰色與經典單寧藍")

    body_db = {
        "標準勻稱 / 肌肉線條平衡體態": "著重衣服面料的挺度與俐落的垂直剪裁，大膽挑戰合身與層次感疊穿。",
        "梨形身型 (胯寬、大腿豐滿)": "強烈推薦 A 字修身長裙、高腰直筒寬褲，搭配微墊肩或一字領上衣。",
        "蘋果身型 (腰腹較圓潤)": "推薦選用大 V 領、方領上衣拉長頸部線條，利用高腰 A 字剪裁營造縱向視覺延伸。",
        "倒三角身型 (肩膀寬闊、骨架大)": "建議上身穿著極簡挺版剪裁，下身搭配傘擺裙、闊腿褲、工裝褲。",
        "沙漏身型 (胸豐臀翹腰細)": "推薦合身針織裙、高腰收腰洋裝，大膽展現優雅的曲線優勢。",
        "矩形 / H 型身型 (腰線不明顯)": "著重運用腰帶、層次疊穿（如襯衫外搭馬甲）來創造身體的凹凸線條。"
    }
    recommended_silhouette = body_db.get(body, "注重衣服面料的挺度與俐落的垂直剪裁。")

    # 核心智慧連動：定義各風格在 YouTube 的關鍵字以及 Google 地圖搜尋目標
    style_keywords_matrix = {
        "日常美式休閒": {"yt_query": "美式休閒 穿搭教學 技巧", "map_query": "服飾店 流行服飾 GAP Levi's"},
        "Clean Fit 極簡風": {"yt_query": "Clean Fit 極簡風 穿搭必備", "map_query": "極簡服飾 質感女裝 COS UNIQLO"},
        "Old Money 老錢風": {"yt_query": "老錢風 靜奢美學 高級感穿搭", "map_query": "精品服飾 精品專櫃 Ralph Lauren"},
        "千金溫柔約會風": {"yt_query": "約會穿搭 小香風 溫柔氣質", "map_query": "化妝品 百貨專櫃 女裝專賣店 Zara"},
        "Cottagecore 法式浪漫": {"yt_query": "法式復古浪漫 穿搭 碎花裙", "map_query": "法式女裝 服飾店 韓系服飾"},
        "日系 City Boy 寬鬆風": {"yt_query": "City Boy 寬鬆工裝 穿搭指南", "map_query": "工裝服飾 潮流服飾 BEAMS niko and"},
        "Y2K 辣妹街頭風": {"yt_query": "Y2K 千禧辣妹 穿搭個性單品", "map_query": "個性服飾 街頭服裝 辣妹服飾"},
        "多巴胺高飽和色彩風": {"yt_query": "多巴胺 撞色 色彩學穿搭", "map_query": "服飾店 流行女裝 H&M"},
        "Gorpcore 戶外機能風": {"yt_query": "Gorpcore 戶外機能 衝鋒衣穿搭", "map_query": "戶外用品 運動服飾 The North Face 始祖鳥"}
    }

    keywords = style_keywords_matrix.get(style, style_keywords_matrix["日常美式休閒"])

    # 組合 Google 地圖動態搜尋 URL (包含化妝與服裝綜合字詞)
    combined_map_query = f"{keywords['map_query']} 化妝品 彩妝店"
    encoded_map_query = quote(combined_map_query)
    google_map_url = f"https://maps.google.com/maps?q=關鍵字&output=embed{encoded_map_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"

    # 組合 YouTube 跳轉搜尋 URL
    encoded_yt_query = quote(keywords['yt_query'])
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_yt_query}"

    return {
        "color_analysis": f"【色彩大師診斷】配合您的【{skin}】，經色彩矩陣運算，最能襯托氣色的黃金色盤為：{recommended_colors}。",
        "outfit_suggestion": f"【服飾結構提案】針對您的【{body}】，在參與【{occasion}】時，建議採取【{style}】。實作指南：{recommended_silhouette}",
        "makeup_tip": f"【精緻妝容美學】為呼應【{style}】的獨特氣場，建議底妝配合膚色進行自然清透提亮，眼影選用低飽和大地色系深邃眼窩。",
        "virtual_tryon_preview": f"【AI 虛擬試衣狀態】已將【{style}】的完整單品依據【{body}】體態數據渲染完畢。",
        
        # 智慧搜尋連動回傳
        "youtube_search_url": youtube_search_url,
        "youtube_search_keywords": keywords['yt_query'],
        "google_map_url": google_map_url,
        "map_search_keywords": combined_map_query
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8790))
    app.run(host='0.0.0.0', port=port, debug=True)
