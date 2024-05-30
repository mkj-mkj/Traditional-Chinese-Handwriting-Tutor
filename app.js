const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const lineWidth = document.getElementById("line-width");
const color = document.getElementById("color");
const destroyBtn = document.getElementById("destroy-btn")
const eraserBtn = document.getElementById("eraser-btn")
const fileInput = document.getElementById("file")
const saveBtn = document.getElementById("save-btn")

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
    if(isPainting){
        ctx.lineTo(event.offsetX, event.offsetY);
        ctx.stroke();
        return;
    }
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
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
    predictionParagraph.textContent = ""
    initCanvas();  // 清除后重新初始化画布
}

function onEraserClick() {
    if (isErasing) {
        isErasing = false;
        ctx.strokeStyle = color.value; // 切换回选择的颜色
        eraserBtn.innerText = "Erase"; // 按钮文字变回橡皮擦
    } else {
        isErasing = true;
        ctx.strokeStyle = "white"; // 设置为橡皮擦模式
        eraserBtn.innerText = "Pen"; // 按钮文字变为画笔
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
    const text = textInput.value;
    if(text !==""){
        ctx.save();
        ctx.lineWidth = 1;
        ctx.font = "68px sans-serif";
        ctx.fillText(text, event.offsetX, event.offsetY)
        ctx.restore();
    }
}

function onSaveClick() {
    const url = canvas.toDataURL()
    const a = document.createElement("a")
    a.href = url;
    a.download = "myDrawing.png";
    a.click();
}

function drawGrid() {
    ctx.save(); // 保存当前画布状态
    ctx.strokeStyle = 'rgba(255, 0, 0, 0.5)'; // 红色透明线
    ctx.lineWidth = 1; // 设置线宽
    ctx.beginPath();
    // 绘制纵向线
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    // 绘制横向线
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();
    ctx.restore(); // 恢复到之前的状态
}

function initCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; // 填充背景色
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid(); // 在画布上绘制辅助线
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
