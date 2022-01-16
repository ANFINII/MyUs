$('input[id=custom_file_1]').change(function(){ $('#file_1').val($(this).val().replace('C:\\fakepath\\', '')); });

$('input[id=custom_file_2]').change(function(){ $('#file_2').val($(this).val().replace('C:\\fakepath\\', '')); });
