function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function proceedToBook(roomId){
    console.log(roomId);
    $.ajax({
        url: '/getcontactinfo',
        data: {
            "roomId": roomId,
        },
        type: 'POST',
        success: function(response) {
            window.location.replace(response.redirectUrl);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function cancelBooking(bookingId){
    $.ajax({
        url: '/cancelbooking',
        data: {
            'bookingId': bookingId,
        },
        type: 'POST',
        success: function(response) {
            if (response.status == 'ok'){
                alert('Booking successfully cancelled');
                location.reload();
            }
            else{
                alert('Problem while cancelling booking');
                location.reload();
            }
            
        },
        error: function(error) {
            console.log(error);
        }
    });
}



$(document).ready( function () {
    $('#bookings').DataTable();
} );
