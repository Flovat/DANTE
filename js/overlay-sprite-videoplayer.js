
/*!
 * Overlay the image on the player.
 */
var arrayEmoji = new Array(17);
var arraySam = new Array(5);
var img = document.getElementById("emoji");
var overlay = document.getElementById("overlay");
var rec = document.getElementById("rec");
var videoID = document.getElementById("annoVideo");  
var player = document.getElementById("playercontent");

var buttonSimpleSam = document.getElementById("buttonsimplesam");
var buttonEmojiSam = document.getElementById("buttonemojisam");

buttonSimpleSam.style.backgroundColor  = "#ccc";
rec.style.visibility = hidden;



//Creo gli array con tutte le Emoji (Arousal,Valence)
function loadEmoji(type) {
    for (var i = 0; i < 17; i++){
        arrayEmoji[i] = "../sprite/Emoji/"+type+"/" + (i+1) + ".png";
    }
    img.src = arrayEmoji[8];
    //img.style.height = "125px";
    overlay.appendChild(img);
    //overlay.style.height = "10px";
    overlay.style.visibility = "hidden";
    overlay.style.opacity = "0.5";
}

function showOverlay() {
    overlay.style.visibility = "visible";
    overlay.style.left ="0px";
    overlay.style.top = "0px";
}

function hiddenOverlay() {
    overlay.style.visibility = "hidden";
}



function moveEmoji(jsonArray) {
    var jsonArrayJS = JSON.parse(jsonArray);
    //Inizializzo l'oggetto di tipo video (VideoFrame) per poter ottenere il frame corrente del video.
    var video = VideoFrame({
        id: 'annoVideo',
        frameRate: FrameRates.film,
        callback: function (response) {
            console.log('callback response: ' + response);
        }
    });

    var animation = setInterval(
    function () {
        if (videoID.paused) {
            clearInterval(animation);
        }
        var currentJsonByFrame = getFrameInJson(jsonArrayJS, video.get());

        var widthPlayer = document.getElementById("playercontent").offsetWidth;
        //overlay.innerHTML = widthPlayer;
        var x = parseFloat(currentJsonByFrame[0].x0);
        var y = parseFloat(currentJsonByFrame[0].y0);
        //x = x - 100;
        overlay.style.left = x + "px";
        overlay.style.top = y + "px";
        //document.getElementById("overlay").style.transition = "all 0.1s";  
        }, 5);
}

function updateEmoji(val, jsonArray) {

    var rest = parseInt(val / 0.125);
    img.src = arrayEmoji[8 + rest];
    overlay.childNodes[0].src = img.src;
}

function scaleEmoji() {
    //Leggo l'altezza e la larghezza del player.
    var width = player.offsetWidth;
    var height = player.offsetHeight;


}

function getFrameInJson(obj,frame) {
    return obj.filter(
        function (obj) { return obj.frame == frame }
    );
}

function showRec(isVisible) {
    rec.src = "../img/rec.png";
    rec.style.height = "25px";
    rec.style.float = "right";
    //img.style.height = "125px";
    rec.style.visibility = isVisible;
}

function simpleSam(type) {
    var imagesaming = document.getElementById("imagesaming");
    imagesaming.src = "../img/simplesam_" + type + ".png";
    buttonSimpleSam.style.backgroundColor = "#ccc";
    buttonEmojiSam.style.backgroundColor = "white";
}
function emojiSam(type) {
    var imagesaming = document.getElementById("imagesaming");
    imagesaming.src = "../img/sam" + type + ".png";
    buttonSimpleSam.style.backgroundColor = "white";
    buttonEmojiSam.style.backgroundColor = "#ccc";
}


