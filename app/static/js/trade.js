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
                    alert(response);
                    console.log("yes")
                    // Refresh the page when successful to remove the trade button.
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    console.log("no")
                    alert(xhr.responseText);
                }
            });
        }
    });
});