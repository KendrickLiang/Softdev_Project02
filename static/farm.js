console.log("connected");

var current_tile = null;

var farm = document.getElementsByClassName('farm-tile');
//console.log(farm);
/*
for(x = 0; x<farm.length; x++) {
    //console.log(x,farm[x]);
    farm[x].addEventListener("mouseover", function(e){
        //console.log(e);
    })
    //console.log(farm[x].innerHTML == 'Dirt');
    if (farm[x].innerHTML == 'Dirt') {
        farm[x].addEventListener("click", function(e) {
            this.innerHTML = "CLICK";
            current_tile = this;
        })
    }
}
*/
var tileSelect = function(tile_id) {
    current_tile = document.getElementById(tile_id);
}

var plant_crop = function(cropName) {
    if (current_tile != null) {
        console.log(current_tile);
        current_tile.innerHTML = cropName;
        current_tile.removeAttribute("onclick");
        current_tile.removeAttribute("data-open");
        current_tile = null;
    }
}

/*
var cropSelect = function(tile) {
    console.log(tile);
    console.log(document.getElementById('cropType').innerHTML);
    //var selector = document.getElementById('modal-button');
    document.addEventListener("click", function(e){
        console.log('Here');
        //console.log(document.getElementById('cropType').value);
        //tile.innerHTML = document.getElementById('cropType').value;
        tile.removeEventListener("click", function(e) {
            //this.innerHTML = "CLICK";
            cropSelect(this)
        });
        tile.addEventListener("mouseover", function(e){
        });
    })
}*/
