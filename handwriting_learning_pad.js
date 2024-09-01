const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const lineWidth = document.getElementById("line-width");
const color = document.getElementById("color");
const destroyBtn = document.getElementById("destroy-btn")
const eraserBtn = document.getElementById("eraser-btn")
const fileInput = document.getElementById("file")
const saveBtn = document.getElementById("save-btn")
const predictionParagraph = document.getElementById('prediction');

const CANVAS_WIDTH = 400;
const CANVAS_HEIGHT = 400;

canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;
ctx.lineWidth = lineWidth.value;
ctx.lineCap = "round";

let isPainting = false;
let isFilling = false;
let isErasing = false;

function onMove(event) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (event.clientX - rect.left) * scaleX;
    const y = (event.clientY - rect.top) * scaleY;

    if (isPainting) {
        ctx.lineTo(x, y);
        ctx.stroke();
        return;
    }
    ctx.beginPath();
    ctx.moveTo(x, y);
}
/*
function drawGrid() {
    const gridSize = Math.min(CANVAS_WIDTH, CANVAS_HEIGHT);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255, 0, 0, 0.2)"; // 淺紅色
    ctx.lineWidth = 1;

    // 繪製兩條垂直線
    ctx.moveTo(gridSize / 2, 0);
    ctx.lineTo(gridSize / 2, gridSize);
    ctx.moveTo(gridSize * 1 / 2, 0);
    ctx.lineTo(gridSize * 1 / 2, gridSize);

    // 繪製兩條水平線
    ctx.moveTo(0, gridSize / 2);
    ctx.lineTo(gridSize, gridSize / 2);
    ctx.moveTo(0, gridSize * 1 / 2);
    ctx.lineTo(gridSize, gridSize * 1 / 2);

    ctx.stroke();
    ctx.closePath();

    // 重置線條樣式
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
}
*/

function startPainting() {
    isPainting = true;
}

function cancelPainting() {
    isPainting = false;
}

function onLineWidthChange(event) {
    ctx.lineWidth = event.target.value;
}

function onColorChange(event) {
    ctx.strokeStyle = event.target.value;
    ctx.fillStyle = event.target.value;
}

function onCanvasClick() {
    if(isFilling){
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    }
}

function onDestroyClick() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    predictionParagraph.textContent = "";
    initCanvas();  // 清除後重新初始化畫布
}

function onEraserClick() {
    if (isErasing) {
        isErasing = false;
        ctx.strokeStyle = color.value; // 切換回選擇的顏色
        eraserBtn.innerText = "Erase"; // 按鈕文字變回橡皮擦
    } else {
        isErasing = true;
        ctx.strokeStyle = "white"; // 設置為橡皮擦模式
        eraserBtn.innerText = "Pen"; // 按鈕文字變為畫筆
    }
}

function onFileChange(event) {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    const image = new Image();
    image.src = url;
    image.onload = function() {
        ctx.drawImage(image, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        fileInput.value = null;
    }
}

function onDoubleClick(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const text = textInput.value;
    if(text !== ""){
        ctx.save();
        ctx.lineWidth = 1;
        ctx.font = "68px sans-serif";
        ctx.fillText(text, x, y);
        ctx.restore();
    }
}

function onSaveClick() {
    const url = canvas.toDataURL();
    const a = document.createElement("a");
    a.href = url;
    a.download = "myDrawing.png";
    a.click();
}

function initCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; // 填充背景色
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    //drawGrid(); // 在畫布上繪製輔助線
}
function evaluation(){
    canvas.toBlob((blob) => {
        console.log(blob);
        const formData = new FormData();
        formData.append('image', blob, 'handwriting.png');

        // 確認 FormData 內容
        for (let pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]);
        }

        fetch('http://127.0.0.1:5000/evaluation/evaluation', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            if (data.error) {
                // 當回應包含錯誤訊息時顯示錯誤
                predictionParagraph.textContent = '錯誤: ' + data.error;
            } else {
                // 顯示相似度得分，格式化到小數點後兩位
                const formattedScore = data.similarity_score.toFixed(2);
                predictionParagraph.textContent = '相似度得分: ' + formattedScore;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            predictionParagraph.textContent = 'Error: ' + error;
        });
    }, 'image/png');
}

// 新增的腳本來處理API請求
function getStrokeOrder() {
const character = document.getElementById('character-input').value;
    if (!character) {
        alert('請輸入一個漢字');
        return;
    }
    // 將漢字轉換為 Unicode 編碼
    const unicodeCode = character.charCodeAt(0).toString(16).toUpperCase(); // 轉換為十六進制
    const encodedCode = unicodeCode.padStart(4, '0'); // 確保有 4 位數字

    // 使用轉換後的編碼創建 PlayerShare 實例
    try {
        console.log('Creating PlayerShare instance...');
        var playerShare = new PlayerShare('https://stroke-order.learningweb.moe.edu.tw/', encodedCode, '0', 'zh_TW');
        console.log('PlayerShare instance created.');
        playerShare.load();
        console.log('PlayerShare load method called.');
    } catch (error) {
        console.error('Error initializing PlayerShare:', error);
    }
}

document.getElementById('backButton');
backButton.addEventListener('click', function() {
    alert('放棄目前所有變更，返回上一頁');
    //window.history.back();
});


document.addEventListener('DOMContentLoaded', function() {
    initCanvas();
});
document.getElementById('submit-button').addEventListener('click', getStrokeOrder);
document.getElementById('upload').addEventListener('click', evaluation);

canvas.addEventListener("mousemove", onMove);
canvas.addEventListener("mousedown", startPainting);
canvas.addEventListener("mouseup", cancelPainting);
canvas.addEventListener("mouseleave", cancelPainting);
canvas.addEventListener("click", onCanvasClick);
canvas.addEventListener("dblclick", onDoubleClick);

lineWidth.addEventListener("change", onLineWidthChange);
color.addEventListener("change", onColorChange);
destroyBtn.addEventListener("click", onDestroyClick);
eraserBtn.addEventListener("click", onEraserClick);
fileInput.addEventListener("change", onFileChange);
saveBtn.addEventListener("click", onSaveClick);
