$(document).ready(function () {
    $("#welcome_text").animate({
        left: '35%'
    }, "slow");
    $("#welcome_text").fadeOut();
    $("#welcome_text").fadeIn();
})

function score1() {
    var x1 = document.getElementById("firstQbar").value;
    document.getElementById("firstScore").innerText = "分數："+x1;
}

function score2() {
    var x2 = document.getElementById("secondQbar").value;
    console.log(x2);
    document.getElementById("secondScore").innerText = "分數："+x2;
}

function talk() {
    var x3 = document.getElementById("thirdText").value;
    console.log(x3);
    document.getElementById("thirdText").value =x3;
}