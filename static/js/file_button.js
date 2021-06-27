$(document).on('click', '#select_file_button', function() { 
    $("#file_button").click();
})

$(document).on('change', '#file_button', function() { 
    $('#filename').val($(this).val().replace(/^.*\\/, ""));
})
