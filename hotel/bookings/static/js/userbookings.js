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




function ProceedToBook(roomId, days){
    $.ajax({
        url: '/checkLogIn',
        data: {
            'roomId': roomId,
        },
        type: 'POST',
        success: function(response) {
            console.log(response.redirectUrl);
            window.location.replace(response.redirectUrl);
        },
        error: function(error) {
            console.log(error);
        }
    });
}