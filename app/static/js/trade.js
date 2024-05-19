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
                    // Refresh the page when successful to remove the trade button.
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    alert(xhr.responseText);
                }
            });
        }
    });
});


$(document).ready(function() {
    $('.delete-btn').click(function() {
        var confirmed = confirm('Are you sure you want to delete this post?');
        if (confirmed) {
            var postId = $(this).closest('.delete-form').find('input[name="post_id"]').val();
            $.ajax({
                url: '/delete-post',
                type: 'POST',
                data: { post_id: postId},
                success: function(response) {
                    alert(response);
                    // Refresh the page when successful to remove the trade button.
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    alert(xhr.responseText);
                }
            });
        }
    });
});

