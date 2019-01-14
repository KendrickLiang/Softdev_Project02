console.log("connected");

var current_tile = null;

var farm = document.getElementsByClassName('farm-tile');

for(x = 0; x<farm.length; x++) {
    farm[x].addEventListener("mouseover", function(e){
        //console.log(e);
    })
}

var tileSelect = function(tile_id) {
    console.log(farm);
    num =  parseInt(tile_id,10);
    t = farm[num];
    //console.log(tile_id, num, document.getElementById(tile_id), t);
    current_tile = t;
    //console.log(current_tile);
}

var plant_crop = function(cropName, cropType) {
    if (current_tile != null) {
        console.log(current_tile);
        current_tile.innerHTML = cropName;
        current_tile.setAttribute("cropType", cropType);
        current_tile.removeAttribute("onclick");
        current_tile.removeAttribute("data-open");
        current_tile = null;
    }
}

var updateTime = function() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML =
    h + ":" + m + ":" + s;
    var t = setTimeout(updateTime, 1000);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}
