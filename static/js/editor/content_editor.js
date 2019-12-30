$('#done').on('click', function () {
    $('.cover').addClass('active');
    $("body").css("overflow", "hidden");
    $('.done-modal').addClass('active');
})

$('#back-button').on('click', function () {
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

$("#content-editor-form").submit(function () {
    const allInputs = $(".fr-element.fr-view")[0].innerHTML + $(".description-input")[0].innerHTML + $(".title-input")[0].innerHTML
    if (allInputs.includes('\\') || allInputs.includes('|')) {
        alert(`You can’t use the following characters (\\, |) because these characters are reserved for the system. Please remove these characters and try again.`)
        return false
    }
    const btn = $(this).find(".btn:focus")[0].name
    const published = $(".published-at").length > 0
    if (btn == 'save' && published) {
        return confirm(`Your post has already been published. Would you like to revert it to draft?`)
    } else if (btn == 'view' && published) {
        return confirm(`Your post has already been published. Viewing your post will automatically publish any new changes to your post. Would you like to continue?`)
    }
    return true
})

// category
$(document).keypress(function (event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13' && $("#category-input").is(":focus") && $("#category-input").val().length > 0) {
        event.preventDefault();
        let categoryInput = $("#category-input").val().trim();
        const html = `
        <div class="category-tag">
            <input class="category" name="category" value="${categoryInput}" readonly>
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
