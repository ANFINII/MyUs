// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$("form").submit(function (event) {
    event.preventDefault();
    let form = $(this);
    $.ajax({
        url: form.prop("action"),
        method: form.prop("method"),
        data: form.serialize(),
        timeout: 1000,
        dataType: "json",
    })
    .done(function (data) {
        $(".comment_aria").append("<p>" + data + "</p>");
    })
});