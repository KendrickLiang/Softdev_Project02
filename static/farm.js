console.log("connected");

var farm = document.getElementsByClassName('farm-tile');
//console.log(farm);
for(x = 0; x<farm.length; x++) {
    //console.log(x,farm[x]);
    farm[x].addEventListener("mouseover", function(e){
        //console.log(e);
    })
    //console.log(farm[x].innerHTML == 'Dirt');
    if (farm[x].innerHTML == 'Dirt') {
        farm[x].addEventListener("click", function(e) {
            this.innerHTML = "CLICK";
            cropSelect(this)
        })
    }
}

var cropSelect = function(tile) {
    console.log(tile);
    console.log(document.getElementById('cropType').innerHTML);
    var selector = document.getElementById('modal-button');
    document.addEventListener("click", function(e){
        console.log('Here');
        console.log(document.getElementById('cropType').value);
        tile.innerHTML = document.getElementById('cropType').value;
        tile.removeEventListener("click", function(e) {
            //this.innerHTML = "CLICK";
            cropSelect(this)
        });
        tile.addEventListener("mouseover", function(e){
        });
    })
}
