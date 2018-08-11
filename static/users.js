var user_id = null;
var username= null;
var email = null;
var real_name = null;
var role = null;

$(function() {
    $.contextMenu({
        selector: 'td',
        callback: function(key, options) {
            var m = "clicked: " + key + "\nUser ID: " + user_id;
            window.console && console.log(m);
        },
        items: {
            "add": {
                name: "Add",
                icon: "add",
                callback: function(key, options) {
                    user_id = null;
                    username = null;
                    email = null;
                    real_name = null;
                    role = null;
                    $('#changePass').prop('checked', true);
                    $('#changePassRow').hide();
                    $("input[name='password']").prop('required',true);
                    $("input[name='confirmation']").prop('required',true);
                    $('.inputPass').removeAttr("disabled");
                    $('#modalEditForm').modal();
                }
            },
            "edit": {
                name: "Edit",
                icon: "edit",
                callback: function(key, options) {
                    $('#modalEditForm').modal();
                }
            },
            "delete": {
                name: "Delete",
                icon: "delete",
                callback: function(key, options) {
                    var m = "clicked: " + key + "\nUser ID: " + user_id;
                    window.console && console.log(m);
                    /*global request*/
                    request("/deleteuser", {id: user_id});
                }
            }
        }
    });

    $('.user_row').contextmenu(function (e) {
        user_id = this.dataset.user_id;
        username = this.dataset.username;
        email = this.dataset.email;
        real_name = this.dataset.real_name;
        role = this.dataset.role;
    });

    $(".user_row").click(function(){
        $(".selected :radio").prop( "checked", false );
        $(".selected").removeClass("selected");
        $(this).addClass("selected");
        $(".selected :radio").prop( "checked", true );
        user_id = $(".selected :radio").val();
        console.log("Selected User ID: " + user_id);
        user_id = this.dataset.user_id;
        username = this.dataset.username;
        email = this.dataset.email;
        real_name = this.dataset.real_name;
        role = this.dataset.role;
    });

    $("#btnAdd").click(function(){
        user_id = null;
        username = null;
        email = null;
        real_name = null;
        role = null;
        $('#changePass').prop('checked', true);
        $('#changePassRow').hide();
        $("input[name='password']").prop('required',true);
        $("input[name='confirmation']").prop('required',true);
        $('.inputPass').removeAttr("disabled");
        $('#modalEditForm').modal();
    });

    $("#btnEdit").click(function(){
        if (user_id) {
            $('#changePassRow').show();
            $('#modalEditForm').modal();
        } else {
            alert("No user selected");
        }
    });

    $("#btnDelete").click(function(){
        if (user_id) {
            request("/deleteuser", {id: user_id});
        } else {
            alert("No user selected");
        }
    });

    /*Reset form when modal is hidden*/
    $('#modalEditForm').on('hidden.bs.modal', function(e) {
        console.log("Hidden");
        $('#modalForm').trigger("reset");
        $('#changePass').prop('checked', false);
        $("input[name='password']").prop('required',false);
        $("input[name='confirmation']").prop('required',false);
        $('.inputPass').attr("disabled", true);
        $('#changePassRow').show();
        user_id = null;
        username= null;
        email = null;
        real_name = null;
        role = null;
    });

    /*Initialise input data*/
    $('#modalEditForm').on('show.bs.modal', function(e) {
        $("input[name='user_id']").val( user_id );
        $("input[name='username']").val( username );
        $("input[name='email']").val( email );
        $("input[name='real_name']").val( real_name );
        $('#role').find('option:selected').removeAttr('selected');
        $('#role [value=' + role +']').attr("selected", "selected");
    });

    $("#changePass").click(function(){
        $(".inputPass").attr("disabled",!this.checked);
        $("input[name='password']").prop('required',this.checked);
        $("input[name='confirmation']").prop('required',this.checked);
    });
});