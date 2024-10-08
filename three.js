var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('3dview').appendChild(renderer.domElement);

// Plane geometry (floor of the room)
var geometry = new THREE.PlaneGeometry(9, 5.74);
var material = new THREE.MeshBasicMaterial({color: 0xcccccc, side: THREE.DoubleSide});
var plane = new THREE.Mesh(geometry, material);
scene.add(plane);

// Blue dot to represent position in 3D
var dotGeometry = new THREE.SphereGeometry(0.1, 32, 32);
var dotMaterial = new THREE.MeshBasicMaterial({color: 0x0000ff});
var blueDot = new THREE.Mesh(dotGeometry, dotMaterial);
scene.add(blueDot);

// Camera position
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

// Animation loop to render the scene
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();

// Convert lat/lon to X, Y for 3D model
function convertLatLonToXY(lat, lon) {
    var latA = 30.8587234, lonA = 75.86167;
    var latD = 30.85825267, lonD = 75.8615873;

    var x = (lon - lonA) / (lonD - lonA) * 9;
    var y = (lat - latA) / (latA - latD) * 5.74;
    return {x: x, y: y};
}

// Listen for location updates via Socket.IO
socket.on('location_update', function (data) {
    var position = convertLatLonToXY(data.latitude, data.longitude);
    blueDot.position.set(position.x - 4.5, position.y - 2.87, 0);
});
