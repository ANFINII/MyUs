// 検索タグの作成ボタンの処理を定義
$(document).on('click', '.main_tag_2', function(event) {
    event.preventDefault();
    const url = $(this).closest('form').attr('action');
    const searchtag = $('form [name=searchtag]').val();
    $('#tag_form')[0].reset();
    document.querySelector('.main_tag_2').setAttribute('disabled', true);
    $.ajax({
        url: url,
        type: 'POST',
        data: {'searchtag': searchtag, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        document.querySelector('.main_tag_2').setAttribute('disabled', true);
        let searchtag_add =
            '<a class="tag_n_add" href="?search=' + response.searchtag + '">' + response.searchtag + '</a>'
        $('.tag_n_list').append(searchtag_add);
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
    })
    .fail(function(response) {
        console.log(response);
    })
});


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
            $('#like_count_object_' + id).html(response['total_like']);
        } else {
            $('.like_color').removeClass('bi-hand-thumbs-up-fill');
            $('.like_color').parent().removeClass('like_fill');
            $('.like_color').addClass('bi-hand-thumbs-up');
            $('.like_color').parent().addClass('like_no');
            $('#like_count_object_' + id).html(response['total_like']);
        }
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
    })
    .fail(function(response) {
        console.log(response);
    })
});
