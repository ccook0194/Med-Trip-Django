
window.addEventListener("load", function() {
    (function($){
        $(document).ready(function() {
            $('.default-img').on("click", function () {
                $('.default-img').prop('checked', false);
                $(this).prop('checked', true);
            });
        })
    })(django.jQuery)
});
