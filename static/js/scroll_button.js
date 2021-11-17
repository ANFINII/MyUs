//ボタンを押すと右に0.2秒かけて500px移動
$(document).on('click', '.main_tag_right', function() {
    $('.main_tag_n').animate({
        scrollLeft: $('.main_tag_n').scrollLeft() + 300,
    }, 200)
    return false
})

//ボタンを押すと左に0.2秒かけて500px移動
$(document).on('click', '.main_tag_left', function() {
    $('.main_tag_n').animate({
        scrollLeft: $('.main_tag_n').scrollLeft() - 300,
    }, 200)
    return false
})
