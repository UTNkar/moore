function PartyMachine() {
    this.state = 0;
    this.keys = [38,38,40,40,37,39,37,39,66,65];
    that = this;
    document.onkeydown = function(e) {
        e = e || window.event;
        that.keypress(e.keyCode);
    }
}

PartyMachine.prototype = {
    keypress: function(key) {
        if (this.keys[this.state] == key) {
            this.state++;
        } else {
            this.state = 0;
        }
        if (this.state == this.keys.length) {
            this.state = 0;
            startTheParty();
        }
    }
};
new PartyMachine();

function startTheParty() {
    alert("Party mode engaged!");
    if (document.getElementById("volvo") === null) {
        var audio = document.createElement("audio");
        audio.setAttribute("id", "volvo");
        audio.setAttribute("loop","loop");
        audio.setAttribute("autoplay","autoplay");

        var mp3 = document.createElement("source");
        mp3.setAttribute("src", "/static/libraries/misc/volvo.mp3");
        mp3.setAttribute("type", "audio/mp3");
        audio.appendChild(mp3);
        document.body.appendChild(audio);
    }
    var iframe = document.createElement("iframe");
    iframe.src = "/static/libraries/misc/party.html";
    iframe.className = "party";
    document.body.appendChild(iframe);
    danceAround(iframe);
}

function transform(element, transformation) {
    element.style.WebkitTransform = transformation;
    element.style.MozTransform = transformation;
    element.style.msTransform = transformation;
}

function danceAround(party) {
    setInterval(function(){transform(party,"rotate(" + Math.round(Math.random()*30-15) + "deg)")},500);
    setInterval(function(){
        party.style.top = Math.round(Math.random()*(innerHeight-300)) + "px";
        party.style.left = Math.round(Math.random()*(innerWidth-300)) + "px";
    },5000);
}