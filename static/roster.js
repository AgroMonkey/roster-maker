var start_date = null;
var end_date = null;

$(function() {
    start_date = new Date($('#startDate').val());
    end_date = new Date($('#endDate').val());
    $('#dateRangePicker').daterangepicker({
        /*ranges: {
            'Today': [moment(), moment()],
            'Tomorrow': [moment().add(1, 'days'), moment().add(1, 'days')],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Current Week': [moment().startOf('week').add(1, 'days'), moment().endOf('week').add('1')],
            'Next Week': [moment().startOf('week').add(8, 'days'), moment().endOf('week').add(8, 'days')],
            'Previous Week': [moment().startOf('week').subtract(6, 'days'), moment().endOf('week').subtract(6, 'days')],
        },*/
        "locale": {
            "autoUpdateInput": false,
            "format": "DD/MM/YYYY",
            "separator": " - ",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "firstDay": 1
        },
        "linkedCalendars": false,
        "singleRangePicker": true,
        "opens": "center",
        "startDate": start_date,
        "endDate": end_date
    });

    /*Submit form on apply of new range*/
    $('#dateRangePicker').on('apply.daterangepicker', function(ev, picker) {
        $('#startDate').val(picker.startDate.format('YYYY-MM-DD'));
        $('#endDate').val(picker.endDate.format('YYYY-MM-DD'));
        $('#dateRangeForm').submit();
    });

    /*Reset date range if clicked outside*/
    /* global moment */
    $('#dateRangePicker').on('outsideClick.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(start_date);
        $(this).data('daterangepicker').setEndDate(end_date);
        $('#dateRangePicker').val(moment(start_date).format("DD/MM/YYYY") + " - " + moment(end_date).format("DD/MM/YYYY"));
    });

});