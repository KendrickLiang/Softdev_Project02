console.log("connected");

var farm = document.getElementsByClassName('farm-tile');
console.log(farm);
for(x = 0; x<farm.length; x++) {
    console.log(x,farm[x]);
    farm[x].addEventListener("mouseover", function(e){
        console.log(e);
    })
    console.log(farm[x].innerHTML == 'G');
    if (farm[x].innerHTML == 'G') {
        farm[x].addEventListener("click", function(e) {
            this.innerHTML = "CLICK";
        })
    }
}
