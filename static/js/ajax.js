// $(document).ready(function(event){
//     $(document).on('click', '.like_form', function(event){
//         event.preventDefault();
//         let video_id = $(this).attr('value');
//         $.ajax({
//         type: "POST",
//         url: "{% url 'video_like' object.id %}",
//         data: {'video_id': video_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: "json",
//         success: function(response){
//             $('.like_form').html(response['form'])
//             console.log($('.like_form').html(response['form']));
//         },
//         error: function(rs, e){
//         console.log(rs.responseText);
//         }
//         });
//     });
// });

// いいねボタンクリック時の処理を定義
$(document).ready(function(event){
    $(document).on('click', '.like_form', function(event){
        event.preventDefault();
        let video_id = $(this).attr('value');
        $.ajax({
        type: "POST",
        url: "{% url 'video_like' object.id %}",
        data: {'video_id': video_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: "json",
        success: function(data) { 
            $('.like_form').like_fill('fas fa-thumbs-up icon-font'); 
            $('.like_form').like('btn btn-success btn-lg'); 
        },
        error: function(rs, e){
            console.log(rs.responseText);
        }
        });
    });
});

// $('.like_form').click(function (event) {
//     event.preventDefault();
//     let video_id = $(this).attr('value');
//     $.ajax({
//         url: "{% url 'video_like' object.id %}",
//         method: 'POST',
//         timeout: 10000,
//         data: {'video_id': video_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//         dataType: "json",
//     })
//     .done(function(data) {
//         $('.like_form').responseText('fas fa-thumbs-up icon-font');
//         $('.like_form').responseText('btn btn-success btn-lg');
//     })
//     .fail(function (data) {
//         alert("fail");
//     })
// });

// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$("form").submit(function (event) {
    event.preventDefault();
    let form = $(this);
    $.ajax({
        url: form.prop("action"),
        method: form.prop("method"),
        data: form.serialize(),
        timeout: 100,
        dataType: "text",
    })
    .done(function (data) {
        $(".comment_aria").append("<p>" + data + "</p>");
    })
});