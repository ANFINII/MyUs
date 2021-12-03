// バツボタンをクリックした時の処理
$(document).on('click', '.notification_aria_list_2', function(event) {
    event.preventDefault();
    const notification_id = $(this).attr('notification-id');
    document.getElementById('notification_aria_link_' + notification_id).remove();
});


// コメントリプライ 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
// $(document).on('click', '.edit_delete', function(event) {
//     event.preventDefault();
//     const url = $(this).parent().attr('action');
//     const id = $(this).attr('obj-id');
//     const path = $(this).attr('path');
//     const comment_id = $(this).attr('comment-id');
//     document.getElementById('modal_content_' + comment_id).classList.remove('active');
//     document.getElementById('mask_' + comment_id).classList.remove('active');
//     // 削除時のアニメーション
//     const highlight = document.querySelector('#comment_aria_list_' + comment_id);
//     highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: {'id': id, 'path': path, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: 'json',
//         timeout: 10000,
//     })
//     .done(function(response) {
//         $('#comment_aria_list_' + comment_id).remove();
//         $('#comment_count').html(response.comment_count);
//         $('#reply_count_open_' + response.parent_id).html('▼ スレッド ' + response.reply_count + ' 件');
//         $('#reply_count_close_' + response.parent_id).html('▲ スレッド ' + response.reply_count + ' 件');
//         console.log(response);
//     })
//     .fail(function(response) {
//         // 失敗した時、背景色を戻す
//         highlight.style.removeProperty('background-color');
//         console.log(response);
//     })
// });
