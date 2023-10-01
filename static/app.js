let picks = []

function printLogic(pick){
    if (pick.cat === "spread"){
        pick.parlayChoice1 = pick.choice;
        pick.PS > 0 ? pick.parlayChoice2 = `+${pick.PS}` : pick.parlayChoice2 = pick.PS;
        pick.parlayChoice3 = pick.price;
    }
    if (pick.cat === "ml"){
        pick.parlayChoice1 = pick.choice;
        pick.parlayChoice2 = "ML";
        pick.ml_price > 0 ? pick.parlayChoice3 = `+${pick.ml_price}` : pick.parlayChoice3 = pick.ml_price;
    }
    if (pick.cat === "total"){
        pick.parlayChoice1 = `${pick.choice} | ${pick.team1.substring(0,3)} @ ${pick.team2.substring(0,3)}`;
        pick.parlayChoice2 = pick.over_under;
        pick.parlayChoice3 = pick.over_under_price;
    }
}

function showPreview(picks) {
    console.log(picks);

    const overlay = document.getElementById('overlay');
    overlay.style.display = 'block';

    const closeOverlayBtn = document.getElementById('closeOverlayBtn');
    closeOverlayBtn.addEventListener('click', function () {
        overlay.style.display = 'none';
    });

    let $eachPick = $('.eachPick');
    $eachPick.html(" ");

    picks.forEach(function (pick) {
        // Access properties of each pick
        let game_id = pick.game_id;
        let choice = pick.choice;
        let away_PS = pick.away_PS;
        let away_PS_price = pick.away_PS_price;

        // Perform an action for each pick
        console.log(`Game ID: ${game_id}`);
        console.log(`Team: ${choice}`);
        console.log(`Away Point Spread: ${away_PS}`);
        console.log(`Away Point Spread Price: ${away_PS_price}`);
        console.log('------------------------');

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

$('.btn2').on('click', function (e) {
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
    // console.log(gameData);
    let checkbox = $(this);

    checkbox.toggleClass('checked')

    if (checkbox.hasClass('checked')) {
        picks.push(gameData);
    }
    else {
        picks.pop(gameData);
    }
});


