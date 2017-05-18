$("#button").click(function(e) {
        // do NOT submit the form as a regular POST request
        email = $('input:text').val()
        e.preventDefault();
        if (validateEmail(email)){
             $.ajax({
            type: 'GET',
            url: '/getBreaches/',
            data: {'account': email},
            dataType: 'text',
            success: function(response) {
               if (response.indexOf("404 - Not found")> -1){
                    $(".resultTitle").show();
                    $(".resultTitle").html("Good news — We found no breaches on your account");
                    $(".pwnedTitle").hide();
                    $(".breachResult").hide();
                    }
               else {
                var arr = JSON.parse(response);
                $(".resultTitle").hide();
                 $(".pwnedTitle").show();
                $(".pwnedTitle").html("Oh no! you have been Pwned!");
                $(".breachResult").show();
                var out = "<h4>Please see the details below:</h4>" + "<div class=\"breachEntries\">";
for(i = 0; i < arr.length; i++) {
        out += "<div class=\"breachEntry\" id=\"breachEntry" + i + "\"><div class=\"breachDomain\"><strong>Domain of Breach:&nbsp;</strong>" + arr[i].Name +
        "&nbsp;(<a href=\"http://" + arr[i].Domain + "\" target=\"_blank\"><strong>http://" + arr[i].Domain + "</a></strong>):&nbsp;" +
        "</div><div class=\"breachDesc\">" +
        arr[i].Description +
        "</div><div class=\"breachItems\"><strong>Breached Items:&nbsp;</strong>" +
        arr[i].DataClasses +
         "</div><div class=\"breachCount\"><strong>Total number of accounts breached:&nbsp;</strong>" +
        arr[i].PwnCount +
        "</div><div class=\"breachDate\"><strong>Breach Date:&nbsp;</strong>" +
        arr[i].BreachDate +
        "</div></div><hr>";
        }
    out += "</div>";
                $(".breachResult").html(out);
                }
             },
            fail : function() {
                alert(" NOT DONE");
            },
            error : function(xhr,errmsg,err) {
            alert(errmsg);
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
     });
        }
        else {
            alert("Please enter a valid email address");
        }
     });
