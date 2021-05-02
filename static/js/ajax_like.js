// いいねボタンクリック時の処理を定義
$(document).ready(function() {
    $(document).on('click', '.like_form', function(event) {
        event.preventDefault();
        const pk = $(this).attr('value');
        const url = $(this).parent().attr('action');
        $.ajax({
            url: url,
            type: 'POST',
            data: {'id': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
        })
        .done(function(response) {
            if (response['liked']) {
                $('.like_color').removeClass('bi-hand-thumbs-up');
                $('.like_color').parent().removeClass('like_no');
                $('.like_color').addClass('bi-hand-thumbs-up-fill')
                $('.like_color').parent().addClass('like_fill');
                $('.like_count').html(response['total_like'])
            } else {
                $('.like_color').removeClass('bi-hand-thumbs-up-fill');
                $('.like_color').parent().removeClass('like_fill');
                $('.like_color').addClass('bi-hand-thumbs-up');
                $('.like_color').parent().addClass('like_no');
                $('.like_count').html(response['total_like'])
            }
            console.log(response)
        })
        .fail(function(response) {
            console.log(response);
        })
    });
});