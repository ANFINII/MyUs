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

// コメントいいねボタンクリック時の処理を定義
$(document).on('click', '.like_form_comment', function(event) {
    event.preventDefault();
    const url = $(this).parent().attr('action');
    const comment_id = $(this).attr('value');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
    })
    .done(function(response) {
        if (response['comment_liked']) {
            $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up');
            $('.like_color_' + comment_id).parent().removeClass('like_no');
            $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up-fill');
            $('.like_color_' + comment_id).parent().addClass('like_fill');
            $('#like_count_' + comment_id).html(response['total_like']);
        } else {
            $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up-fill');
            $('.like_color_' + comment_id).parent().removeClass('like_fill');
            $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up');
            $('.like_color_' + comment_id).parent().addClass('like_no');
            $('#like_count_' + comment_id).html(response['total_like']);
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

// コメント 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#comment_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const id = $(this).attr('obj-id');
    const path = $(this).attr('path');
    const text = $('form [name=text]').val().replace(/\n+$/g,'');
    $('#comment_form')[0].reset();
    document.getElementById('comment_form_button').setAttribute('disabled', true);
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'path': path, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_count').html(response.comment_count);
        $('#comment_aria_add').html(response.comment_lists);
        const form_reset = document.getElementById('comment_form_area');
        form_reset.style.height = '39px';
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// 返信コメント表示, 非表示
$(document).on('click', '.reply_button', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.add('active');
    document.getElementById('reply_button_' + comment_id).classList.add('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.remove('vanish');
    $('#reply_' + comment_id).textareaAutoHeight();
})

$(document).on('click', '.reply_button_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active');
    document.getElementById('reply_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish');
})

$(document).on('click', '.reply_cancel_button', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active');
    document.getElementById('reply_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish');
})

$(document).on('click', '.reply_list_button', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('reply_aria_list_' + comment_id).classList.add('active');
    document.getElementById('reply_list_button_' + comment_id).classList.add('vanish');
    document.getElementById('reply_list_button_cancel_' + comment_id).classList.remove('vanish');
})

$(document).on('click', '.reply_list_button_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('reply_aria_list_' + comment_id).classList.remove('active');
    document.getElementById('reply_list_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_list_button_cancel_' + comment_id).classList.add('vanish');
})

// コメントリプライ 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$(document).on('click', '.reply_form', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const id = $(this).attr('obj-id');
    const path = $(this).attr('path');
    const comment_id = $(this).attr('comment-id');
    const text = $('#reply_' + comment_id).val().replace(/\n+$/g,'');
    $('#comment_aria_list_reply_' + comment_id)[0].reset();
    document.getElementById('reply_form_button_' + comment_id).setAttribute('disabled', true);
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'path': path, 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#reply_count_open_' + comment_id).html('▼ スレッド ' + response.reply_count + ' 件');
        $('#reply_count_close_' + comment_id).html('▲ スレッド ' + response.reply_count + ' 件');
        $('#reply_aria_add_' + comment_id).html(response.reply_lists);
        const form_reset = document.getElementById('reply_' + comment_id);
        form_reset.style.height = '39px';
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
    document.getElementById('comment_form_update_' + comment_id).style.height = '31px';
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

$(document).on('click', '.edit_delete', function(event) {
    event.preventDefault();
    const url = $(this).parent().attr('action');
    const id = $(this).attr('obj-id');
    const path = $(this).attr('path');
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
    // 削除時のアニメーション
    const highlight = document.querySelector('#comment_aria_list_' + comment_id);
    highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'path': path, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_' + comment_id).remove();
        $('#comment_count').html(response.comment_count);
        $('#reply_count_open_' + response.parent_id).html('▼ スレッド ' + response.reply_count + ' 件');
        $('#reply_count_close_' + response.parent_id).html('▲ スレッド ' + response.reply_count + ' 件');
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
$(document).on('focus', '.reply_form_area', function(event) {
    event.preventDefault();
    const comment_id = $(this).attr('comment-id');

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
        document.getElementById('reply_form_button_' + comment_id).removeAttribute('disabled');
    }

    $(document).on('input', '#reply_' + comment_id, function(event) {
        event.preventDefault();
        const text = $(this).val();
        if (!text || !text.match(/\S/g)) {
            // disabled属性を設定
            document.getElementById('reply_form_button_' + comment_id).setAttribute('disabled', true);
        } else {
            // disabled属性を削除
            document.getElementById('reply_form_button_' + comment_id).removeAttribute('disabled');

            // ショートカット
            shortcut.add('Ctrl+Enter', function() {
                $('#reply_form_button_' + comment_id).click();
            });
            shortcut.add('meta+Enter', function() {
                $('#reply_form_button_' + comment_id).click();
            });
        }
    });
});
