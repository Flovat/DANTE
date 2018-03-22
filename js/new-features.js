/*!
 * New contents: caricamento delle sprite, overlay delle sprite nel video player, gestione dei pulsanti per la scelta del tipo di annotazione,
 *               gestione del feedback registrazione.
 */
var arrayEmoji = new Array(17);
var arraySam = new Array(5);
//Controllo se sovrapporre Emoji o SimpleSAM
var scaleEmotions = {
    SAM: 1,
    EMOJI: 2,
};
var typeOverlay = scaleEmotions.SAM;
var annotation = {
    YOU: 1,
    EXPERT: 2,
};
var typeAnnotation = annotation.YOU;
var currentSliderValue = 0.0;
var img = document.getElementById("overlay-img");
var overlayContent = document.getElementById("overlay");
overlayContent.style.left = "0px";
overlayContent.style.top = "0px";
var rec = document.getElementById("rec");
var videoID = document.getElementById("annoVideo");
var player = document.getElementById("playercontent");
var contentButtons = document.getElementById("type-annotation");
var buttonSimpleSam = document.getElementById("buttonsimplesam");
var buttonEmojiSam = document.getElementById("buttonemojisam");
var buttonyouannotation = document.getElementById("buttonyouannotation");
var buttonexpertannotation = document.getElementById("buttonexpertannotation");
var slidercontent = document.getElementById("slider-content");
var currentType;
var isExpert = false;

//Inizializzo il focus sui bottoni.
buttonyouannotation.style.backgroundColor = "#ccc";
buttonSimpleSam.style.backgroundColor = "#ccc";
//rec.style.visibility = hidden;
rec.src = "../img/norec.png";
rec.style.height = "25px";
rec.style.float = "right";


//Creo gli array con tutte le Emoji (Arousal,Valence)
function loadEmoji(type) {
    currentType = type;
   
        for (var i = 0; i < 17; i++) {
            arrayEmoji[i] = "../sprite/Emoji/" + type + "/" + (i + 1) + ".png";
        }
        for (var i = 0; i < 5; i++) {
            arraySam[i] = "../sprite/Sam/" + type + "/" + (i + 1) + ".png";
        }
        if (typeOverlay == 1) {
            img.src = arraySam[3];
        } else {
            img.src = arrayEmoji[8];
        }
        overlayContent.appendChild(img);
        overlayContent.style.visibility = "hidden";
        overlayContent.style.opacity = "0.5";
}

function showOverlay(type) {
    overlayContent.style.visibility = type;
}



//Gestisco il movimento della sprite leggendo le posizioni dal json.
function moveEmoji(jsonArrayPosition, jsonArrayExpert) {
    var jsonArrayUS = JSON.parse(jsonArrayPosition);
    if (isExpert)
        var jsonArrayEX = JSON.parse(jsonArrayExpert);

    if (typeAnnotation == 2) {
            showOverlay("visible");
        }
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

                var currentJsonByFrame = getFrameInJson(jsonArrayUS, video.get());

                var widthPlayer = document.getElementById("playercontent").offsetWidth;
                //overlay.innerHTML = widthPlayer;
                var x = parseFloat(currentJsonByFrame[0].x0);
                var y = parseFloat(currentJsonByFrame[0].y0);
                //x = x - 100;
                overlayContent.style.left = x + "px";
                overlayContent.style.top = y + "px";
                //document.getElementById("overlay").style.transition = "all 0.1s";  

                //Annotation Expert.
                //Se l'utente ha scelto di farsi trainare dall'annotazione dell'esperto.
                if (typeAnnotation == 2) {
                    if (isExpert) {
                        var currentExpertJsonByFrame = getFrameInJson(jsonArrayEX, video.get());
                        updateEmoji(parseFloat(currentExpertJsonByFrame[0].value));
                    }
                }

                if (videoID.paused) {
                    clearInterval(animation);
                }

            }, 5);
}

//Cambio di sprite in basa all'annotazione dell'utente.
function updateEmoji(value) {
    var rest;
    //Controllo se sono io a dover fare l'annotazione oppure se sono trainato dall'esperto.
    //Mi salvo l'ultimo valore dello slider.
    currentSliderValue = value;
    if (typeOverlay == 1) {
        rest = parseInt(value / 0.4);
        img.src = arraySam[2 + rest];
    } else {
        rest = parseInt(value / 0.125);
        img.src = arrayEmoji[8 + rest];
    }
    overlayContent.childNodes[0].src = img.src;
}

//Costruisco un oggetto con le informaizoni sul frame corrente dal json.
function getFrameInJson(obj, frame) {
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
        typeOverlay = scaleEmotions.SAM;
        buttonSimpleSam.style.backgroundColor = "#ccc";
        buttonEmojiSam.style.backgroundColor = "white";
}
function emojiSam(type) {
        var imagesaming = document.getElementById("imagesaming");
        imagesaming.src = "../img/sam" + type + ".png";
        typeOverlay = scaleEmotions.EMOJI;
        buttonSimpleSam.style.backgroundColor = "white";
        buttonEmojiSam.style.backgroundColor = "#ccc";
}

function youAnnotation() {
    typeAnnotation = annotation.YOU;
    slidercontent.style.visibility = "visible";
    buttonexpertannotation.style.backgroundColor = "white";
    buttonyouannotation.style.backgroundColor = "#ccc";
}

function expertAnnotation() {
    if (isExpert) {
        typeAnnotation = annotation.EXPERT;
        slidercontent.style.visibility = "hidden";
        buttonyouannotation.style.backgroundColor = "white";
        buttonexpertannotation.style.backgroundColor = "#ccc";
    }
}


//Controllo se esiste l'annotazione dell'esperto.
function isThereExpertAnnotation(ex) {
    isExpert = ex;
}
function needWriteAnnotation() {
    return (typeAnnotation == 1) ? true : false;
}

//Hide e show dei bottoni.
function showButtons(isVisible) {
    contentButtons.style.visibility = isVisible;
}


