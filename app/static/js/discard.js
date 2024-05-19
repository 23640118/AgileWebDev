$(document).ready(function() {
    $('.discard-btn').click(function() {
        // Accessing card rarity
        var rarity = $(this).closest('.discard-form').find('input[name="rarity"]').val();
        let money = 0;
        if (rarity == 'legendary')
                money = 500;
        else if (rarity == 'epic')
                money = 250;
        else if (rarity == 'rare')
            money = 100;
        else if (rarity == 'common')
            money = 50;

        // Confirming discard
        var confirmed = confirm('Are you sure you want to discard for ' + money + '?');
        if (confirmed) {
            var cardId = $(this).closest('.discard-form').find('input[name="card_id"]').val();
            $.ajax({
                url: '/discard-card',
                type: 'POST',
                data: { card_id: cardId},
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