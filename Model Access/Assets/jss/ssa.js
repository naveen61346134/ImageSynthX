function checkProcessedStatus() {
    var fileName = document.getElementById('filename').value;
    console.log(fileName)
    $.ajax({
        url: '/check_processed_status/' + fileName,
        type: 'GET',
        success: function (response) {
            if (response.status === 'success') {
                $('#output-div').removeClass('loading');
                console.log("Removed loading class")
                $('#output-div').css('background-image', 'url(' + response.result_url + '.png' + ')');
                console.log("Changed background to:" + response.result_url + ".png")
            } else {
                setTimeout(checkProcessedStatus, 1000);
                console.log("Waiting for file")
            }
        },
        error: function () {
            console.log('Error checking processed status.');
        }
    });
}

$(document).ready(function () {
    checkProcessedStatus();
    $('form').submit(function () {
        document.getElementById('output-div').style.backgroundImage = 'url("/Assets/gifs/loader2.gif")';
        checkProcessedStatus();
    });
});
