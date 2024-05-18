$(document).ready(function() {
    $('.trade-btn').click(function() {
        var confirmed = confirm('Are you sure you want to trade?');
        if (confirmed) {
            var postId = $(this).closest('.trade-form').find('input[name="post_id"]').val();
            $.ajax({
                url: '/update-post',
                type: 'POST',
                data: { post_id: postId},
                success: function(response) {
                    alert(response)
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    alert(xhr.responseText)
                }
            });
        }
    });
});