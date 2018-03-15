
/*!
 * Overlay the image on the player.
 */
var arrayEmoji = new Array(17);
var img = document.getElementById("emoji");
var overlay = document.getElementById("overlay");
var videoID = document.getElementById("annoVideo");  
var player = document.getElementById("playercontent");

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
