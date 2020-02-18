function percentage() {

    var score1 = document.getElementById('crit1').value;
    var percent1 = document.getElementById('per1').innerText;
    var integer = parseInt(percent1) / 100;
    var totala1 = score1*integer;
    var totala2 = totala1.toFixed(2);

    if (totala1 < 0) {
        document.getElementById('pg1').innerText = 0;
    }
    else {
        document.getElementById('pg1').innerText = totala2
    }



    var score2 = document.getElementById('crit2').value;
    var percent2 = document.getElementById('per2').innerText;
    var integer = parseInt(percent2) / 100;
    var totalb1 = score2*integer;
    var totalb2 = totalb1.toFixed(2);

    if (totalb1 < 0) {
        document.getElementById('pg2').innerText = 0;
    }
    else {
        document.getElementById('pg2').innerText = totalb2
    }


    var score3 = document.getElementById('crit3').value;
    var percent3 = document.getElementById('per3').innerText;
    var integer = parseInt(percent3) / 100;
    var totalc1 = score3*integer;
    var totalc2 = totalc1.toFixed(2);

    if (totalc1 < 0) {
        document.getElementById('pg3').innerText = 0;
    }
    else {
        document.getElementById('pg3').innerText = totalc2
    }


    var alltotal = parseFloat(totala2) + parseFloat(totalb2) + parseFloat(totalc2)
    var final = alltotal.toFixed(2)

    document.getElementById('total').innerText = final

    setTimeout(percentage, 1000);
    }

percentage()v
