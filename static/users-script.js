/* global request */

$(document).ready(function(){
    let user_id = 0;
    // Updates user_id when a row is clicked and adds selected class
    $(".user_row").click(function(){
        $(".selected :radio").prop( "checked", false );
        $(".selected").removeClass("selected");
        $(this).addClass("selected");
        $(".selected :radio").prop( "checked", true );
        user_id = $(".selected :radio").val();
        console.log("Selected User ID: " + user_id);
    });

    $("#btnEdit").click(function(){
        if (user_id != 0) {
            request("/edituser", {id: user_id}, "get");
        } else {
            alert("No user selected");
        }

    });

    $("#btnReset").click(function(){
        if (user_id != 0) {
            request("/resetuser", {id: user_id});
        } else {
            alert("No user selected");
        }
    });

    $("#btnDelete").click(function(){
        if (user_id != 0) {
            request("/deleteuser", {id: user_id});
        } else {
            alert("No user selected");
        }
    });
});