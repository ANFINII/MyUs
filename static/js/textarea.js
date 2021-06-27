$(function() {
    const target = $('.textarea');
    const rawTarget = target.get(0);
    let lineHeight = Number(target.attr('rows'));
    while (rawTarget.scrollHeight > rawTarget.offsetHeight) {
        lineHeight++;
        target.attr('rows', lineHeight);
    }
});

$(function() {
    const $textarea = $('.textarea');
    const lineHeight = parseInt($textarea.css('lineHeight'));
    $textarea.on('input', function(evt) {
        const lines = ($(this).val() + '\n').match(/\n/g).length;
        $(this).height(lineHeight * lines);
    });
});

$(function() {
    const target = $('.textarea_br');
    const rawTarget = target.get(0);
    let lineHeight = Number(target.attr('rows'));
    while (rawTarget.scrollHeight > rawTarget.offsetHeight) {
        lineHeight++;
        target.attr('rows', lineHeight);
    }
});

$(function() {
    const $textarea = $('.textarea_br');
    const lineHeight = parseInt($textarea.css('lineHeight'));
    $textarea.on('input', function(evt) {
        const lines = ($(this).val() + '\n').match(/\n/g).length;
        $(this).height(lineHeight * lines);
    });
});
