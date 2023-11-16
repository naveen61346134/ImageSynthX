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
                // Continue checking
                setTimeout(checkProcessedStatus, 1000); // Check every second
                document.getElementById('output-div').style.backgroundImage = 'url("/Assets/gifs/loader2.gif")';
            }
        },
        error: function () {
            console.log('Error checking processed status.');
        }
    });
}

// Start checking status once the page is loaded
$(document).ready(function () {
    $('form').submit(checkProcessedStatus);
    checkProcessedStatus(); // Call it once on page load
});