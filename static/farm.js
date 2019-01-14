console.log("connected");

var current_tile = null;

var farm = document.getElementsByClassName('farm-tile');

for(x = 0; x<farm.length; x++) {
    farm[x].addEventListener("mouseover", function(e){
        //console.log(e);
    })
}

var crops = [];
var findCrops = function() {
    for(x = 0; x<farm.length; x++) {
        if (farm[x].innerHTML != "Tree" && farm[x].innerHTML != "Rock" && farm[x].innerHTML != "Dirt") {
                addCrop(farm[x]);
        }
    }
}

var addCrop = function(tile) {
    crops.push(tile);
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
        viewing_tile = current_tile;
        current_tile.innerHTML = cropName;
        addCrop(current_tile);
        current_tile.setAttribute("cropType", cropType);
        current_tile.setAttribute("gdd", 0);

        $.post( "/plantInfo", {
            "cropID": cropType
        }, function(data) {
            console.log(data);
            if (data['gddMaxBoundary'] == null) {
                viewing_tile.setAttribute("gdd_max", 30);
            } else {
                viewing_tile.setAttribute("gdd_max", data['gddMaxBoundary']);
            }
            viewing_tile.setAttribute("gdd_min", data['gddBaseTemp']);
        });


        current_tile.setAttribute("onclick", showInfo());
        current_tile.removeAttribute("data-open");
        current_tile = null;
    }
}

var showInfo = function() {

}

var updateTime = function() {
    // Clock UPDATE
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML =
    h + ":" + m + ":" + s;

    // Crop UPDATE
    for (index = 0; index < crops.length; index++) {
        crops[index].setAttribute("gdd", parseFloat(crops[index].getAttribute("gdd"))+15);
    }

    var t = setTimeout(updateTime, 1000);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

var init = function() {
    findCrops();
    updateTime();
}
