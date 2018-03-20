
/*!
 * New contents: caricamento delle sprite, overlay delle sprite nel video player, gestione dei pulsanti per la scelta del tipo di annotazione,
 *               gestione del feedback registrazione.
 */
var arrayEmoji = new Array(17);
var arraySam = new Array(5);
//Controllo se sovrapporre Emoji o SimpleSAM
var typeOverlay = "SAM";
var currentSliderValue = 0.0;
var img = document.getElementById("overlay-img");
var overlay = document.getElementById("overlay");
overlay.style.left = "0px";
overlay.style.top = "0px";
var rec = document.getElementById("rec");
var videoID = document.getElementById("annoVideo");  
var player = document.getElementById("playercontent");
var contentButtons = document.getElementById("type-annotation");
var buttonSimpleSam = document.getElementById("buttonsimplesam");
var buttonEmojiSam = document.getElementById("buttonemojisam");

var currentType;

buttonSimpleSam.style.backgroundColor  = "#ccc";
//rec.style.visibility = hidden;
rec.src = "../img/norec.png";
rec.style.height = "25px";
rec.style.float = "right";

//Nascondo lo slider se sto mostrando il video d'esempio.
function hideLayout(type) {
    
    if (type == "example") {
        document.getElementById("slider").style.visibility = "hidden";
        showButtons("hidden");
    } else {
        document.getElementById("slider").style.visibility = "visible";
    }
    overlay.style.visibility = "visible";
    //overlay.innerHTML = "PORCO DIO";
}

//Creo gli array con tutte le Emoji (Arousal,Valence)
function loadEmoji(type) {
    currentType = type;
    hideLayout(type);
    if(type != "example"){
        for (var i = 0; i < 17; i++){
            arrayEmoji[i] = "../sprite/Emoji/"+type+"/" + (i + 1) + ".png";
        }
        for (var i = 0; i < 5; i++) {
            arraySam[i] = "../sprite/Sam/" + type + "/" + (i + 1) + ".png";
        }
        if (typeOverlay == "SAM") {
            img.src = arraySam[3];
        } else {
            img.src = arrayEmoji[2];
        }
        overlay.appendChild(img);
        overlay.style.visibility = "hidden";
        overlay.style.opacity = "0.5";
    }
}

function showOverlay() {
    overlay.style.visibility = "visible";
}

function hiddenOverlay() {
    overlay.style.visibility = "hidden";
}


//Gestisco il movimento della sprite leggendo le posizioni dal json.
function moveEmoji(jsonArray) {
    if (currentType != "example"){
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
}

//Cambio di sprite in basa all'annotazione dell'utente.
function updateEmoji(val) {
    if (currentType != "example") {
        var rest;
        //Mi salvo l'ultimo valore dello slider.
        currentSliderValue = val;
        if (typeOverlay == "SAM") {
            rest = parseInt(val / 0.4);
            img.src = arraySam[2 + rest];
        } else {
            rest = parseInt(val / 0.125);
            img.src = arrayEmoji[8 + rest];
        }
        overlay.childNodes[0].src = img.src;
    }
}

//Costruisco un oggetto con le informaizoni sul frame corrente dal json.
function getFrameInJson(obj,frame) {
    return obj.filter(
        function (obj) { return obj.frame == frame }
    );
}

//Rec image
function showRec(isVisible) {
    if (isVisible == "visible")
        rec.src = "../img/yesrec.png";
    else
        rec.src = "../img/norec.png";

    //img.style.height = "125px";
    //rec.style.visibility = isVisible;
    if (isVisible) updateEmoji(currentSliderValue);
}

//Cambio imagesaming, in base al tipo di annotazione che l'utente vuole svolgere.
function simpleSam(type) {
    var imagesaming = document.getElementById("imagesaming");
    imagesaming.src = "../img/simplesam_" + type + ".png";
    typeOverlay = "SAM";
    buttonSimpleSam.style.backgroundColor = "#ccc";
    buttonEmojiSam.style.backgroundColor = "white";
}
function emojiSam(type) {
    var imagesaming = document.getElementById("imagesaming");
    imagesaming.src = "../img/sam" + type + ".png";
    typeOverlay = "EMOJI";
    buttonSimpleSam.style.backgroundColor = "white";
    buttonEmojiSam.style.backgroundColor = "#ccc";
}

//Hide e show dei bottoni.
function showButtons(isVisible) {
    contentButtons.style.visibility = isVisible; 
}

