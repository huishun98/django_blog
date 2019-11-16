$('#done').on('click', function () {
    $('.cover').addClass('active');
    $("body").css("overflow", "hidden");
    $('.done-modal').addClass('active');
})
$('#back-button').on('click', function () {
    // plus save functions,
    $('.cover').removeClass('active');
    $("body").css("overflow", "auto");
    $('.done-modal').removeClass('active');
})
$(".title-input").change(function (event) {
    $(".title-input").val(event['target'].value)
})
$(".description-input").change(function (event) {
    $(".description-input").text(event['target'].value)
})

// category
$(document).keypress(function (event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13' && $("#category-input").is(":focus") && $("#category-input").val().length > 0) {
        event.preventDefault();
        let categoryInput = $("#category-input").val().trim();
        const html = `
        <div class="category-tag">
            <input class="category" name="category" value="${categoryInput}">
            <a class="link remove-category" href="javascript:void(0)">x</a>
        </div>
        `
        $(".category-tags").append(html);
        $("#category-input").val('');
    } else if (keycode == '13') {
        event.preventDefault();
    }
});
$(document).on('click', '.remove-category', function () {
    $(this).parent().remove()
})


new FroalaEditor('#edit', {
    heightMin: 400,
    fileUploadURL: '/upload_file',
    fileUploadParams: {
        id: 'my_editor',
        csrfmiddlewaretoken: getCookie('csrftoken')
    },
    imageUploadURL: '/upload_image',
    imageUploadParams: {
        id: 'my_editor',
        csrfmiddlewaretoken: getCookie('csrftoken')
    },
    videoUploadURL: '/upload_video',
    videoUploadParams: {
        id: 'my_editor',
        csrfmiddlewaretoken: getCookie('csrftoken')
    },
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
