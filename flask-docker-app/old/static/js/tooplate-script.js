function calculateHeight(img, originalWidth, originalHeight) {
    const minHeight = 400;
    let imgHeight = img.width() * originalHeight / originalWidth;
    imgHeight = imgHeight < minHeight ? minHeight : imgHeight;
    return imgHeight;
}

function resizeParallaxes() {
    const parallax1 = $('#parallax-1');
    const parallax2 = $('#parallax-2');
    const newHeight1 = calculateHeight(parallax1, 1800, 690);
    const newHeight2 = calculateHeight(parallax2, 1800, 590);
    parallax1.css('min-height', newHeight1 + 'px');
    parallax2.css('min-height', newHeight2 + 'px');
}

$(document).ready(function () {
    resizeParallaxes();

    $(window).resize(function () {
        resizeParallaxes();
    });
});