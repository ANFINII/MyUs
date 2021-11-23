// WebSocketオブジェクト
let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
const chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/chat/detail/' + obj_id);

$('#comment_form').submit(function(event) {
    event.preventDefault();
    const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    const message = $('form [name=text]').val().replace(/\n+$/g,'');
    $('#comment_form')[0].reset();
    document.getElementById('comment_form_area').style.height = '40px';
    document.getElementById('comment_form_button').setAttribute('disabled', true);
    chatSocket.send(JSON.stringify({
        'command': 'create_message',
        'obj_id': obj_id,
        'user_id': user_id,
        'message': message,
    }));
})

chatSocket.onmessage = function(e) {
    document.getElementById('comment_form_button').setAttribute('disabled', true);
    const data = JSON.parse(e.data);
    const response = data['message'];
    console.log(response)
    const render =
    '<div id="comment_aria_list_' + response.comment_id +'" class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
            '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
            '<p>' + response.nickname + ' ' + '</p>' +
            '<time class="time">' + ' ' + response.created + '</time>' +
        '</div>' +
        '<div id="comment_aria_list_2_' + response.comment_id + '" class="comment_aria_list_2">' + response.text + '</div>' +
        '<a href="/chat/detail/thread/' + response.comment_id + '" class="comment_aria_thread">' +
            'スレッド表示' +
            '<span id="reply_count_' + response.comment_id + '">返信 0 件</span>' +
        '</a>' +
        '<div class="edit_button">' +
            '<a type="button" name="update" comment-id="' + response.comment_id + '" class="edit_button_update">編集</a>' +
            '<a type="button" name="delete" comment-id="' + response.comment_id + '" class="edit_button_delete">削除</a>' +
            '<div id="modal_content_' + response.comment_id + '" class="modal_content">' +
                '<h2 class="modal_content_header">メッセージの削除</h2>' +
                '<span class="modal_content_body_span">このメッセージを削除しますか？</span>' +
                '<div class="modal_content_body">' +
                    '<div class="comment_aria_list">' +
                        '<a href="/userpage/' + response.nickname + '">' +
                            '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                        '</a>' +
                        '<div class="comment_aria_list_1">' +
                            '<div class="comment_aria_list_nickname">' + response.nickname + '</div>' +
                            '<time class="comment_aria_list_time">' + response.created + '</time>' +
                        '</div>' +
                        '<div class="comment_aria_list_1">' + response.message + '</div>' +
                    '</div>' +
                '</div>' +
                '<form method="POST" action="/chat/detail/message/delete/' + response.comment_id + '" class="modal_content_footer">' +
                    '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light modal_cancel">' +
                    '<input type="button" name="delete" value="削除" comment-id="' + response.comment_id + '"  obj-id="' + response.obj_id + '" class="btn btn-danger edit_delete">' +
                '</form>' +
            '</div>' +
            '<div comment-id="' + response.comment_id + '" id="mask_' + response.comment_id + '" class="mask modal_cancel"></div>' +
        '</div>' +
    '</div>' +
    '<div id="edit_update_main_' + response.comment_id + '" class="edit_update_main_chat">' +
        '<form method="POST" action="/chat/detail/message/update/' + response.comment_id + '" comment-id="' + response.comment_id + '" class="edit_update_chat">' +
            '<a href="/userpage/' + response.nickname + '">' +
                '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
            '</a>' +
            '<div class="edit_textarea_caht">' +
                '<textarea name="update_text" rows="1" class="textarea_br" placeholder="メッセージ入力" id="comment_form_update_' + response.comment_id + '" required>' + response.text + '</textarea>' +
                '<div class="chat_frame"></div>' +
                '<div class="comment_input_chat"></div>' +
                '<div class="edit_update_footer">' +
                    '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light btn-xs edit_update_cancel">' +
                    '<input type="submit" name="update" value="更新" class="btn btn-success btn-xs">' +
                '</div>' +
            '</div>' +
        '</form>' +
    '</div>';

    $('#chat_section_main_area').append(render);
//     // $('#chat_section_main_area').append(response.comment_lists);
//     // $('#user_count').html(response.user_count);
//     // $('#comment_count').html(response.comment_count);
//     $('#chat_section_main_area').html(response.comment_lists);
//     // const obj = document.getElementById('chat_section_main_area');
//     // obj.scrollTop = obj.scrollHeight;
    console.log(e);
};


