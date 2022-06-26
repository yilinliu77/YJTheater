let mySocket = null;
let myPlayer = null;
let nickname = null;
let countFunc = null;

//Stupid
let ignoreListenerOnce = false;

function getTimeString(vTime) {
    let h = vTime / 60 / 60;
    let m = Math.floor(vTime / 60 % 60);
    let s = vTime % 60;
    return `${h.toFixed(0)}:${m.toFixed(0)}:${s.toFixed(0)}`;
}


function switch_source(source_name, source_address) {
    myPlayer.source = {
        type: 'video',
        title: 'source_name',
        sources: [
            {
                src: source_address,
                type: 'video/mp4',
                // size: 720,
            }
        ],
        // tracks: [
        //     {
        //         kind: 'captions',
        //         label: 'English',
        //         srclang: 'en',
        //         src: '/path/to/captions.en.vtt',
        //         default: true,
        //     },
        //     {
        //         kind: 'captions',
        //         label: 'French',
        //         srclang: 'fr',
        //         src: '/path/to/captions.fr.vtt',
        //     },
        // ],
    };

}

function login() {
    nickname = prompt("A Nickname?");
    alert("Welcome " + nickname);

    mySocket = io.connect();
    // myPlayer = videojs('player');
    myPlayer = new Plyr('#player');

    /* 
    Player callback function
    */
    myPlayer.on('pause', function () {
        if (myPlayer.seeking)
            return;
        if (ignoreListenerOnce)
        {
            ignoreListenerOnce = false;
            return;
        }
        mySocket.emit("pause", { "nickname": nickname });
    });
    myPlayer.on('play', function () {
        if (myPlayer.seeking) 
            return;
        if (ignoreListenerOnce)
        {
            ignoreListenerOnce = false;
            return;
        }
        mySocket.emit("play", { "nickname": nickname });
    });
    myPlayer.on('seeked', function () {
        // mySocket.emit("play", { "nickname": nickname });
    });

    /*
    Socket callback function
    */
    mySocket.on('registerUsers', function (msg) {
        msg = JSON.parse(msg);
        msg = msg.filter(function (item) {
            let result = document.getElementById(item["nickname"]);
            return result == null;
        });
        let ol = document.getElementById("roomate");
        for (item in msg) {
            let li = document.createElement("li");
            li.appendChild(document.createTextNode(msg[item]["nickname"] + " : " + getTimeString(Number(msg[item]["time"]))));
            li.setAttribute("id", msg[item]["nickname"]);
            ol.appendChild(li);
        }

    });
    mySocket.on('timeReport', function (msg) {
        let li = document.getElementById(msg["nickname"]);
        if (li)
            li.innerText = msg["nickname"] + " : " + getTimeString(msg["time"]);
    });
    mySocket.on('synchronizeYourself', function (msg) {
        if (msg["nickname"] != nickname) {
            let cur = myPlayer.currentTime;
            delta = Number(msg["time"]) - cur;
            if (delta < 0)
                myPlayer.rewind(-delta);
            else
                myPlayer.forward(delta);
            showToast(`${msg["nickname"]} has synchronized the video`);
        }
    });
    mySocket.on('play', function (msg) {
        if (msg["nickname"] != nickname) {
            ignoreListenerOnce = true;
            myPlayer.play();
            showToast(`${msg["nickname"]} has played the video`);
        }
    });
    mySocket.on('pause', function (msg) {
        if (msg["nickname"] != nickname) {
            ignoreListenerOnce = true;
            myPlayer.pause();
            showToast(`${msg["nickname"]} has paused the video`);
        }
    });

    //显示投票结果
    mySocket.on("display_vote", function (msg) {
        var table_root = document.getElementById("vote_table");
        for (var i = 4; i < table_root.firstElementChild.childNodes.length; i += 2) {
            var row_node = table_root.firstElementChild.childNodes[i];
            var key = row_node.childNodes[3].innerText;
            row_node.childNodes[7].firstElementChild.innerText = msg[key]["count"];
        }
    });

    mySocket.emit("register", { "nickname": nickname });

    countFunc = self.setInterval(function () {
        mySocket.emit("timeReport", { "nickname": nickname, "time": myPlayer.currentTime });
    }, 1000);
}


/*
send to "synchronize"
params:
*/
function synchronize() {
    let whereYouAt = myPlayer.currentTime;

    mySocket.emit("synchronize", { "time": whereYouAt, "nickname": nickname });

}

function showToast(vText) {
    let x = document.getElementById("snackbar")
    x.className = "show";
    x.innerText = vText;
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}