// https://codepen.io/amir-s/pen/jzqZdG?editors=0010

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

let canvas;
let currColor = '#8080ff';

let ws;

const controls = {
  view: {x: 0, y: 0, zoom: 11},
  viewPos: { prevX: null,  prevY: null,  isDragging: false },
}

const warn = (duration) => {
  Toastify({
    position: "left",
    text: "Você tem que esperar",
    duration,
    style: {
      background: 'linear-gradient(to right, #ff4949 , #c63c3c)'
    }
    
  }).showToast();
}

const setTile = async (x, y, color) => {
  const tile = {x, y, color};
  const xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = () => {
    if (xmlhttp.readyState === 4) {
      console.log(xmlhttp.response);
    }
  }
  xmlhttp.open("POST", `${API_URL}/tile`, true);
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.send(JSON.stringify(tile));
}

function preload() {

  controls.view.x = (window.innerWidth - 100*controls.view.zoom)/2;
  controls.view.y = (window.innerHeight - 100*controls.view.zoom)/2;


  img = createImage(100, 100);
  for (let i = 0; i < img.width; i++) {
    for (let j = 0; j < img.height; j++) {
      img.set(i, j, color(255, 255, 255));
    }
  }
  
  const xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = () => {
    if (xmlhttp.readyState === 4) {
      const { place: tiles} = JSON.parse(xmlhttp.response);
      tiles.forEach((tile) => {
        const {x, y, color: c} = tile;
        img.set(x, y, color(c));
      })
    }
  }
  xmlhttp.open("GET", `${API_URL}/place`, true);
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.send();

  ws = new WebSocket(WS_URL);
  ws.onopen = () => {
    console.log('connected to websocket');
  }
  ws.onmessage = (e) => {
    const {x, y, color: c} = JSON.parse(e.data);
    img.set(x, y, color(c));
  }
}

function setup() {
	canvas = createCanvas(window.innerWidth, window.innerHeight);
  canvas.parent('container');
  canvas.mouseWheel(e => Controls.zoom(controls).worldZoom(e))
  const inputDiv = document.getElementById('color');
  inputDiv.value = currColor;
  inputDiv.addEventListener('change', (event) => {
    currColor = event.target.value;
  });
  frameRate(240);
}

function draw() {
  noSmooth();
	background(100)
  translate(controls.view.x, controls.view.y);
  scale(controls.view.zoom)
  image(img, 0, 0)
  img.updatePixels()
}

window.mousePressed = e => Controls.move(controls).mousePressed(e)
window.mouseDragged = e => Controls.move(controls).mouseDragged(e);
window.mouseReleased = e => Controls.move(controls).mouseReleased(e);

class Controls {
  static move(controls) {
    function mousePressed(e) {
      controls.viewPos.prevX = e.clientX;
      controls.viewPos.prevY = e.clientY;
    }

    function mouseDragged(e) {
      const {prevX, prevY, isDragging} = controls.viewPos;
      controls.viewPos.isDragging = true;

      const pos = {x: e.clientX, y: e.clientY};
      const dx = pos.x - prevX;
      const dy = pos.y - prevY;

      if(prevX || prevY) {
        controls.view.x += dx;
        controls.view.y += dy;
        controls.viewPos.prevX = pos.x, controls.viewPos.prevY = pos.y
      }
    }

    function mouseReleased(e) {
      if(!controls.viewPos.isDragging) {
        const x = Math.floor((e.clientX - controls.view.x)/controls.view.zoom);
        const y = Math.floor((e.clientY - controls.view.y)/controls.view.zoom);
        setTile(x, y, currColor)
        warn(2000)
      }

      controls.viewPos.isDragging = false;
      controls.viewPos.prevX = null;
      controls.viewPos.prevY = null;
    }
 
    return {
      mousePressed, 
      mouseDragged, 
      mouseReleased
    }
  }

  static zoom(controls) {
    // function calcPos(x, y, zoom) {
    //   const newX = width - (width * zoom - x);
    //   const newY = height - (height * zoom - y);
    //   return {x: newX, y: newY}
    // }

    function worldZoom(e) {
      const {x, y, deltaY} = e;
      const direction = deltaY > 0 ? -1 : 1;
      const factor = 1;
      let zoom = 1 * direction * factor;

      if(controls.view.zoom + zoom < 1 || controls.view.zoom + zoom > 16) return; 
      
      const wx = (x-controls.view.x)/(width*controls.view.zoom);
      const wy = (y-controls.view.y)/(height*controls.view.zoom);
      controls.view.x -= wx*width*zoom;
      controls.view.y -= wy*height*zoom;
      controls.view.zoom += zoom;
    }

    return {worldZoom}
  }
}
