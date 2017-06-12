function enterTankName() {
    var tankName = $('.award-generator-text').val();
    $('.tank-name').text(tankName);  
}

function colorOrange() {
    $('.tank-name')
        .addClass('orange')
        .removeClass('red blue purple');
}

function colorBlue() {
    $('.tank-name')
        .addClass('blue')
        .removeClass('red orange purple');
}

function colorPurple() {
    $('.tank-name')
        .addClass('purple')
        .removeClass('red blue orange');
}

function colorRed() {
    $('.tank-name')
        .addClass('red')
        .removeClass('orange blue purple');
}

function noStar() {
    $('#award-generator-0')
        .removeClass('a0-1 a0-2 a0-3');
}

function singleStar() {
    $('#award-generator-0')
        .addClass('a0-1')
        .removeClass('a0-2 a0-3');
}

function doubleStar() {
    $('#award-generator-0')
        .addClass('a0-2')
        .removeClass('a0-1 a0-3');
}

function tripleStar() {
    $('#award-generator-0')
        .addClass('a0-3')
        .removeClass('a0-1 a0-2');
}

function noTank() {
    $('#award-generator-1')
        .removeClass('a1-1 a1-2 a1-3');
}

function bronzeTank() {
    $('#award-generator-1')
        .addClass('a1-1')
        .removeClass('a1-2 a1-3');
}

function silverTank() {
    $('#award-generator-1')
        .addClass('a1-2')
        .removeClass('a1-1 a1-3');
}

function goldTank() {
    $('#award-generator-1')
        .addClass('a1-3')
        .removeClass('a1-1 a1-2');
}

function noMedal() {
    $('#award-generator-2')
        .removeClass('a2-1 a2-2 a2-3');
}

function combatMedal() {
    $('#award-generator-2')
        .addClass('a2-1')
        .removeClass('a2-2 a2-3');
}

function battleMedal() {
    $('#award-generator-2')
        .addClass('a2-2')
        .removeClass('a2-1 a2-3');
}

function heroicMedal() {
    $('#award-generator-2')
        .addClass('a2-3')
        .removeClass('a2-1 a2-2');
}

function noSword() {
    $('#award-generator-3')
        .removeClass('a3-1 a3-2 a3-3');
}

function shiningSword() {
    $('#award-generator-3')
        .addClass('a3-1')
        .removeClass('a3-2 a3-3');
}

function batteredSword() {
    $('#award-generator-3')
        .addClass('a3-2')
        .removeClass('a3-1 a3-3');
}

function rustySword() {
    $('#award-generator-3')
        .addClass('a3-3')
        .removeClass('a3-1 a3-2');
}

function noDoT() {
    $('#award-generator-4')
        .removeClass('a4-3');
}

function defenderOfTruth() {
    $('#award-generator-4')
        .addClass('a4-3');
}

function noCup() {
    $('#award-generator-5')
        .removeClass('a5-1 a5-2 a5-3');
}

function bronzeCup() {
    $('#award-generator-5')
        .addClass('a5-1')
        .removeClass('a5-2 a5-3');
}

function silverCup() {
    $('#award-generator-5')
        .addClass('a5-2')
        .removeClass('a5-1 a5-3');
}

function goldCup() {
    $('#award-generator-5')
        .addClass('a5-3')
        .removeClass('a5-1 a5-2');
}

function noPH() {
    $('#award-generator-6')
        .removeClass('a6-1');
}

function purpleHeart() {
    $('#award-generator-6')
        .addClass('a6-1');
}

function noWC() {
    $('#award-generator-7')
        .removeClass('a7-1');
}

function warCorrespondent() {
    $('#award-generator-7')
        .addClass('a7-1');
}

function noLB() {
    $('#award-generator-8')
        .removeClass('a8-1');
}

function lightBulb() {
    $('#award-generator-8')
        .addClass('a8-1');
}
