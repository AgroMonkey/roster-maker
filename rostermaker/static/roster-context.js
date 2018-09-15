var date = null;
var user = null;
var shift_id = null;
var slocation = null;
var start_time = null;
var end_time = null;
var start_date = null;
var end_date = null;
var sbreak = null;

$(function() {
    start_date = new Date($('#startDate').val());
    end_date = new Date($('#endDate').val());
    itemsDisabled = {}
    itemsDisabled["delete"] = true;
    itemsDisabled["edit"] = true;
    $.contextMenu({
        selector: 'td',
        callback: function(key, options) {
            var m = "clicked: " + key + "\nDate: " + date + " User: " + user;
            window.console && console.log(m);
        },
        events: {
            hide : function(options){
                itemsDisabled["delete"] = true;
                itemsDisabled["edit"] = true;
            }
        },
        items: {
            "add": {
                name: "Add",
                icon: "add",
                callback: function(key, options) {
                    shift_id = null;
                    start_time = null;
                    end_time = null;
                    sbreak = null;
                    if (window.location.pathname == "/locations") {
                        user = null;
                    }
                    if (window.location.pathname == "/roster") {
                        slocation = null;
                    }
                    $('#modalEditForm').modal();
                }
            },
            "edit": {
                name: "Edit",
                icon: "edit",
                callback: function(key, options) {
                    $('#modalEditForm').modal();
                },
                disabled: function(key, opt) {
                    return !!itemsDisabled[key];
                }
            },
            "delete": {
                name: "Delete",
                icon: "delete",
                callback: function(key, options) {
                    var m = "clicked: " + key + "\nDate: " + date + " User: " + user;
                    window.console && console.log(m);
                    /*global request*/
                    request("/deleteshift", {shift_id: shift_id}, "post");
                    /*$('.shift[data-shift_id=' + shift_id + ']').remove()*/
                },
                disabled: function(key, opt) {
                    return !!itemsDisabled[key];
                }
            }
        }
    });

    $('td').contextmenu(function (e) {
        date = this.dataset.date;
        if (window.location.pathname == "/locations") {
            slocation = this.dataset.slocation;
        }
        if (window.location.pathname == "/roster") {
            user = this.dataset.user;
        }
    });

    $('.shift').contextmenu(function (e) {
        itemsDisabled["delete"] = false;
        itemsDisabled["edit"] = false;
        shift_id = this.dataset.shift_id;
        if (window.location.pathname == "/locations") {
            user = $(this).find('[data-user]').data('user');
        }
        if (window.location.pathname == "/roster") {
            slocation = $(this).find('[data-location]').data('location');
        }
        start_time = $(this).find('[data-start_time]').data('start_time');
        end_time = $(this).find('[data-end_time]').data('end_time');
        sbreak = $(this).find('[data-break]').data('break');
    });

    /*Reset form when modal is hidden*/
    $('#modalEditForm').on('hidden.bs.modal', function(e) {
        $('#modalForm').trigger("reset");
        date = null;
        if (user) {
            $('#selectRealName').find('option:selected').removeAttr('selected');
            user = null;
            $('#selectRealName').children('option').first().attr("selected", "selected");
        }
        shift_id = null;
        slocation = null;
        start_time = null;
        end_time = null;
        sbreak = null;
    });

    /*Initialise input data*/
    $('#modalEditForm').on('show.bs.modal', function(e)
    {
        if (user) {
            $('#selectRealName').find('option:selected').removeAttr('selected');
            $('#selectRealName [value=' + user +']').attr("selected", "selected");
        }
        $( "input[name='date']" ).val( date );
        $( "input[name='location']" ).val( slocation );
        $( "input[name='start_time']" ).val( start_time );
        $( "input[name='end_time']" ).val( end_time );
        $('#selectBreak').find('option:selected').removeAttr('selected');
        $('#selectBreak [value=' + sbreak +']').attr("selected", "selected");
        $( "input[name='shift_id']" ).val( shift_id );
    });

});