// 検索タグの送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#tag_form').submit(function(event) {
    event.preventDefault();
    const url = $(this).attr('action');
    const searchtag = $('form [name=searchtag]').val();
    $.ajax({
        url: url,
        type: 'POST',
        data: {'searchtag': searchtag, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(response) {
        let searchtag_add =
            '<a class="tag_n_add" href="?search=' + response.searchtag + '">' + response.searchtag + '</a>'
        $('#tag_form')[0].reset();
        $('.tag_n_list').append(searchtag_add);
        console.log(response)
    })
    .fail(function(response) {
        console.log(response);
    })
});
