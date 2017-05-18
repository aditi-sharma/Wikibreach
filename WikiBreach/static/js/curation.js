 $('[id^=deleteAlert]').unbind().click(function(e) {
        // do NOT submit the form as a regular POST request
        e.preventDefault();
        message_id = $(this).attr('value');
        $.ajax({
            type: 'POST',
            url: '/getAlerts/',
            data: {'id': message_id},
            success: function() {
                alert('Message deleted!');
                $('#'+message_id).remove();
             },
            fail : function() {
                alert('Unable to delete the message. Please reload page and try again!');
            },
            error : function(xhr,errmsg,err) {
            alert('Unable to delete the message. Please reload page and try again!');
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
                });
     });

     $('[id^=deletePost]').unbind().click(function(e) {
        // do NOT submit the form as a regular POST request
        e.preventDefault();
        id = $(this).attr('value');
        $.ajax({
            type: 'POST',
            url: '/rejectUserPost/',
            data: {'id': id},
            success: function() {
                alert('User Post deleted!');
                $('#'+id).remove();
             },
            fail : function() {
                alert('Unable to delete the user post. Please reload page and try again!');
            },
            error : function(xhr,errmsg,err) {
            alert('Unable to delete the user post. Please reload page and try again!');
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
                });
     });