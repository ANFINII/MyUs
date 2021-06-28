$(document).ready(function() {
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

    // Commentクリック時の処理を定義
    $('.click_id').on('click', function(event) {
    //     event.preventDefault();
        const url = $(this).attr('action');
        const form_id = $(this).attr('form-id');
        const check_id = $(this).children('label').attr('for');
        const comment_aria_check_id_1 = document.getElementsByClassName('get-id-1')[0];
        const comment_aria_check_id_2 = document.getElementsByClassName('get-id-2')[0];
        comment_aria_check_id_1.setAttribute('id', check_id);
        comment_aria_check_id_2.setAttribute('for', check_id);
        $.ajax({
            url: url,
            type: 'POST',
            data: {'form_id': form_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
        })
        .done(function(response) {
            console.log(response)
        })
        .fail(function(response) {
            console.log(response);
        })
    });

    // 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
    $('form').submit(function(event) {
        event.preventDefault();
        const form = $(this);
        const url = form.attr('action');
        const id = form.attr('obj-id');
        const text = $('form [name=text]').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: {'id':id, 'text':text, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
            timeout: 10000,
        })
        .done(function(response) {
            let comment_aria_list_add =
                '<label for="comment_aria_check_id" class="comment_aria_list">' +
                    '<a href="/userpage/' + response.nickname +'">' +
                        '<img src="' + response.user_image +'" title="' + response.nickname + '" class="profile_image_comment">' +
                    '</a>' +
                    '<div class="comment_aria_list_1">' +
                        '<p>' + response.nickname + '</p>' +
                        '<time>' + ' ' + response.created + '</time>' +
                    '</div>' +
                    '<div class="comment_aria_list_2">' + response.text + '</div>' +
                '</label>';
            let obj = document.getElementById('comment_aria_add');
            obj.scrollTop = obj.scrollHeight;
            $('#comment_form')[0].reset();
            $('#user_count').html(response.user_count);
            $('#comment_count').html(response.comment_count);
            $('#comment_aria_add').append(comment_aria_list_add);
            console.log(response)
        })
        .fail(function(response) {
            console.log(response);
        })
    });
});