// chatSocket.onopen = function(e) {
//     // fetchMessage();
//     console.log('open', e)
// }

// chatSocket.onerror = function(e) {
//     console.log('error', e)
// }

// chatSocket.onclose = function(e) {
//     console.log('close', e)
// }

// chatSocket.onmessage = function(e) {
//     let data = JSON.parse(e.data);
//     if (data['command'] === 'messages') {
//         for (let i=0; i<data['messages'].length; i++) {
//             createMessage(data['messages'][i]);
//         }
//     } else if (data['command'] === 'create_message') {
//         createMessage(data['message']);
//     }
// };

// function fetchMessage() {
//     chatSocket.send(JSON.stringify({'command': 'fetch_message'}));
// }

// function createMessage(data) {
//     let author = data['nickname']
// }

// いいねボタンクリック時の処理を定義
$(document).on('click', '.like_form', function(event) {
    event.preventDefault();
    const id = $(this).attr('value');
    const url = $(this).parent().attr('action');
    const path = $(this).parent().attr('path');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'path': path, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
    })
    .done(function(response) {
        if (response['liked']) {
            $('.like_color').removeClass('bi-hand-thumbs-up');
            $('.like_color').parent().removeClass('like_no');
            $('.like_color').addClass('bi-hand-thumbs-up-fill');
            $('.like_color').parent().addClass('like_fill');
            $('#like_count_' + id).html(response['total_like']);
        } else {
            $('.like_color').removeClass('bi-hand-thumbs-up-fill');
            $('.like_color').parent().removeClass('like_fill');
            $('.like_color').addClass('bi-hand-thumbs-up');
            $('.like_color').parent().addClass('like_no');
            $('#like_count_' + id).html(response['total_like']);
        }
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// フォローボタンクリック時の処理を定義
$(document).on('click', '.follow_form', function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const nickname = $(this).children().attr('value');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'nickname': nickname, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
    })
    .done(function(response) {
        if (response['followed']) {
            $('.follow_change').removeClass('btn-success');
            $('.follow_change').addClass('btn-danger');
            $('.btn-danger').html('解除する');
            $('.follower_count').html(response['follower_count']);
        } else {
            $('.follow_change').removeClass('btn-danger');
            $('.follow_change').addClass('btn-success');
            $('.btn-success').html('フォローする');
            $('.follower_count').html(response['follower_count']);
        }
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
// $('#comment_form').submit(function(event) {
//     event.preventDefault();
//     const url = $(this).attr('action');
//     const id = $(this).attr('obj-id');
//     const text = $('form [name=text]').val().replace(/\n+$/g,'');
//     $('#comment_form')[0].reset();
//     document.getElementById('comment_form_area').style.height = '40px';
//     document.getElementById('comment_form_button').setAttribute('disabled', true);
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: {'id': id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: 'json',
//         timeout: 10000,
//     })
//     .done(function(response) {
//         document.getElementById('comment_form_button').setAttribute('disabled', true);
//         $('#user_count').html(response.user_count);
//         $('#comment_count').html(response.comment_count);
//         $('#chat_section_main_area').append(response.comment_lists);
//         const obj = document.getElementById('chat_section_main_area');
//         obj.scrollTop = obj.scrollHeight;
//         console.log(response);
//     })
//     .fail(function(response) {
//         console.log(response);
//     })
// });

// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#reply_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const id = $(this).attr('obj-id');
    const comment_id = $(this).attr('comment-id');
    const reply = $('form [name=reply]').val().replace(/\n+$/g,'');
    $('#reply_form')[0].reset();
    document.getElementById('reply_form_area').style.height = '40px';
    document.getElementById('reply_form_button').setAttribute('disabled', true);
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'reply': reply, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#user_count').html(response.user_count);
        $('#reply_count_' + comment_id).html('返信 ' + response.reply_count + ' 件');
        $('#chat_section_thread_area').append(response.reply_lists);
        const obj = document.getElementById('chat_section_thread');
        obj.scrollTop = obj.scrollHeight;
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// メッセージ編集
$(document).on('click', '.edit_button_update', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('edit_update_main_' + comment_id).classList.add('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.add('active');
    document.getElementById('comment_form_update_' + comment_id).style.height = '40px';
    $('#comment_form_update_' + comment_id).textareaAutoHeight();
})

$(document).on('click', '.edit_update_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
})

$(document).on('click', '.edit_update_button', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const comment_id = $(this).attr('comment-id');
    const text = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g,'');
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
    document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
    // 更新時のアニメーション
    const highlight = document.querySelector('#comment_aria_list_' + comment_id);
    highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        // 成功した時、背景色を戻す
        highlight.style.removeProperty('background-color');
        $('#comment_aria_list_2_' + comment_id).html(response.text);
        console.log(response);
    })
    .fail(function(response) {
        // 失敗した時、背景色を戻す
        highlight.style.removeProperty('background-color');
        console.log(response);
    })
});

