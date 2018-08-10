$(document).ready( function() {
    var curr = new Date; // get current date
    var first = curr.getDate() - curr.getDay() + 1; // First day is the day of the month - the day of the week
    var last = first + 6;
    var start = new Date;
    start.setDate(first);
    var end = new Date;
    end.setDate(last);
    $('#startDate').val(formatDate(start));
    $('#endDate').val(formatDate(end));
});

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

function formatDate(date) {
    var day = date.getDate();
    day = pad(day);
    var month = date.getMonth();
    ++month;
    month = pad(month);
    var year = date.getFullYear();
    return (year + "-" + month + "-" + day);
}