// 検索タグの送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
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
