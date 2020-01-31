const express = require("express");
const app = express();
const bodyparser = require("body-parser");
const multer = require('multer')
const firebase= require("./firinit");
const fs = require('fs');

app.use(bodyparser.urlencoded({
  extended: true
}));

var form = "<!DOCTYPE HTML><html><body>" +
"<form method='post' action='/upload' enctype='multipart/form-data'>" +
"<input type='file' name='upload'/>" +
"<input type='submit' /></form>" +
"</body></html>";


app.use("/uploads",express.static("./uploads"));

app.get('/', function (req, res){
  res.writeHead(200, {'Content-Type': 'text/html' });
  res.end(form);
});



var storage = multer.diskStorage({
  destination: './uploads',
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

var upload = multer({
  storage: storage
});
var mybucket=firebase.storage().bucket();

app.post("/upload", upload.single('upload'),
  async function (req, res) {
    console.log(req.body);
    console.log(req.file.filename);
    let response=await mybucket.upload("uploads/"+req.file.filename);
    let link="https://storage.googleapis.com/three-eyed-raven-e67c5.appspot.com/"+req.file.filename;
    let msgid=req.file.filename.replace(/\..+/g,"") || "unidentified";
    let from=req.file.filename.slice(10).replace(/\..+/g,"") || "unknown";
     firebase.firestore().collection("uploads").doc().set({
       msgid,
       time:+new Date(),
       data:link,
       from
     });
    return res.status(200).end("Uploaded image !");
  });



// function to encode file data to base64 encoded string
function base64_encode(file) {
    // read binary data
    var bitmap = fs.readFileSync(file);
    // convert binary data to base64 encoded string
    return new Buffer(bitmap).toString('base64');
}


app.use(bodyparser.json());


app.listen(3000);