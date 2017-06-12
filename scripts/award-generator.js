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
