function confirmModal(title, body, callback) {
    $('#confirmModalTitle').text(title);
    $('#confirmModalContents').text(body);
    $('#confirmModal').modal('show');
    $('#confirmButton').off('click').click(function() {
        callback(true);
    });
    $('#cancelButton').off('click').click(function() {
        callback(false);
    });
}

$('#dialogModal').on('hidden.bs.modal', function () {
    location.reload();
});


$(document).ready(function() {
    $('.trade-btn').click(function() {
        var self = this;
        confirmModal('Confirmation', 'Are you sure you want to trade?', function(confirmed) {
            if (confirmed) { 
                var postId = $(self).closest('.trade-form').find('input[name="post_id"]').val();
                console.log("Confirmed")
                $.ajax({
                    url: '/update-post',
                    type: 'POST',
                    data: { post_id: postId},
                    success: function(response) {
                        document.getElementById('modalTitle').innerHTML = "Trade Successed!";
                        document.getElementById('modalContents').innerHTML = response;
                    },
                    error: function(xhr, status, error) {
                        console.error(xhr.responseText);
                        document.getElementById('modalTitle').innerHTML = "Trade Failed";
                        document.getElementById('modalContents').innerHTML = xhr.responseText;
                    }
                });
                $('#dialogModal').modal('show');
            }
            else{
                console.log("canceled")
            }
        })
    });
});


$(document).ready(function() {
    $('.delete-btn').click(function() {
        var self = this;
        confirmModal('Confirmation', 'Are you sure you want to delete this post?', function(confirmed) {
            if (confirmed) { 
                var postId = $(self).closest('.delete-form').find('input[name="post_id"]').val();
                console.log("Confirmed")
                $.ajax({
                    url: '/delete-post',
                    type: 'POST',
                    data: { post_id: postId},
                    success: function(response) {
                        document.getElementById('modalTitle').innerHTML = "Post Deleted!"
                        document.getElementById('modalContents').innerHTML = response;
                    },
                    error: function(xhr, status, error) {
                        console.error(xhr.responseText);
                        document.getElementById('modalTitle').innerHTML = "Error"
                        document.getElementById('modalContents').innerHTML = xhr.responseText;
                    }
                });
                $('#dialogModal').modal('show');
            }
        });
    });
});

