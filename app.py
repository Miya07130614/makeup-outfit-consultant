import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 設定允許上傳的檔案格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # 1. 獲取文字與下拉選單參數（若無選擇則套用智慧預設值）
    skin_tone = request.form.get('skin_tone', '自然膚色')
    style_preference = request.form.get('style', '日常休閒')
    occasion = request.form.get('occasion', '日常外出')
    
    # 確保空白欄位也能有預設值
    if not skin_tone: skin_tone = '自然膚色'
    if not style_preference: style_preference = '日常休閒'
    if not occasion: occasion = '日常外出'

    # 2. 處理圖片上傳（非強制，若無上傳則使用系統預設模特兒）
    has_image = False
    image_status = "使用系統預設模特兒進行分析"
    
    if 'user_photo' in request.files:
        file = request.files['user_photo']
        if file and file.filename != '' and allowed_file(file.filename):
            has_image = True
            image_status = f"成功接收使用者照片：{file.filename}"

    # 3. 模擬 AI 試衣與美學分析邏輯（後續可串接 Azure AI 或其他 API）
    # 這裡根據風格與膚色給出客製化建議
    recommendations = generate_consultant_report(skin_tone, style_preference, occasion)

    return jsonify({
        "status": "success",
        "image_handling": image_status,
        "input_summary": {
            "skin_tone": skin_tone,
            "style": style_preference,
            "occasion": occasion
        },
        "report": recommendations
    })

def generate_consultant_report(skin_tone, style, occasion):
    # 簡易的邏輯矩陣，模擬 AI 顧問的精準推薦
    colors = {
        "暖色調": "大地色系、燕麥色、芥末黃",
        "冷色調": "純白、寶藍、霧粉、冷灰",
        "自然膚色": "經典黑白、莫蘭迪色系、丹寧藍"
    }.get(skin_tone, "經典米色與丹寧")

    return {
        "color_analysis": f"針對您的【{skin_tone}】，推薦搭配【{colors}】，能最有效提亮氣色。",
        "outfit_suggestion": f"因應【{occasion}】場合，我們為您規劃的【{style}】穿搭方案為：質感純色上衣搭配剪裁俐落的下身，注重舒適與線條感。",
        "makeup_tip": "妝容建議保持乾淨底妝，搭配低飽和度的唇膏，展現高級偽素顏感。",
        "virtual_tryon_preview": f"已為您生成【{style}】風格的 AI 試衣虛擬預覽圖。"
    }

if __name__ == '__main__':
    # Render 會透過環境變數指定 Port，本機測試則預設 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
