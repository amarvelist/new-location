// Socket.IO connection to listen for location updates
var socket = io.connect(window.location.origin);

// Get the 2D canvas context
var canvas = document.getElementById("map");
var context = canvas.getContext("2d");

// Room corners (from your architectural map)
var corners = {
    A: {lat: 30.8587234, lon: 75.86167},
    B: {lat: 30.85866605, lon: 75.86168643},
    C: {lat: 30.8584899, lon: 75.861709167},
    D: {lat: 30.85825267, lon: 75.8615873}
};

// Function to convert latitude and longitude to X, Y coordinates
function convertLatLonToXY(lat, lon) {
    var x = (lon - corners.A.lon) / (corners.D.lon - corners.A.lon) * 600;
    var y = (lat - corners.A.lat) / (corners.B.lat - corners.A.lat) * 400;
    return { x: x, y: y };
}

// Draw the room outline on the canvas
function drawRoom() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle = "#000";
    context.strokeRect(0, 0, 600, 400);
}

// Update the blue dot position on the 2D map
socket.on('location_update', function (data) {
    drawRoom();  // Redraw the room outline

    var position = convertLatLonToXY(data.latitude, data.longitude);

    // Draw the blue dot
    context.beginPath();
    context.arc(position.x, position.y, 5, 0, 2 * Math.PI, false);
    context.fillStyle = "blue";
    context.fill();
});
