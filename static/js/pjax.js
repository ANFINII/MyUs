// Pjax処理
let object_dict = {};
history.replaceState(null, null, location.href);

function pjax_dict(href) {
    const obj = document.querySelector('.main_contents').innerHTML;
    object_dict[href] = obj;
    history.pushState(null, null, href);
}

// サイドボタンを押した時の処理
$(document).on('click', '.pjax_button', function(event) {
    event.preventDefault();
    const url = $(this).attr('path');
    const href = $(this).attr('href');
    $.ajax({
        url: url,
        type: 'GET',
        data: {'href': href, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        dataType: 'json',
    })
    .done(function(response) {
        pjax_dict(href)
        window.addEventListener('popstate', e => {
            const back_url = location.pathname;
            const back_obj = object_dict[back_url];
            $('.main_contents').html(back_obj);
        });
        $('.main_contents').html(response.html);
    })
    .fail(function(response) {
        console.log(response);
    })
});
