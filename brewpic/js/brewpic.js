


    // Bouton qui permet d'afficher la console
    var consoleButton  = document.getElementById("console-button");
    var consoleContainer = document.getElementById("console-container");

    var mixerButton = document.getElementById("mixer-button");
    var pumprevButton = document.getElementById("pumprev-button");
    var pumpeauButton = document.getElementById("pumpeau-button");

    var consolebut = document.getElementById("console-button");
    var consoleVar = false

    var pausebut = document.getElementById("pause-button")
    var pauseVar = false

    var emergencystop = document.getElementById("emergencystop");
    var alarm = document.getElementById("alarmpic");
    var alarmstop = false;

    mixerButton.addEventListener("click", function(){
        if(mixerButton.innerHTML == "Mixer ON"){
            WebSocketGetState({'MIXER':true});
            mixerButton.innerHTML = "Mixer OFF";
            mixerButton.classList.remove("mybtn1");
            mixerButton.classList.add("mybtn2");
        }
        else{
            WebSocketGetState({'MIXER':false});
            mixerButton.innerHTML = "Mixer ON";
            mixerButton.classList.remove("mybtn2");
            mixerButton.classList.add("mybtn1");
        }
    }, false);

    pumprevButton.addEventListener("click", function(){
        if(pumprevButton.innerHTML == "Pump reverdoir ON"){
            WebSocketGetState({'REVERDOIR':true});
            pumprevButton.innerHTML = "Pump reverdoir OFF";
            pumprevButton.classList.remove("mybtn1");
            pumprevButton.classList.add("mybtn2");
        }
        else{
            WebSocketGetState({'REVERDOIR':false});
            pumprevButton.innerHTML = "Pump reverdoir ON";
            pumprevButton.classList.remove("mybtn2");
            pumprevButton.classList.add("mybtn1");
        }
    }, false);

    pumpeauButton.addEventListener("click", function(){
        if(pumpeauButton.innerHTML == "Pump cuveau ON"){
            WebSocketGetState({'PUMPRECIRCULEAU':true});
            pumpeauButton.innerHTML = "Pump cuveau OFF";
            pumpeauButton.classList.remove("mybtn1");
            pumpeauButton.classList.add("mybtn2");
        }
        else{
            WebSocketGetState({'PUMPRECIRCULEAU':false});
            pumpeauButton.innerHTML = "Pump cuveau ON";
            pumpeauButton.classList.remove("mybtn2");
            pumpeauButton.classList.add("mybtn1");
        }
    }, false);


    consolebut.addEventListener("click", function(){
        if(consoleVar){
            consoleVar = false
            consolebut.classList.remove("mybtn2");
            consolebut.classList.add("mybtn1");
        }
        else{
            consoleVar = true
            consolebut.classList.remove("mybtn1");
            consolebut.classList.add("mybtn2");
        }
    }, false);


    pausebut.addEventListener("click", function(){
        if(pauseVar){
            WebSocketGetState({'PAUSE':false});
            pauseVar = false
            pausebut.classList.remove("mybtn2");
            pausebut.classList.add("mybtn1");
        }
        else{
            WebSocketGetState({'PAUSE':true});
            pauseVar = true
            pausebut.classList.remove("mybtn1");
            pausebut.classList.add("mybtn2");
        }
    }, false);


    consoleButton.addEventListener("click", function(){
        consoleContainer.classList.toggle("show");
    }, false);

    emergencystop.addEventListener("click", function(){
        window.alert("EMERGENCY STOP!!!!! (todo... pour l'instant ne fait rien du tout!!!!)");
    }, false);

    
	function stop(){
		if(window.confirm("Are you sure you want to quit?")){
			WebSocketGetState({'QUIT':true});
		}
	}
	
    alarm.addEventListener("click", function(){
        alarmstop=true;
    }, false);

    function WebSocketTest() {
        if ("WebSocket" in window) {
            alert("WebSocket is supported by your Browser!");
            // Let us open a web socket
            //var ws = new WebSocket("ws://localhost:8888/websocket");
            var ws = new WebSocket("ws://192.168.7.2:8888/websocket");
            ws.onopen = function () {
                // Web Socket is connected, send data using send()
                ws.send("Message to send");
                alert("Message is sent...");
            };
            ws.onmessage = function (evt) {
                var received_msg = evt.data;
                alert("Message is received...\n" + evt.data.toString());
            };
            ws.onclose = function () {
                // websocket is closed.
                alert("Connection is closed...");
            };
        }
        else {
            // The browser doesn't support WebSocket
            alert("WebSocket NOT supported by your Browser!");
        }
    }


    /*
     var stateData = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
     0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1,
     0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0,
     1, 0, 0, 0, 1, 1, 0, 0, 1];*/
    //
    var stateData = [4098, 2420113410, 615027274, 21589, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,"",[],"",""];
    //var stateData = [4098, 2420113410, 615027273, 21673, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,"",[],"",""]

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
        var date = new Date(stateData[16]*1000);
        // Hours part from the timestamp
        var hours = date.getHours();
        // Minutes part from the timestamp
        var minutes = "0" + date.getMinutes();
        // Seconds part from the timestamp
        var seconds = "0" + date.getSeconds();
        var elt_hour = document.getElementById("hour");
        if(elt_hour != null){
            elt_hour.innerHTML = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
        }

        var elt_timer = document.getElementById("timer");
        date = new Date(stateData[17]*1000);
        hours = date.getHours() - 1;
        minutes = "0" + date.getMinutes();
        seconds = "0" + date.getSeconds();
        if(elt_timer != null){
            elt_timer.innerHTML = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
        }

        var elt_cycle = document.getElementById("cycle");
        if(elt_cycle != null){
            elt_cycle.innerHTML = stateData[18];
        }
        var elt_temp_cuveau = document.getElementById("temp_cuveau");
        if(elt_temp_cuveau != null){
            //elt_temp_cuveau.innerHTML  = "Cuve eau &nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + stateData[4] + "&#x2103";
            elt_temp_cuveau.innerHTML  =  stateData[4] + "&#x2103";
        }
        var elt_temp_cuvebrass = document.getElementById("temp_cuvebrass");
        if(elt_temp_cuvebrass != null){
            //elt_temp_cuvebrass.innerHTML = "Cuve brassage &nbsp; " + stateData[5] + "&#x2103";
            elt_temp_cuvebrass.innerHTML = stateData[5] + "&#x2103";
        }
        var elt_temp_rever = document.getElementById("temp_rever");
        if(elt_temp_rever != null){
            //elt_temp_rever.innerHTML = "Cuve reverdoir &nbsp;&nbsp;" +stateData[6] + "&#x2103";
            elt_temp_rever.innerHTML = stateData[6] + "&#x2103";
        }
        var elt_temp_cuvebu = document.getElementById("temp_cuvebu");
        if(elt_temp_cuvebu != null){
            //elt_temp_cuvebu.innerHTML ="Cuve ebu &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      " +stateData[7] + "&#x2103";
            elt_temp_cuvebu.innerHTML =stateData[7] + "&#x2103";
        }
        var elt_vol_cuveau = document.getElementById("vol_cuveau");
        if(elt_vol_cuveau != null){
            //elt_vol_cuveau.innerHTML ="Cuve eau &nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + stateData[12] + "l";
            elt_vol_cuveau.innerHTML = stateData[12] + "l";
        }
        var elt_vol_cuvebrass = document.getElementById("vol_cuvebrass");
        if(elt_vol_cuvebrass != null){
            //elt_vol_cuvebrass.innerHTML = "Cuve brassage &nbsp;" +stateData[15] + "l";
            elt_vol_cuvebrass.innerHTML = stateData[15] + "l";

        }
        var elt_vol_rever = document.getElementById("vol_rever");
        if(elt_vol_rever != null){
            //elt_vol_rever.innerHTML ="Cuve reverdoir &nbsp;&nbsp;" + stateData[13] + "l";
            elt_vol_rever.innerHTML = stateData[13] + "l";
        }
        var elt_vol_cuvebu = document.getElementById("vol_cuvebu");
        if(elt_vol_cuvebu != null){
            //elt_vol_cuvebu.innerHTML ="Cuve ebu &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + stateData[14]+ "l";
            elt_vol_cuvebu.innerHTML = stateData[14]+ "l";
        }


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
        var ttt = document.getElementById("test");
        if(ttt != null){
            ttt.innerHTML = stateData[5] + "&#x2103";
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
        //INPUT FILE GESTION
        if(stateData[21] != []){
            var fI = document.getElementById("fileI");
            for(var ii=fI.length;ii<stateData[21].length;ii++){
                var option = document.createElement("option");
                option.text = stateData[21][ii];
                fI.add(option);
            }
        }
        if(stateData[22] != ""){
            document.getElementById('file-content1').innerHTML = stateData[22];
        }
        if(stateData[23] != ""){
            document.getElementById('file-content2').innerHTML = stateData[23];
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

    function readSingleFile(e) {
        var fI =  document.getElementById("fileI");
		if(fI.selectedIndex >= 0){
			WebSocketGetState({'SELECT_INPUT_FILE':fI.options[fI.selectedIndex].text});
		}
/*        var file = e.target.files[0];
        if (!file) {
            return;
        }
        var reader = new FileReader();
        reader.onload = function(e) {
            var contents = e.target.result;
            displayContents(contents.substring(0,contents.indexOf('\n')));
        };
        reader.readAsText(file);
        WebSocketGetState({'SELECT_INPUT_FILE':document.getElementById("fileI").value});*/
    }
/*
    function displayContents(contents) {
        var element = document.getElementById('file-content');
        element.innerHTML = contents;
    }
*/


    function click_adjtemp_cuveau(){
        WebSocketGetState({'CUVEAU_HEAT': Number(document.getElementById('adjtemp_cuveau').value)});
    }


    function beginbrass(){
        var fI = document.getElementById("fileI");
        if(fI.selectedIndex < 0) {
            window.alert("Choose a valid input file first!\n (if no file available please add an input file in the /recettes directory!)");
        }else{
			WebSocketGetState({'SELECT_INPUT_FILE':fI.options[fI.selectedIndex].text});
		    if(stateData[22] != ""){
				document.getElementById('file-content1').innerHTML = stateData[22];
			}
			if(stateData[23] != ""){
				document.getElementById('file-content2').innerHTML = stateData[23];
			}
			//var ii;
			//while(ii=0;ii<10000;ii++){}
            WebSocketGetState({'PAUSE': false});
            fI.disabled=true;
        }
    }
    function RAZ(){
        WebSocketGetState({'RESTART':true});
        document.getElementById("fileI").disabled=false;
    }

    document.getElementById('fileI')
        .addEventListener('change', readSingleFile, false);
    document.getElementById('fileI')
        .addEventListener('click', readSingleFile, false);


    updateIHM() ;

    var dd = new Date()
    document.getElementById("titredate").innerHTML = "Brassage du " + dd.getDay() +"/"+dd.getMonth()+"/"+dd.getFullYear();