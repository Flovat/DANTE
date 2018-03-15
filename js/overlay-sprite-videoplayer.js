
/*!
 * Overlay the image on the player.
 */
var arrayEmoji = new Array(17);
//Creo gli array con tutte le Emoji (Arousal,Valence)
function loadEmoji(type) {
    for (var i = 0; i < 17; i++){
        arrayEmoji[i] = "../sprite/Emoji/"+type+"/" + (i+1) + ".png";
    }
    var img = document.createElement("img");
    img.src = arrayEmoji[8];
    var overlay = document.getElementById("overlay");
    overlay.appendChild(img);
    overlay.style.visibility = "hidden";
    overlay.style.opacity = "0.5";
}

function showOverlay() {
    var overlay = document.getElementById("overlay");
    overlay.style.visibility = "visible";
    var video = document.getElementById("annoVideo");  
    document.getElementById("overlay").style.left ="0px";
    document.getElementById("overlay").style.top = "0px";
}

function hiddenOverlay() {
    var overlay = document.getElementById("overlay");
   //overlay.removeChild(overlay.childNodes[1]);
    overlay.style.visibility = "hidden";
    var video = document.getElementById("annoVideo");
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
        if (document.getElementById("annoVideo").paused) {
            clearInterval(animation);
        }
        var currentJsonByFrame = getFrameInJson(jsonArrayJS, video.get());
        //document.getElementById("overlay").innerHTML = video.get();

        var x = parseFloat(currentJsonByFrame[0].x0);
        var y = parseFloat(currentJsonByFrame[0].y0);

        document.getElementById("overlay").style.left = x + "px";
        document.getElementById("overlay").style.top = y + "px";
        //document.getElementById("overlay").style.transition = "all 0.1s";  
        }, 5);
}

function updateEmoji(val,jsonArray) {
    
   // var jsonArrayJS = JSON.parse(jsonArray);
    var overlay = document.getElementById("overlay");
   
    //Inizializzo l'oggetto di tipo video (VideoFrame) per poter ottenere il frame corrente del video.
   /* var video = VideoFrame({
        id: 'annoVideo',
        frameRate: FrameRates.film,
        callback: function (response) {
            console.log('callback response: ' + response);
        }
    });*/

   // var currentJsonByFrame = getFrameInJson(jsonArrayJS, video.get());

    //overlay.innerHTML = currentJsonByFrame[0].x1;
    
    var rest = parseInt(val / 0.125);
    //Scorrere il video frame per frame, posizionando l'emoji alla giusta distanza dalla testa.
    var img = document.createElement("img");
    img.src = arrayEmoji[8 + rest];
    overlay.childNodes[0].src = img.src;


    /*var x = (Math.random() * 30) + parseFloat(currentJsonByFrame[0].x1);
    var y = (Math.random() * 30) + parseFloat(currentJsonByFrame[0].y0);

    document.getElementById("overlay").style.left = x + "px";
    document.getElementById("overlay").style.top = y + "px";
    document.getElementById("overlay").style.transition = "all 0.5s";
    */
    
}

function getFrameInJson(obj,frame) {
    return obj.filter(
        function (obj) { return obj.frame == frame }
    );
}
