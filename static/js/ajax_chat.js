// WebSocketオブジェクト
let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
const chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/chat/detail/' + obj_id);

$('#comment_form').submit(function(event) {
    event.preventDefault();
    const obj_id = $(this).attr('obj-id');
    const message = $('form [name=text]').val().replace(/\n+$/g,'');
    $('#comment_form')[0].reset();
    document.getElementById('comment_form_area').style.height = '40px';
    document.getElementById('comment_form_button').setAttribute('disabled', true);
    chatSocket.send(JSON.stringify({
        'command': 'create_message',
        'obj_id': obj_id,
        'message': message,
    }));
})

chatSocket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    if (data['command'] === 'fetch_message') {
        for (let i=0; i<data['messages'].length; i++) {
            createMessage(data['messages'][i]);
        }
    } else if (data['command'] === 'create_message') {
        document.getElementById('comment_form_button').setAttribute('disabled', true);
        const response = data['message'];
        $('#chat_section_main_area').append(response.comment_lists);
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        const obj = document.getElementById('chat_section_main_area');
        obj.scrollTop = obj.scrollHeight;
        console.log(response)
        console.log(event);
    } else if (data['command'] === 'update_message') {
        const response = data['message'];
        // 成功した時、背景色を戻す
        const highlight = document.querySelector('#comment_aria_list_' + response.comment_id);
        highlight.style.removeProperty('background-color');
        $('#comment_aria_list_2_' + response.comment_id).html(response.text);
        console.log(response);
        console.log(event);
    } else if (data['command'] === 'delete_message') {
        const response = data['message'];
        $('#comment_aria_list_' + response.comment_id).remove();
        $('#edit_update_main_' + response.comment_id).remove();
        $('#comment_aria_list_2_' + response.comment_id).html('スレッドが削除されました！');
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        console.log(response);
    }
};

function fetchMessage() {
    const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
    console.log(obj_id)
    chatSocket.send(JSON.stringify({
        'command': 'fetch_message',
        'obj_id': obj_id,
    }));
}

chatSocket.onopen = function(event) {
    fetchMessage();
    console.log('open', event)
}

chatSocket.onerror = function(event) {
    console.log('error', event)
}

chatSocket.onclose = function(event) {
    console.log('close', event)
}

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
    const comment_id = $(this).attr('comment-id');
    const message = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g,'');
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
    document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
    // 更新時のアニメーション
    const highlight = document.querySelector('#comment_aria_list_' + comment_id);
    highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
    chatSocket.send(JSON.stringify({
        'command': 'update_message',
        'comment_id': comment_id,
        'message': message,
    }));
})

// $(document).on('click', '.edit_update_button', function(event) {
//     event.preventDefault();
//     const url = $(this).closest('form').attr('action');
//     const comment_id = $(this).attr('comment-id');
//     const text = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g,'');
//     document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
//     document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
//     document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
//     // 更新時のアニメーション
//     const highlight = document.querySelector('#comment_aria_list_' + comment_id);
//     highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: {'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: 'json',
//         timeout: 10000,
//     })
//     .done(function(response) {
//         // 成功した時、背景色を戻す
//         highlight.style.removeProperty('background-color');
//         $('#comment_aria_list_2_' + comment_id).html(response.text);
//         console.log(response);
//     })
//     .fail(function(response) {
//         // 失敗した時、背景色を戻す
//         highlight.style.removeProperty('background-color');
//         console.log(response);
//     })
// });

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
    chatSocket.send(JSON.stringify({
        'command': 'delete_message',
        'comment_id': comment_id,
    }));
})



// $(document).on('click', '.edit_delete_comment', function(event) {
//     event.preventDefault();
//     const url = $(this).parent().attr('action');
//     const id = $(this).attr('obj-id');
//     const comment_id = $(this).attr('comment-id');
//     document.getElementById('modal_content_' + comment_id).classList.remove('active');
//     document.getElementById('mask_' + comment_id).classList.remove('active');
//     // 削除時のアニメーション
//     const highlight_1 = document.querySelector('#comment_aria_list_' + comment_id);
//     const highlight_2 = document.querySelector('#comment_aria_list_cross_' + comment_id);
//     highlight_1.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
//     if (highlight_2 !== null) {
//         highlight_2.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
//     }
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: {'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: 'json',
//         timeout: 10000,
//     })
//     .done(function(response) {
//         $('#comment_aria_list_' + comment_id).remove();
//         $('#edit_update_main_' + comment_id).remove();
//         $('#comment_aria_list_2_' + comment_id).html('スレッドが削除されました！');
//         $('#user_count').html(response.user_count);
//         $('#comment_count').html(response.comment_count);
//         console.log(response);
//     })
//     .fail(function(response) {
//         // 失敗した時、背景色を戻す
//         highlight_1.style.removeProperty('background-color');
//         highlight_2.style.removeProperty('background-color');
//         console.log(response);
//     })
// });

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
