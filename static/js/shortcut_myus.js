// textareaのdisabled判定
// commentショートカット
$(document).on('focus', '#comment_form_area', function(event) {
    event.preventDefault();

    // focus時にそれ以外のtextareaを無効化する
    const targetElem = document.querySelectorAll('.form_button');
    const targetCount = targetElem.length;
    if (targetElem) {
        for (let i = 0; i < targetCount; i++)
        targetElem[i].setAttribute('disabled', true);
    }

    const text = $(this).val();
    if (text || text.match(/\S/g)) {
        // disabled属性を削除
        document.getElementById('comment_form_button').removeAttribute('disabled');
    }

    $(document).on('input', '#comment_form_area', function(event) {
        event.preventDefault();
        const text = $(this).val();
        if (!text || !text.match(/\S/g)) {
            // disabled属性を設定
            document.getElementById('comment_form_button').setAttribute('disabled', true);
        } else {
            // disabled属性を削除
            document.getElementById('comment_form_button').removeAttribute('disabled');

            // ショートカット
            shortcut.add('Ctrl+Enter', function() {
                $('#comment_form_button').click();
            });
            shortcut.add('meta+Enter', function() {
                $('#comment_form_button').click();
            });
        }
    });
});

// updateショートカット
$(document).on('focus', '.update_form_area', function(event) {
    event.preventDefault();
    const comment_id = $(this).attr('comment-id');

    // focus時にそれ以外のtextareaを無効化する
    const targetElem = document.querySelectorAll('.form_button');
    const targetCount = targetElem.length;
    if (targetElem) {
        for (let i = 0; i < targetCount; i++)
        targetElem[i].setAttribute('disabled', true);
    }

    const text = $(this).val();
    if (text || text.match(/\S/g)) {
        // disabled属性を削除
        document.getElementById('update_form_button_' + comment_id).removeAttribute('disabled');
    }

    // ショートカット
    shortcut.add('Ctrl+Enter', function() {
        $('#update_form_button_' + comment_id).click();
    });
    shortcut.add('meta+Enter', function() {
        $('#update_form_button_' + comment_id).click();
    });

    $(document).on('input', '#comment_form_update_' + comment_id, function(event) {
        event.preventDefault();
        const text = $(this).val();
        if (!text || !text.match(/\S/g)) {
            // disabled属性を設定
            document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
        } else {
            // disabled属性を削除
            document.getElementById('update_form_button_' + comment_id).removeAttribute('disabled');

            // ショートカット
            shortcut.add('Ctrl+Enter', function() {
                $('#update_form_button_' + comment_id).click();
            });
            shortcut.add('meta+Enter', function() {
                $('#update_form_button_' + comment_id).click();
            });
        }
    });
});
