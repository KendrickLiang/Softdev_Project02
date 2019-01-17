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
    var tiles = document.getElementsByClassName('farm-tile');
    $.post( "/getCrop", {
    }, function(data) {
        data = JSON.parse(data);
        console.log(data);
        list = data['cropList'].split(";");
        if (list[0] != "")  {
            for(x = 0; x < list.length; x++) {
                attributes = list[x].split("$?");
                target = tiles[parseInt(list[0])];
                target.setAttribute("cropType", list[1]);
                target.setAttribute("gdd", list[2]);
                target.setAttribute("gdd_max", list[3]);
                target.setAttribute("gdd_min", list[4]);
                target.setAttribute("stages", list[5]);
                target.setAttribute("onclick", "showInfo('" + list[0] + "')");
                target.removeAttribute("data-open");
                addCrop(target);
            }
        }
    })
}

var addCrop = function(tile) {
    crops.push(tile);
}

var removeCrop = function(tile) {
    crops.splice(crops.indexOf(tile), 1);
}

var resetTile = function(tile) {
    tile.innerHTML = "Dirt";
    tile.removeAttribute("cropType");
    tile.removeAttribute("gdd");
    tile.removeAttribute("gdd_max");
    tile.removeAttribute("gdd_min");
    tile.removeAttribute("stages");
    tile.setAttribute("class", "farm-tile Dirt")
    tile.setAttribute("onclick", "tileSelect('" + viewing_tile.getAttribute("index") + "')");
    tile.setAttribute("data-open", "");
    removeCrop(tile);
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
        viewing_tile.innerHTML = cropName;
        addCrop(viewing_tile);
        viewing_tile.setAttribute("cropType", cropType);
        viewing_tile.setAttribute("gdd", 0);

        $.post( "/plantInfo", {
            "cropID": cropType
        }, function(data) {
            //console.log(typeof data);
            data = JSON.parse(data);
            //console.log(typeof data);
            if (""+data['gddMaxBoundary'] == null) {
                viewing_tile.setAttribute("gdd_max", 30);
            } else {
                viewing_tile.setAttribute("gdd_max", ""+data['gddMaxBoundary']);
            }
            //console.log(data['gddMaxBoundary']);
            viewing_tile.setAttribute("gdd_min", ""+data['gddBaseTemp']);
            viewing_tile.setAttribute("stages", JSON.stringify(data['stages']));
        });

        //console.log("HERE", viewing_tile);
        viewing_tile.setAttribute("class", "farm-tile " + viewing_tile.innerHTML)
        viewing_tile.setAttribute("onclick", "showInfo('" + viewing_tile.getAttribute("index") + "')");
        viewing_tile.removeAttribute("data-open");
        current_tile = null;
    }
}

var showInfo = function(tile_id) {
    num =  parseInt(tile_id,10);
    t = farm[num];
    gdd = t.getAttribute("gdd");
    stages = JSON.parse(t.getAttribute('stages'));
    //console.log(typeof stages);
    //console.log(stages);
    for (index = stages.length-1; index >= 0; index--) {
        if (gdd >= parseInt(stages[index]['gddThreshold']) ) {
            if (index == stages.length-1) {
                if (gdd >= 2 * parseInt(stages[index]['gddThreshold'])) {
                    message = "" + t.getAttribute('id') + " : " + t.innerHTML +
                    "\nat GDD of " + gdd + " has rotted away\nBetter luck next time!";
                    resetTile(t);
                } else {
                    message = "" + t.getAttribute('id') + " : " + t.innerHTML +
                    "\nat GDD of " + gdd + " has been harvested\n+$10 to account";
                    updateCash(10);
                    resetTile(t);
                }
            } else {
                message = "" + t.getAttribute('id') + " : " + t.innerHTML +
                "\nCurrent GDD : " + gdd +
                "\nCurrent Stage : " + stages[index]['id'] +
                "\nDescription : " + stages[index]['description'];
            }
            alert(message);
            index = -1;
            return '';
        }
    }
    message = "" + t.getAttribute('id') + " : " + t.innerHTML +
    "\nCurrent GDD : " + gdd +
    "\nNo Growth";
    alert(message);
    return '';
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
    if (true) { // isDay
        for (index = 0; index < crops.length; index++) {
            crops[index].setAttribute("gdd", parseFloat(crops[index].getAttribute("gdd"))+15);
            //gdd = crops[index].getAttribute("gdd");
            //stages = JSON.parse(crops[index].getAttribute('stages'))
            //if (gdd >= 2 * parseInt(stages[stages.length-1]['gddThreshold'])) {
            //    message = "" + t.getAttribute('id') + " : " + t.innerHTML +
            //    "\nat GDD of " + gdd + " has rotted away\nBetter luck next time!";
            //    resetTile(t);
            //}
        }
    }
    var t = setTimeout(updateTime, 1000);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

var current_temperature;
var isDay;
var rainBoost;

var getWeather = function(e) {
    $.post( "/weatherInfo", {
    }, function(data) {
        console.log(typeof data);
        data = JSON.parse(data)['0'];
        console.log(typeof data);
        console.log(data);
        current_temperature = parseFloat(data['Temperature']['Metric']['Value']);
        if (data['IsDayTime'] == "true") {
            isDay = true;
        } else {
            isDay = false;
        }
        if (data['HasPrecipitation'] == "true" && data['PrecipitationType'] == "Rain") {
            rainBoost = true;
        } else {
            rainBoost = false;
        }
    });
    var weather = setTimeout(getWeather, 600000);
}

var updateCash = function(num) {
    data = {
        'cashNum': num
    }
    $.post("/updateCash", data)
    document.getElementById('cashAmount').innerHTML = parseInt(document.getElementById('cashAmount').innerHTML) + num;
}

var saveMap = function() {
    var map = "";
    var cropListing = "";
    var count = 0;
    for(x = 0; x<farm.length; x++) {
        if (count == 9) {
            map += farm[x].innerHTML + ";";
            count = 0;
        } else {
            map += farm[x].innerHTML + ",";
            count += 1;
        }
    }
    for (x = 0; x<crops.length; x++) {
        // index;,cropType;,gdd;,gdd_max;,gdd_min;,stages;
        cropListing +=
            crops[x].getAttribute('index') + "$?" +
            crops[x].getAttribute('cropType') + "$?" +
            crops[x].getAttribute('gdd') + "$?" +
            crops[x].getAttribute('gdd_max') + "$?" +
            crops[x].getAttribute('gdd_min') + "$?" +
            crops[x].getAttribute('stages') + ";";
    }
    document.getElementById('save_time').innerHTML = document.getElementById('time').innerHTML
    dataSent = {
        'map': map,
        'cropsMap': cropListing
    }
    $.post("/updateMap", dataSent);
}

var init = function() {
    findCrops();
    getWeather();
    updateTime();
}
