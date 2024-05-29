document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const predictionParagraph = document.getElementById('prediction');
    ctx.lineWidth = 2; // Setting the line width for the grid and drawing

    // Function to draw grid
    function drawGrid() {
        ctx.strokeStyle = 'rgba(255, 0, 0, 0.4)'; // Red color with lower opacity
        ctx.beginPath();
        // Draw horizontal line
        ctx.moveTo(0, canvas.height / 2);
        ctx.lineTo(canvas.width, canvas.height / 2);
        // Draw vertical line
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
    }

    // Initialize canvas background and grid
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid();

    // Setup drawing
    let drawing = false;
    canvas.addEventListener('mousedown', function(e) {
        drawing = true;
        ctx.beginPath();
        ctx.strokeStyle = 'black'; // Set the stroke color to black for drawing
        ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    });

    canvas.addEventListener('mousemove', function(e) {
        if (drawing) {
            ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
            ctx.stroke();
        }
    });

    canvas.addEventListener('mouseup', function() {
        drawing = false;
    });

    // Clear button 
    document.getElementById('clear').addEventListener('click', function() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; // Set the fill color to white
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill the canvas with white
    drawGrid(); // Redraw the grid after clearing
    predictionParagraph.textContent = ""
    });
    
    // Save button
    document.getElementById('save').addEventListener('click', function() {
        const image = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
        const link = document.createElement('a');
        link.download = 'canvas.png';
        link.href = image;
        link.click();
    });

    // Upload button
    document.getElementById('upload').addEventListener('click', () => {
        canvas.toBlob((blob) => {
          /*
          // 創建URL以便在頁面上顯示圖像
          const imgUrl = URL.createObjectURL(blob);
          const img = document.createElement('img');
          img.src = imgUrl;
          document.body.appendChild(img); // 在頁面上顯示圖像以確認
          imageContainer.innerHTML = ''; // 清空容器
          imageContainer.appendChild(img); // 添加新的圖像
          */
  
          const formData = new FormData();
          formData.append('image', blob, 'handwriting.png');
          // 後端位址
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
      });
});
