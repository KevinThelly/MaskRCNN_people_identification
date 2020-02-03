

function get(){
    var json=JSON.parse(require("../output/data.json"));
    console.log(json)
    var coords=json["coords"] || [];
    var count=json["count"];
    var width=json["width"];
    var height=json["height"];
    console.log(height)
}

get()