// メッセージ削除ダイアログ
$(document).on('click', '.edit_button_delete', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.add('active');
    document.getElementById('mask_' + comment_id).classList.add('active');
});

$(document).on('click', '.modal_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
});

$(document).on('click', '.edit_delete_comment', function(event) {
    event.preventDefault();
    const url = $(this).parent().attr('action');
    const id = $(this).attr('obj-id');
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
    // 削除時のアニメーション
    const highlight_1 = document.querySelector('#comment_aria_list_' + comment_id);
    const highlight_2 = document.querySelector('#comment_aria_list_cross_' + comment_id);
    highlight_1.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    if (highlight_2 !== null) {
        highlight_2.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    }
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_' + comment_id).remove();
        $('#comment_aria_list_2_' + comment_id).html('スレッドが削除されました！');
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        console.log(response);
    })
    .fail(function(response) {
        // 失敗した時、背景色を戻す
        highlight_1.style.removeProperty('background-color');
        highlight_2.style.removeProperty('background-color');
        console.log(response);
    })
});

$(document).on('click', '.edit_delete_reply', function(event) {
    event.preventDefault();
    const url = $(this).parent().attr('action');
    const id = $(this).attr('obj-id');
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
    // 削除時のアニメーション
    const highlight = document.querySelector('#comment_aria_list_' + comment_id);
    highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_' + comment_id).remove();
        $('#user_count').html(response.user_count);
        $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件');
        console.log(response);
    })
    .fail(function(response) {
        // 失敗した時、背景色を戻す
        highlight.style.removeProperty('background-color');
        console.log(response);
    })
});

// textareaのdisabled判定
// replyショートカット
$(document).on('focus', '#reply_form_area', function(event) {
    event.preventDefault();

    // focus時にそれ以外のtextareaを無効化する
    const targetElem = document.querySelectorAll('.form_button');
    const targetCount = targetElem.length;
    if (targetElem) {
        for (let i = 0; i < targetCount; i++)
        targetElem[i].setAttribute('disabled', true);
    }

    const text = $(this).val();
    if (text || text.match(/\S/g)) {
        // disabled属性を削除
        document.getElementById('reply_form_button').removeAttribute('disabled');
    }

    $(document).on('input', '#reply_form_area', function(event) {
        event.preventDefault();
        const text = $(this).val();
        if (!text || !text.match(/\S/g)) {
            // disabled属性を設定
            document.getElementById('reply_form_button').setAttribute('disabled', true);
        } else {
            // disabled属性を削除
            document.getElementById('reply_form_button').removeAttribute('disabled');

            // ショートカット
            shortcut.add('Ctrl+Enter', function() {
                $('#reply_form_button').click();
            });
            shortcut.add('meta+Enter', function() {
                $('#reply_form_button').click();
            });
        }
    });
});
