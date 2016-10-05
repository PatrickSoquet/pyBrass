


    // Bouton qui permet d'afficher la console


    var emergencystop = document.getElementById("emergencystop");
    var alarm = document.getElementById("alarmpic");
    var alarmstop = false;












    emergencystop.addEventListener("click", function(){
        window.alert("EMERGENCY STOP!!!!! (todo... pour l'instant ne fait rien du tout!!!!)");
    }, false);


    alarm.addEventListener("click", function(){
        alarmstop=true;
    }, false);


    var stateData = [4098, 2420113410, 615027274, 21589, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,"",[],"",""];


    function WebSocketGetState(msg) {
        //var ws = new WebSocket("ws://63342/patou-brass/");
        var ws = new WebSocket("ws://localhost:8888/websocket");
		//var ws = new WebSocket("ws://192.168.7.2:8888/websocket");
        //from html to python ws server
        ws.onopen = function () {
            // Web Socket is connected, send data using send()
            console.log(msg);
            console.log(JSON.stringify(msg));
            ws.send(JSON.stringify(msg));
            //alert("ok");
        };
        //from pyhton ws server to html
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            console.log(evt.data);
            stateData = JSON.parse(evt.data);

        };
        ws.onclose = function () {
            // websocket is closed.
        };

    }

    var img_array = [];
    window.onload = function precharge_image() {
        for (var ii = 1; ii < 10; ii++) {
            img_array[ii] = new Image();
            img_array[ii].className = "brewpic";
            img_array[ii].id = ii;
            img_array[ii].src = "elt/00" + ii.toString() + ".png"
        }
        for (var ii = 10; ii < 100; ii++) {
            img_array[ii] = new Image();
            img_array[ii].className = "brewpic";
            img_array[ii].id = ii;
            img_array[ii].src = "elt/0" + ii.toString() + ".png";
        }
        for (var ii = 100; ii < 112; ii++) {
            img_array[ii] = new Image();
            img_array[ii].className = "brewpic";
            img_array[ii].id = ii;
            img_array[ii].src = "elt/" + ii.toString() + ".png";
        }

        for (var ii = 1; ii < 112; ii++) {
            document.getElementById("img_place").appendChild(img_array[ii]);
        }
    };

    function updateIHM(){



        var elt_tempgauge_cuveau = document.getElementById("tempgauge_cuveau");
        if(elt_tempgauge_cuveau != null){
            document.getElementById("gt1").innerHTML = stateData[4] + "&#x2103";
            elt_tempgauge_cuveau.value = stateData[4];
            setgaugevalue(elt_tempgauge_cuveau);
        }
        var elt_tempgauge_cuvebrass = document.getElementById("tempgauge_cuvebrass");
        if(elt_tempgauge_cuvebrass != null){
            document.getElementById("gt2").innerHTML = stateData[5] + "&#x2103";
            elt_tempgauge_cuvebrass.value = stateData[5];
            setgaugevalue(elt_tempgauge_cuvebrass);
        }
        var elt_tempgauge_rever = document.getElementById("tempgauge_rever");
        if(elt_tempgauge_rever != null){
            document.getElementById("gt3").innerHTML = stateData[6] + "&#x2103";
            elt_tempgauge_rever.value = stateData[6];
            setgaugevalue(elt_tempgauge_rever);
        }
        var elt_tempgauge_cuvebu = document.getElementById("tempgauge_cuvebu");
        if(elt_tempgauge_cuvebu != null){
            document.getElementById("gt4").innerHTML = stateData[7] + "&#x2103";
            elt_tempgauge_cuvebu.value = stateData[7];
            setgaugevalue(elt_tempgauge_cuvebu);
        }




        //ALARME GESTION
        if(stateData[19] == 1 && alarmstop == false){
            document.getElementById("alarmpic").style.display = 'block';
            document.getElementById("alarmtxt").style.display = 'block';
            document.getElementById("alarmtxt").innerHTML = stateData[20];

        }else{
            document.getElementById("alarmpic").style.display = 'none';
            document.getElementById("alarmtxt").style.display = 'none';
            if(stateData[19] == 0){
                alarmstop=false;
            }
        }

    }

    /*
     setInterval(function displayImg() {
     WebSocketGetState("");
     if (document.body != null) {
     for (var ii = 1; ii < 112; ii++) {
     if (stateData[ii] == 0) {
     img_array[ii].style.display = 'none';
     } else {
     img_array[ii].style.display = 'block';
     }
     }
     }
     }, 1000);
     */
    /*	stateData format:
     0..3: 112 bits pour l'affichage des 111 images
     4	: température	cuveau
     5	: température	cuve brass
     6	: température	reverdoir
     7	: température	cuvebu
     8	: SV			cuveau
     9	: SV			cuve brass (non utilisé)
     10	: SV			reverdoir
     11	: SV			cuvebu
     12	: volume		cuveau
     13	: volume		reverdoir
     14	: volume		cuvebu
     15	: volume		cuve brass
     16	: timer
     17	: nb cycle
     18	: chrono
     19 : alarm (bool)
     20 : alarm text
     21 : list of INPUT file available ("" after begin brass)
     22 : first line of text from INPUT FILE
     23 : second line of text from INPUT FILE
     */
    setInterval(function displayImg() {
        WebSocketGetState("");
        if(document.body != null){
            for(var ii=1;ii<32;ii++){
                if((stateData[0]&(1<<ii)) == 0){
                    img_array[ii].style.display = 'none';
                }else {
                    img_array[ii].style.display = 'block';
                }
            }
            for(var ii=0;ii<32;ii++){
                if((stateData[1]&(1<<ii)) == 0){
                    img_array[32+ii].style.display = 'none';
                }else {
                    img_array[32+ii].style.display = 'block';
                }
            }
            for(var ii=0;ii<32;ii++){
                if((stateData[2]&(1<<ii)) == 0){
					img_array[64+ii].style.display = 'none';
                }else {
                    img_array[64+ii].style.display = 'block';
                }
            }
            for(var ii=0;ii<16;ii++){
                if((stateData[3]&(1<<ii)) == 0){
                    img_array[96+ii].style.display = 'none';
                }else {
                    img_array[96+ii].style.display = 'block';
                }
            }
            updateIHM();

        }}, 1000);


    function setgaugevalue(gauge){
        //vert pour 0-50° / jaune 50-75° / rouge 75-100°
        if(gauge.value<75){
            gauge.low = 0;
        }else {
            gauge.low = 1;
        }
    }

    updateIHM() ;
