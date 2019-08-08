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

function generateNamesForm(numOfPeople){
    content = '<form id="namesForm">';
    for (i = 1; i <= numOfPeople; i++)
    {
        content +='  <div>'+
                 '     <label>Name '+i+'</label>'+
                 '  </div>'+
                 '  <div>'+
                 '       <input type="text" name="name'+i+'" placeholder="Name'+i+'" required>'+
                 '  </div>'+
                 '  <div>'+
                 '     <label>Surname '+i+'</label>'+
                 '  </div>'+
                 '  <div>'+
                 '       <input type="text" required name="surname'+i+'" placeholder="Surname'+i+'">'+
                 '  </div>'+
                 '<br>';    
    }
    content += '</form>'
    return content
}


function getGuestsNames(bookingId, numOfPeople){

    $.confirm({
        title: 'Confirm!',
        content: generateNamesForm(numOfPeople),
        buttons: {
            confirm: function () {
                var form = document.getElementById('namesForm');
                var formData = new FormData(form);
                doCheckIn(bookingId, formData, numOfPeople);
            },
            cancel: function () {
                $.alert('Canceled!');
            },
        }
    });
}






function doCheckIn(bookingId, formData, numOfPeople){
    
    
    formData.append('bookingId', bookingId);
    formData.append('numOfPeople', numOfPeople);

    for (var pair of formData.entries()) {
        console.log(pair[0]+ ', ' + pair[1]); 
    }

    $.ajax({
        type: 'POST',
        url: '/docheckin',
        dataType: 'json',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,

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