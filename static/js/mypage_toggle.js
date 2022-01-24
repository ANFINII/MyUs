// トグルボタンをクリックした時の処理
$(document).on('click', '.toggle_mypage', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const advertise = $(this).closest('form').attr('advertise');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'advertise': advertise, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#auto_advertise').html(response.advertise);
    })
    .fail(function(response) {
        console.log(response);
    })
});
