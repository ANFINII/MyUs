// トグルボタンをクリックした時の処理
$(document).on('click', '.toggle_button', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const notify = $(this).closest('form').attr('notify');
    const notify_type = $(this).closest('form').attr('notify-type');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'notify': notify, 'notify_type': notify_type, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#notification_table').html(response.notify_setting_lists);
    })
    .fail(function(response) {
        console.log(response);
    })
});
