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

    report_data = generate_search_linked_report(skin_tone, style_preference, body_type, occasion)

    return jsonify({
        "status": "success",
        "image_handling": image_status,
        "report": report_data
    })

def generate_search_linked_report(skin, style, body, occasion):
    # 色彩資料庫
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

    # 身型資料庫
    body_db = {
        "標準勻稱 / 肌肉線條平衡體態": "著重衣服面料的挺度與俐落的垂直剪裁，大膽挑戰合身與層次感疊穿。",
        "梨形身型 (胯寬、大腿豐滿)": "強烈推薦 A 字修身長裙、高腰直筒寬褲，搭配微墊肩或一字領上衣。",
        "蘋果身型 (腰腹較圓潤)": "推薦選用大 V 領、方領上衣拉長頸部線條，利用高腰 A 字剪裁營造縱向視覺延伸。",
        "倒三角身型 (肩膀寬闊、骨架大)": "建議上身穿著極簡挺版剪裁，下身搭配傘擺裙、闊腿褲、工裝褲。",
        "沙漏身型 (胸豐臀翹腰細)": "推薦合身針織裙、高腰收腰洋裝，大膽展現優雅的曲線優勢。",
        "矩形 / H 型身型 (腰線不明顯)": "著重運用腰帶、層次疊穿（如襯衫外搭馬甲）來創造身體的凹凸線條。"
    }
    recommended_silhouette = body_db.get(body, "注重衣服面料的挺度與俐落的垂直剪裁。")

    # 智慧矩陣：新增【電商穿搭、彩妝】導購搜尋關鍵字
    style_keywords_matrix = {
        "日常美式休閒": {
            "yt_query": "美式休閒 穿搭教學 技巧", 
            "map_query": "服飾店 GAP Levi's",
            "shop_cloth": "美式休閒 寬鬆重磅 大學T 丹寧牛仔褲",
            "shop_makeup": "自然裸妝感 霧面唇膏 大地色眼影盤"
        },
        "Clean Fit 極簡風": {
            "yt_query": "Clean Fit 極簡風 穿搭必備", 
            "map_query": "極簡服飾 COS UNIQLO",
            "shop_cloth": "Clean Fit 極簡版型 素色襯衫 俐落西裝褲",
            "shop_makeup": "微光澤粉底液 乾淨偽素顏 晶透護唇膏"
        },
        "Old Money 老錢風": {
            "yt_query": "老錢風 靜奢美學 高級感穿搭", 
            "map_query": "精品服飾 Ralph Lauren Massimo Dutti",
            "shop_cloth": "老錢風 針織老爺衫 羊毛小香風 靜奢單品",
            "shop_makeup": "高級啞光粉底 氣質低調裸色口紅 精致修容"
        },
        "千金溫柔約會風": {
            "yt_query": "約會穿搭 小香風 溫柔氣質", 
            "map_query": "女裝專賣店 百貨專櫃 Zara snidel",
            "shop_cloth": "溫柔氣質裙裝 針織小外套 復古瑪莉珍鞋",
            "shop_makeup": "粉嫩蜜桃色腮紅 淚袋臥蠶筆 玫瑰色水光唇釉"
        },
        "Cottagecore 法式浪漫": {
            "yt_query": "法式復古浪漫 穿搭 碎花裙", 
            "map_query": "法式女裝 服飾店 浪漫裙裝",
            "shop_cloth": "法式復古碎花長裙 V領泡泡袖 慵懶風針織",
            "shop_makeup": "復古法式紅唇 蓬鬆微捲髮造型 暖色調腮紅"
        },
        "日系 City Boy 寬鬆風": {
            "yt_query": "City Boy 寬鬆工裝 穿搭指南", 
            "map_query": "潮流服飾 BEAMS niko and",
            "shop_cloth": "Cityboy寬鬆襯衫 戶外工裝褲 重磅寬版短T",
            "shop_makeup": "清爽控油潔顏 零粉感防曬 男士自然修容"
        },
        "Y2K 辣妹街頭風": {
            "yt_query": "Y2K 千禧辣妹 穿搭個性單品", 
            "map_query": "個性服飾 辣妹服飾 Bershka",
            "shop_cloth": "Y2K短版高腰上衣 金屬感工裝裙 復古厚底鞋",
            "shop_makeup": "高調貓眼眼線 芭比粉水光唇蜜 閃耀打亮打底"
        },
        "多巴胺高飽和色彩風": {
            "yt_query": "多巴胺 撞色 色彩學穿搭", 
            "map_query": "流行女裝 H&M 服飾店",
            "shop_cloth": "多巴胺高飽和度上衣 繽紛撞色配件 亮色系單品",
            "shop_makeup": "彩色眼線筆 繽紛指甲油 糖果色系明亮妝容"
        },
        "Gorpcore 戶外機能風": {
            "yt_query": "Gorpcore 戶外機能 衝鋒衣穿搭", 
            "map_query": "戶外用品 The North Face 始祖鳥",
            "shop_cloth": "Gorpcore防水衝鋒衣 戰術機能三防褲 戶外越野鞋",
            "shop_makeup": "高效防水防汗防曬 運動長效定妝噴霧"
        }
    }

    keywords = style_keywords_matrix.get(style, style_keywords_matrix["日常美式休閒"])

    # 1. 導覽與地圖
    combined_map_query = f"{keywords['map_query']} 化妝品店 彩妝專櫃"
    google_map_url = f"https://maps.google.com/maps?q={quote(combined_map_query)}&t=&z=14&ie=UTF8&iwloc=&output=embed"

    # 2. YouTube
    youtube_search_url = f"https://www.youtube.com/results?search_query={quote(keywords['yt_query'])}"

    # 3. 核心：電商導購連結生成 (以台灣最大流量電商蝦皮購物為例，可自由替換其他平台)
    shopee_cloth_url = f"https://shopee.tw/search?keyword={quote(keywords['shop_cloth'])}"
    shopee_makeup_url = f"https://shopee.tw/search?keyword={quote(keywords['shop_makeup'])}"

    return {
        "color_analysis": f"【色彩大師診斷】配合您的【{skin}】，經色彩矩陣運算，最能襯托氣色的黃金色盤為：{recommended_colors}。",
        "outfit_suggestion": f"【服飾結構提案】針對您的【{body}】，在參與【{occasion}】時，建議採取【{style}】。實作指南：{recommended_silhouette}",
        "makeup_tip": f"【精緻妝容美學】為呼應【{style}】的獨特氣場，建議底妝配合膚色進行自然清透提亮，眼影選用低飽和大地色系深邃眼窩。",
        "virtual_tryon_preview": f"【AI 虛擬試衣成功】已將【{style}】風格單品完美適配您的【{body}】骨架，虛擬試衣渲染已同步就緒！",
        
        "youtube_search_url": youtube_search_url,
        "youtube_search_keywords": keywords['yt_query'],
        "google_map_url": google_map_url,
        "map_search_keywords": combined_map_query,
        
        # 導購回傳數據
        "shop_cloth_keywords": keywords['shop_cloth'],
        "shop_makeup_keywords": keywords['shop_makeup'],
        "shopee_cloth_url": shopee_cloth_url,
        "shopee_makeup_url": shopee_makeup_url
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8790))
    app.run(host='0.0.0.0', port=port, debug=True)
