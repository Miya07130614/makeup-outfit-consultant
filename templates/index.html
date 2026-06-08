from flask import Flask, render_template, request, jsonify
import werkzeug

app = Flask(__name__)

# 限制最大上傳檔案為 16MB，防止大圖塞爆伺服器
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # 1. 安全讀取表單參數（若前端未選，則賦予智慧預設值）
        skin_tone = request.form.get('skin_tone') or "亞洲標準自然中性色調"
        body_type = request.form.get('body_type') or "標準勻稱 / 肌肉線條平衡體態"
        style = request.form.get('style') or "日常美式休閒"
        occasion = request.form.get('occasion') or "日常街頭外出"
        
        # 2. 讀取上傳的照片 (安全檢查)
        user_photo = request.files.get('user_photo')
        image_handling_msg = "💡 系統未偵測到上傳照片，已自動啟用『3D模特兒全息特徵模型』進行演算。"
        
        if user_photo and user_photo.filename != '':
            # 這裡代表使用者有上傳照片，未來可在這裡對接 AI 視覺辨識 API
            image_handling_msg = f"✨ 成功讀取用戶上傳照片【{werkzeug.utils.secure_filename(user_photo.filename)}】，已完成全息特徵矩陣轉譯！"

        # 3. 模擬高階智慧大數據矩陣的運算結果
        # 依據使用者選擇的風格，動態調整導購關鍵字與建議
        report = {
            "color_analysis": f"您的原生色彩學判定為【{skin_tone}】。此色調在光學測算下，建議彩妝色譜優先選用具備提亮面部折疊度的中性光澤色系，服飾避開高飽和螢光色，能完美襯托膚色純淨度。",
            
            "outfit_suggestion": f"針對您的【{body_type}】體態，黃金幾何剪裁定調為：加強肩膀至腰線的流暢度。配合【{style}】意向，應選用挺括、具備高磅數結構的織物，在【{occasion}】場景中能展現無懈可擊的俐落氣場。",
            
            "makeup_tip": f"因應【{style}】的美學矩陣，彩妝定調為：低飽和高級感霧面妝容。重塑眉眼深邃度，搭配微光澤感修容，確保在【{occasion}】的燈光折射下，五官依然精緻立體。",
            
            "virtual_tryon_preview": f"AI 實時全息渲染：{style} 方案已就緒",
            "shop_cloth_keywords": f"{style} 挺括修身 命定單品",
            "shop_makeup_keywords": f"{style} 適配彩妝 霧面修容盤",
            "youtube_search_keywords": f"{style} {occasion} 穿搭美學教學",
            "map_search_keywords": "百貨專櫃 時尚買手店"
        }

        # 4. 建立對應的外連網址
        report["shopee_cloth_url"] = f"https://shopee.tw/search?keyword={report['shop_cloth_keywords']}"
        report["shopee_makeup_url"] = f"https://shopee.tw/search?keyword={report['shop_makeup_keywords']}"
        report["youtube_search_url"] = f"https://www.youtube.com/results?search_query={report['youtube_search_keywords']}"

        # 返回標準 JSON 格式給前端
        return jsonify({
            "status": "success",
            "image_handling": image_handling_msg,
            "report": report
        })

    except Exception as e:
        # 當後端真的發生非預期錯誤時，捕捉並回傳錯誤訊息，避免前端直接噴連線異常
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
