// 通知リンクをクリックした時の処理
$(document).on('click', '.notification_aria_anker', function() {
    const url = $(this).attr('action');
    const notification_id = $(this).attr('notification-id');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'notification_id': notification_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// バツボタンをクリックした時の処理
$(document).on('click', '.notification_aria_list_2', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const notification_id = $(this).attr('notification-id');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'notification_id': notification_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        document.getElementById('notification_aria_link_' + notification_id).remove();
        if (response.notification_count === 0) {
            $('.bi-bell-fill').removeClass('active');
            $('.bi-exclamation-lg').removeClass('active');
        }
    })
    .fail(function(response) {
        console.log(response);
    })
});
