const puputeer=require('puppeteer');
const request=require('request');
var firebase = require('firebase-admin');    
var serviceAccount = require('./ifp007-871c5ef9dc83.json');

firebase.initializeApp({
  credential: firebase.credential.cert(serviceAccount),
  databaseURL: 'https://ifp007.firebaseio.com'
});

db = firebase.firestore();
var mybucket=firebase.storage().bucket("ifp007.appspot.com");



const fs=require('fs');
let {PythonShell} = require('python-shell');

db.collection("switch").doc("status").onSnapshot((doc)=>{
    console.log(doc.data());
    if(doc.data().state){
        crawl();
        db.collection("switch").doc("status").set({
            state:false
        })
    }
         
})


async function crawl(){
    console.log("entered");


   
let url="http://mipcm.com/"

let browser=await puputeer.launch({headless: false, args:['--no-sandbox']});
var page = await browser.newPage();
page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3738.0 Safari/537.36');
        await page.setViewport({
            width: 1366,
            height: 768
        });
        await page.goto(url); //goes to men or women link of the site shopmango
        await page.waitFor("iframe");
        console.log("iframeloaded")

        var el = await page.$('iframe');
        const frame = await el.contentFrame();
        console.log(frame);
        await frame.waitFor("#signin_name");
    await frame.$eval("#signin_name", el => el.value = 'kevinthelly');
    await frame.$eval("#signin_pw", el => el.value = '123kevin');
    await frame.click('#sign_in');
    await page.waitFor("iframe");
    console.log("iframeloaded")

    var el1 = await page.$('iframe');
    const frame1 = await el1.contentFrame();
    await frame1.waitFor(".device_list_img div img")
    console.log("wkhawfh")
    frame1.click(".device_list_img div img");
    console.log("clicked");
    await frame1.waitFor("#play_view_box");
    frame1.click("div#play_view_box");
    let ok=await frame1.$eval('#play_screen',x=>x.style.background);
    let downloadurl=ok.split("(")[1].split(")")[0];
    let ll= await browser.newPage();
    let viewsource=await ll.goto(downloadurl.replace(/\"/g,""));
    fs.writeFile("../images/live.jpg", await viewsource.buffer(), function (err) {
        if (err) {
            return console.log(err);
        }
    
        console.log("The file was saved!");
        
    });
    PythonShell.run('../app.py', null, async function (err) {
        if (err) throw err;
        console.log('finished');
            fs.readdir('../output/',async function(err,d){
                
                let image=d.filter(x=>~x.indexOf(".jpg"))[0];
                let response=await mybucket.upload("../output/"+image);
                console.log(response);
                let link="https://storage.googleapis.com/ifp007.appspot.com/"+image;
                console.log(link);
                fs.unlinkSync("../output/"+image);
               

            
            })
                  
      });
    browser.close();
}





