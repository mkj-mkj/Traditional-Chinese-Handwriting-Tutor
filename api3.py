import re
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-sourcecode', methods=['GET'])
def get_sourcecode():
    # 從查詢參數中獲取漢字
    character = request.args.get('character')
    
    if not character:
        return jsonify({'error': 'Character is required'}), 400
    
    # 發送 POST 請求到目標網站以獲取筆順動畫的 HTML
    url = 'https://stroke-order.learningweb.moe.edu.tw/showFlash.do'
    data = {
        'textfield': character,
        'show': '確定',
        'lang': 'zh_TW',
        'useAlt': '0'
    }
    
    response = requests.post(url, data=data)

    if response.status_code == 200:
        # 確保響應成功後再處理
        webpage_content = response.content.decode('utf-8')

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(webpage_content, 'html.parser')

        # 查找 id 為 'sourcecode' 的 textarea 元素
        sourcecode_element = soup.find('textarea', id='sourcecode')

        if sourcecode_element:
            # 提取 sourcecode 元素的內容
            sourcecode = sourcecode_element.prettify()
            sourcecode = sourcecode.replace('\\', '')
            # 使用正則表達式找到 JavaScript 程式碼並提取
            script_content = re.search(r'<script.*?</div>', sourcecode, re.DOTALL)
            if script_content:
                # 將 JavaScript 程式碼插入到你的 HTML 文件中
                return jsonify({'javascript': script_content.group(0)})
            else:
                return jsonify({'sourcecode': sourcecode})
        else:
            return jsonify({'error': 'Failed to find sourcecode element.'}), 404
    else:
        return jsonify({'error': f'Failed to retrieve webpage. Status code: {response.status_code}'}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)