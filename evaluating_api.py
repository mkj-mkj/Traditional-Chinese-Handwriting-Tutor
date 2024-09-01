from flask import Flask, request, jsonify, Blueprint
import os
from .Evaluating import evaluation
import tempfile

evaluation_bp = Blueprint('evaluation', __name__,)

def save_image_to_temp_file(image_data):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(image_data)
    temp_file.close()
    return temp_file.name


@evaluation_bp.route('/evaluation', methods=['POST'])
def recognize():
    temp_image_path = None
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    try:
        image = request.files['image'].read() #獲取圖像的二進制數據
        temp_image_path = save_image_to_temp_file(image)
        
        print(f"儲存的圖片路徑: {temp_image_path}")

        api_key_path = 'path/to/vision_api.txt'
        #csv_folder_path = 'path/to/csv_files/'

        # 讀取 API Key
        #def read_api_key(filepath):
            #with open(filepath, 'r', encoding='utf-8-sig') as file:
                #return file.read().strip()
        #api_key = read_api_key(api_key_path)
        api_key = 'AIzaSyBWMTXSjokqtekyyPZbB2Bt3hDuOoj3xmc'

        # 執行字符辨識和比對
        result = evaluation(temp_image_path, api_key)
        print (result)
        return jsonify(result)
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        #清理臨時圖片
        if temp_image_path and os.path.exists(temp_image_path):
            os.remove(temp_image_path)


    

