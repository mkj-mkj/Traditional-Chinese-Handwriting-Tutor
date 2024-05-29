document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
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
        drawGrid(); // Redraw the grid after clearing
    });

    // Save button
    document.getElementById('save').addEventListener('click', function() {
        const image = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
        const link = document.createElement('a');
        link.download = 'canvas.png';
        link.href = image;
        link.click();
    });
});