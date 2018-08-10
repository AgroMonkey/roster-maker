$(document).ready(function(){
    // Toggles password fields
    $("#changePass").click(function(){
        $(".inputPass").attr("disabled",!this.checked);
    });
});