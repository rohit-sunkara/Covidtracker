$(document).ready(function () {
    $('.modal').modal();
    $('.datepicker').datepicker({
        format: 'dd-mm-yyyy'
    });
    $('select').formSelect();
});