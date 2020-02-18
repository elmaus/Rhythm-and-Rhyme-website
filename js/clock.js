
function clock() {

    var now = new Date();
    var dead = document.getElementById("dead").innerText
    var eventDate = new Date(dead);

    var utc = now.getTime() + (now.getTimezoneOffset() * 60000);

    var currentTime = now.getTime();
    var eventTime = eventDate.getTime();

    var remTime = eventTime - currentTime;

    var s = Math.floor(remTime / 1000);
    var m = Math.floor(s/60);
    var h = Math.floor(m/60);
    var d = Math.floor(h/24);

    h %= 24;
    m %= 60;
    s %= 60;

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    if (d < 0) {
        d = "0";
        h = "00";
        m = "00";
        s = "00";
        document.getElementById("entryname").disabled = true;
        document.getElementById("entrytitle").disabled = true;
        document.getElementById("entrylink").disabled = true;
        document.getElementById("entrybtn").disabled = true;
    }

    document.getElementById("days").innerText = d;
    document.getElementById("hours").innerText = h;
    document.getElementById("minutes").innerText = m;
    document.getElementById("seconds").innerText = s;

    setTimeout(clock, 1000);

}
clock()
