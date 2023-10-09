let picks = []
const $calc = $('.calc');
const $winAmount = $('.winAmount');
let payOut = 0;

function printLogic(pick){
    if (pick.cat === "spread"){
        pick.parlayChoice1 = pick.choice;
        pick.PS > 0 ? pick.parlayChoice2 = `+${pick.PS}` : pick.parlayChoice2 = pick.PS;
        pick.parlayChoice3 = pick.price;
    }
    else if (pick.cat === "ml"){
        pick.parlayChoice1 = pick.choice;
        pick.parlayChoice2 = "ML";
        pick.ml_price > 0 ? pick.parlayChoice3 = `+${pick.ml_price}` : pick.parlayChoice3 = pick.ml_price;
    }
    else if (pick.cat === "total"){
        pick.parlayChoice1 = `${pick.choice} | ${pick.team1.substring(0,3)} @ ${pick.team2.substring(0,3)}`;
        pick.parlayChoice2 = pick.over_under;
        pick.parlayChoice3 = pick.over_under_price;
    }
}

function showPreview(picks) {
    console.log(picks);

    const $overlay = $('#overlay');
    $overlay.css('display', 'block');

    const $closeOverlayBtn = $('#closeOverlayBtn');
    $closeOverlayBtn.click(function () {
        $overlay.css('display', 'none');
    });

    let $eachPick = $('.eachPick');
    $eachPick.html(" ");

    picks.forEach(function (pick) {
        printLogic(pick)

        let nextPick = `
            <div class="row over">
                <div class="col-8 previewTeam">
                    ${pick.parlayChoice1}
                </div>
                <div class="col-2 previewTeam">
                    ${pick.parlayChoice2}
                </div>
                <div class="col-2 previewTeam odds">
                    ${pick.parlayChoice3}
                </div>
            </div>`;

        $eachPick.append(nextPick);
    });
    
}

function calculateParlay(){
    let betAmount = parseFloat($calc.val());

    // if (100 < betAmount || 0 >= betAmount) {
    //     alert('Please enter a valid bet amount between 1 and 100.');
    //     return;
    // }

    // convert American odds to Decimal odds to prep for calculations
    // Calculate the total odds (multiply all odds together)
    const totalOdds = picks.reduce((acc, pick) => {
    let dec;
    parseInt(pick.parlayChoice3) > 0 ? dec = (pick.parlayChoice3/100)+1 : dec = -(100/pick.parlayChoice3)+1;
    return acc * dec;
    }, 1);

    payOut = (betAmount * totalOdds).toFixed(2);
    
    if (payOut == "NaN"){
        $winAmount.text("");
        return;
    }
    $winAmount.text(`To Win: ${payOut}`);
;}

$('.show-overlay').on('click', function (e) {
    e.preventDefault();
    if (picks.length === 0){
        alert("Please select picks first")
    }
    else{
        showPreview(picks);
    }
})

$('.game-box').on('click', function (e) {
    let gameData = JSON.parse($(this).data('value'));
    console.log(gameData);
    if (gameData['over_under'] == "OFF") {
        return
    }
    
    let checkbox = $(this);

    checkbox.toggleClass('checked')

    if (checkbox.hasClass('checked')) {
        picks.push(gameData);
    }
    else {
        picks.pop(gameData);
    }
});

$calc.on('keyup', (e) => {
    calculateParlay();
})

$('#submitParlayBtn').on('click', (e) =>{
    e.preventDefault();
    console.log(picks);
    let betAmount = $calc.val();
    let toWin = payOut;
    let data = {
        key1 : picks,
        betAmount : betAmount,
        toWin : toWin,
    };

    $.ajax({
        type: 'POST',
        url: '/submit-parlay',
        // dataType: 'json',
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            console.log('Parlay submitted successfully:');
            window.location.href = "http://127.0.0.1:5000/action";
        },
        error: function (error) {
            console.error('Error submitting parlay:');
        }
    });    
})

$('#balanceReset').on('click', (e) => {
    $.ajax({
        type: 'POST',
        url: '/reset-balance',
        data: '100',
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            console.log('Balance reset successfully');
            window.location.href = "http://127.0.0.1:5000/";
        },
        error: function (error) {
            console.error('Error resetting balance');
        }
    });
})
