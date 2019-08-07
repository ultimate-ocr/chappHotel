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

function doCheckIn(bookingId){
    $.ajax({
        url: '/docheckin',
        data: {
            'bookingId': bookingId,
        },
        type: 'POST',
        success: function(response) {
            if (response.status == 'ok'){
                alert('Check in successfully performed');
                location.reload();
            }
            else{
                alert('Problem while doing Check In');
                location.reload();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function doCheckOut(bookingId){
    $.ajax({
        url: '/docheckout',
        data: {
            'bookingId': bookingId,
        },
        type: 'POST',
        success: function(response) {
            if (response.status == 'ok'){
                alert('Check Out successfully performed');
                location.reload();
            }
            else{
                alert('Problem while ding Check out');
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