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
    .done(function() {
    })
    .fail(function() {
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


// 通知設定のトグルボタンをクリックした時の処理
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
