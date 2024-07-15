const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const lineWidth = document.getElementById("line-width");
const color = document.getElementById("color");
const destroyBtn = document.getElementById("destroy-btn")
const eraserBtn = document.getElementById("eraser-btn")
const fileInput = document.getElementById("file")
const saveBtn = document.getElementById("save-btn")
const predictionParagraph = document.getElementById('prediction');

const CANVAS_WIDTH = window.innerWidth * 0.6;
const CANVAS_HEIGHT = window.innerHeight * 0.5;

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
    drawGrid(); // 在畫布上繪製輔助線
}

function uploadImage() {
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'handwriting.png');

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            predictionParagraph.textContent = 'Predicted Character: ' + data['Predicted Character'];
        })
        .catch((error) => {
            console.error('Error:', error);
            predictionParagraph.textContent = 'Error: ' + error;
        });
    }, 'image/png');
}

document.getElementById('backButton');
backButton.addEventListener('click', function() {
    alert('放棄目前所有變更，返回上一頁');
    //window.history.back();
});


document.addEventListener('DOMContentLoaded', function() {
    initCanvas();
});
document.getElementById('upload').addEventListener('click', uploadImage);

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
