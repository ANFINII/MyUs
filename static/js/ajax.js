// いいねボタンクリック時の処理を定義
$('.like_form').on('click', function(event) {
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
            $('.like_count').html(response['total_like']);
        } else {
            $('.like_color').removeClass('bi-hand-thumbs-up-fill');
            $('.like_color').parent().removeClass('like_fill');
            $('.like_color').addClass('bi-hand-thumbs-up');
            $('.like_color').parent().addClass('like_no');
            $('.like_count').html(response['total_like']);
        }
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// コメントいいねボタンクリック時の処理を定義
$('.like_form_comment').on('click', function(event) {
    event.preventDefault();
    const id = $(this).attr('value');
    const url = $(this).parent().attr('action');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
    })
    .done(function(response) {
        if (response['comment_liked']) {
            $('.like_color_' + id).removeClass('bi-hand-thumbs-up');
            $('.like_color_' + id).parent().removeClass('like_no');
            $('.like_color_' + id).addClass('bi-hand-thumbs-up-fill');
            $('.like_color_' + id).parent().addClass('like_fill');
            $('#like_count_' + id).html(response['total_like']);
        } else {
            $('.like_color_' + id).removeClass('bi-hand-thumbs-up-fill');
            $('.like_color_' + id).parent().removeClass('like_fill');
            $('.like_color_' + id).addClass('bi-hand-thumbs-up');
            $('.like_color_' + id).parent().addClass('like_no');
            $('#like_count_' + id).html(response['total_like']);
        }
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// フォローボタンクリック時の処理を定義
$('.follow_form').on('click', function(event) {
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
    const text = $('form [name=text]').val();
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id':id, 'path': path, 'text':text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        let comment_aria_list_add =
            '<div class="comment_aria_list">' +
                '<a href="/userpage/' + response.nickname +'">' +
                    '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                '</a>' +
                '<div class="comment_aria_list_1">' +
                    '<p>' + response.nickname + '</p>' +
                    '<time>' + ' ' + response.created + '</time>' +
                '</div>' +
                '<div class="comment_aria_list_2">' + response.text + '</div>' +
                '<div class="comment_aria_list_3">' +
                    '<i class="bi bi-hand-thumbs-up icon-font" title="いいね数">' + ' ' + '</i>' +
                    '<label for="reply_aria_check_id" class="reply_aria_check_id">' + '返信' + '</label>' +
                '</div>' +
            '</div>';
        $('#comment_form')[0].reset();
        $('#comment_count').html(response.comment_count);
        $('#comment_aria_add').append(comment_aria_list_add);
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});

// 返信コメント表示, 非表示
$('.reply_button').on('click', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.add('active');
    document.getElementById('reply_button_' + comment_id).classList.add('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.remove('vanish');
})

$('.reply_button_cancel').on('click', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active');
    document.getElementById('reply_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish');
})

$('.reply_cancel_button').on('click', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active');
    document.getElementById('reply_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish');
})

$('.reply_list_button').on('click', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('reply_aria_list_' + comment_id).classList.add('active');
    document.getElementById('reply_list_button_' + comment_id).classList.add('vanish');
    document.getElementById('reply_list_button_cancel_' + comment_id).classList.remove('vanish');
})

$('.reply_list_button_cancel').on('click', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('reply_aria_list_' + comment_id).classList.remove('active');
    document.getElementById('reply_list_button_' + comment_id).classList.remove('vanish');
    document.getElementById('reply_list_button_cancel_' + comment_id).classList.add('vanish');
})

// コメントリプライ 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('.reply_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const id = $(this).attr('obj-id');
    const path = $(this).attr('path');
    const comment_id = $(this).attr('comment-id');
    const text = $('form [name=reply]').val();
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'path': path, 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        let reply_aria_list_add =
        '<div class="comment_aria_list">' +
            '<a href="/userpage/' + response.nickname +'">' +
                '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
            '</a>' +
            '<div class="comment_aria_list_1">' +
                '<p>' + response.nickname + '</p>' +
                '<time>' + ' ' + response.created + '</time>' +
            '</div>' +
            '<div class="comment_aria_list_2">' + response.text + '</div>' +
            '<div class="comment_aria_list_3">' +
                '<i class="bi bi-hand-thumbs-up icon-font" title="いいね数">' + ' ' + '</i>' +
                '<label for="reply_aria_check_id" class="reply_aria_check_id">' + '返信' + '</label>' +
            '</div>' +
        '</div>';
    $('#comment_aria_list_reply_' + comment_id)[0].reset();
    $('#reply_count_' + comment_id).html(response.reply_count);
    $('#reply_aria_add').append(reply_aria_list_add);
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
})

$(document).on('click', '.edit_update_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
})

$('.edit_update').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const comment_id = $(this).attr('comment-id');
    const text = $('#comment_form_update_' + comment_id).val();
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_2_' + comment_id).html(response.text);
        console.log(response);
    })
    .fail(function(response) {
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
    const comment_id = $(this).attr('comment-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_' + comment_id).remove();
        $('#comment_count').html(response.comment_count);
        console.log(response);
    })
    .fail(function(response) {
        console.log(response);
    })
});
