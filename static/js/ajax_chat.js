$(window).on('load', function() {
    let pathname = $(location).attr('pathname');

    if(pathname) {
        let target = $(pathname).position();
        $('.edit_section_main').animate({scrollTop: target}, 'slow');
        $('.edit_section_main').scrollTop(target.top);
    }
});

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
            $('.followchange').removeClass('btn-success');
            $('.followchange').addClass('btn-danger');
            $('.btn-danger').html('解除する');
            $('.follower_count').html(response['follower_count']);
        } else {
            $('.followchange').removeClass('btn-danger');
            $('.followchange').addClass('btn-success');
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
$('#comment_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const id = $(this).attr('obj-id');
    const text = $('form [name=text]').val();
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        function scrollBottom(){
            let target = $('.chat_section_main_area').last();
            let position = target.position().top + $('.chat_section_main_area').scrollTop();
            $('.chat_section_main_area').animate({scrollTop: position}, 500, 'swing');
        }

        let comment_aria_list_add =
            '<div id="comment_aria_list_' + response.comment_id +'" class="comment_aria_list">' +
                '<a href="/userpage/' + response.nickname + '">' +
                    '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                '</a>' +
                '<div class="comment_aria_list_1">' +
                    '<p>' + response.nickname + '</p>' +
                    '<time>' + response.created + '</time>' +
                '</div>' +
                '<div id="comment_aria_list_2_' + response.comment_id + '" class="comment_aria_list_2">' + response.text + '</div>' +
                '<a href="/chat/detail/' + id + '/' + response.title + '/thread/' + response.comment_id + '" class="comment_aria_thread">' +
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
                                    '<p>' + response.nickname + '</p>' +
                                    '<time>' + response.created + '</time>' +
                                '</div>' +
                                '<div class="comment_aria_list_2">' + response.text + '</div>' +
                            '</div>' +
                        '</div>' +
                        '<form method="POST" action="/chat/detail/message/delete/' + response.comment_id + '" class="modal_content_footer">' +
                            '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light modal_cancel">' +
                            '<input type="button" name="delete" value="削除" comment-id="' + response.comment_id + '"  obj-id="' + id + '" class="btn btn-danger edit_delete">' +
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
        let obj = document.getElementById('comment_aria_add');
        obj.scrollTop = obj.scrollHeight;
        $('#comment_form')[0].reset();
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        $('#comment_aria_add').append(comment_aria_list_add);
        scrollBottom();
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});

// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#reply_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const id = $(this).attr('obj-id');
    const comment_id = $(this).attr('comment-id');
    const text = $('form [name=reply]').val();
    $.ajax({
        url: url,
        type: 'POST',
        data: {'id': id, 'text': text, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        let reply_aria_list_add =
            '<div id="comment_aria_list_' + comment_id + '" class="comment_aria_list">' +
                '<a href="/userpage/' + response.nickname +'">' +
                    '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                '</a>' +
                '<div class="comment_aria_list_1">' +
                    '<p>' + response.nickname + '</p>' +
                    '<time> ' + response.created + '</time>' +
                '</div>' +
                '<div id="comment_aria_list_2_' + comment_id + '" class="comment_aria_list_2">' + response.text + '</div>' +
                '<a href="/chat/detail/' + id + '/' + response.title + '/thread/' + comment_id + '" class="comment_aria_thread">' +
                    'スレッド表示' +
                    '<span id="reply_count_' + comment_id + '">返信 0 件</span>' +
                '</a>' +
                '{% if comment.author.id == user.id %}' +
                    '{% include "parts/modal_content_comment.html" %}' +
                '{% endif %}' +
            '</div>';
        let obj = document.getElementById('reply_aria_add');
        obj.scrollTop = obj.scrollHeight;
        $('#reply_form')[0].reset();
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        $('#reply_count_' + comment_id).html('返信 ' + response.reply_count + ' 件');
        $('#reply_aria_add').append(reply_aria_list_add);
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});

// メッセージ編集
$(document).on('click', '.edit_button_update', function() {
    const comment_id = $(this).attr('comment-id');
    // const $text = $('#comment_form_update_' + comment_id).val();
    // $text.replace($text, '\n').css('white-space', 'pre-wrap');

    // console.log($text)
    // const $textarea = $('.textarea_br');
    // const lineHeight = parseInt($text.css('white-space', 'pre-wrap'));

    // $text.on('input', function(evt) {
    //     const lines = ($(this).val() + '\n').match(/\n/g).length;
    //     $(this).height(lineHeight * lines);
    // });
    document.getElementById('edit_update_main_' + comment_id).classList.add('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.add('active');
})

$(document).on('click', '.edit_update_cancel', function() {
    const comment_id = $(this).attr('comment-id');
    document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
})

$('.edit_update_chat').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const comment_id = $(this).attr('comment-id');
    const text = $('#comment_form_update_' + comment_id).val();
    // const text =  $('form [name=text]').val();
    // const text = $('form [name=text]').val();
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
        $('#comment_aria_list_2_' + comment_id).html(response.text)
        console.log(response)
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
        $('#user_count').html(response.user_count);
        $('#comment_count').html(response.comment_count);
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});
