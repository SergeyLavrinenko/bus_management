
var curTime = "";
var timePoint = ':';


function getHost() {
    return "http://" + host.substring(0, host.length - 1);
}

function GetData(){
    SendRequest("post",getHost() + "/ajax/getTime","",function (Request) {
        var jsonObj = eval("(" + Request.responseText + ")");
        curTime = jsonObj["time"].split(":");
    },
        function () {
            curTime = ["--","--"];
        });
}

function TimeBlink() {
    try{
        timePoint = timePoint == " " ? ":" : ' ';
        if (curTime != "") {
            document.getElementById('time-hours').innerHTML = curTime[0];
            document.getElementById('time-point').innerHTML = timePoint;
            document.getElementById('time-minuts').innerHTML = curTime[1];
        }

    }
    catch(e){

    }

}