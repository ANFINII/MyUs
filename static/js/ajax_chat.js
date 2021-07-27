$(window).on('load', function() {
    let pathname = $(location).attr('pathname');

    if(pathname) {
        let target = $(pathname).position();
        $('.chat_section_main').animate({scrollTop: target}, 'slow');
        $('.chat_section_main').scrollTop(target.top);
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
    const form = $(this);
    const url = form.attr('action');
    const id = form.attr('obj-id');
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
            '<div class="comment_aria_list">' +
                '<a href="/userpage/' + response.nickname + '">' +
                    '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                '</a>' +
                '<div class="comment_aria_list_1">' +
                    '<p>' + response.nickname + '</p>' +
                    '<time> ' + response.created + '</time>' +
                '</div>' +
                '<div class="comment_aria_list_2">' + response.text + '</div>' +
                '<a href="/chat/detail/' + response.pk + '/thread/' + response.comment_id + '" class="comment_aria_thread">' +
                    'スレッド表示' +
                    '<span>返信 0 件</span>' +
                '</a>' +
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
    const form = $(this);
    const url = form.attr('action');
    const id = form.attr('obj-id');
    const comment_id = form.attr('comment-id');
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
            '<div class="comment_aria_list">' +
                '<a href="/userpage/' + response.nickname +'">' +
                    '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                '</a>' +
                '<div class="comment_aria_list_1">' +
                    '<p>' + response.nickname + '</p>' +
                    '<time> ' + response.created + '</time>' +
                '</div>' +
                '<div class="comment_aria_list_2">' + response.text + '</div>' +
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
$('.chat_button_update').on('click', function() {
    const form = $(this);
    const comment_id = form.attr('obj-id');
    document.getElementById('chat_update_main_' + comment_id).classList.add('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.add('active');
})

$('.chat_update_cancel').on('click', function() {
    const form = $(this);
    const comment_id = form.attr('obj-id');
    document.getElementById('chat_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
})

$('.comment_form_update').submit(function(event) {
    event.preventDefault();
    const form = $(this);
    const url = form.attr('action');
    const comment_id = form.attr('obj-id');
    const text = $('#comment_form_update_' + comment_id).val();
    console.log(text)

    document.getElementById('chat_update_main_' + comment_id).classList.remove('active');
    document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_2_' + response.comment_id).html(response.text)
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});

// メッセージ削除ダイアログ
$('.chat_button_delete').on('click', function() {
    const form = $(this);
    const comment_id = form.attr('obj-id');
    document.getElementById('modal_content_' + comment_id).classList.add('active');
    document.getElementById('mask_' + comment_id).classList.add('active');
});

$('.modal_cancel').on('click', function() {
    const form = $(this);
    const comment_id = form.attr('obj-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
});

$('.chat_delete').on('click', function(event) {
    event.preventDefault();
    const form = $(this);
    const url = form.parent().attr('action');
    const comment_id = form.attr('obj-id');
    document.getElementById('modal_content_' + comment_id).classList.remove('active');
    document.getElementById('mask_' + comment_id).classList.remove('active');
    $.ajax({
        url: url,
        type: 'POST',
        data: {'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        $('#comment_aria_list_' + response.comment_id).remove();
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});
