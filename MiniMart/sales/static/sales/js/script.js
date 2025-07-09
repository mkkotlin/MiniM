$(document).ready(function(){
    $('#add_sale_toggle').click(function(){
        $('.add_sale_form').slideToggle()
        const text = $(this).text()
        $(this).text(text === '➕ Add Sale'? '➖Hide Form':'➕ Add Sale')
    });

    $('#submit').click(function(e){
        e.preventDefault();


        $.ajax({
            type:'POST',
            url:'/sales/add_sale/',
            data:$('#sale_form').serialize(),
            success: function(response){
                alert(response.message || 'Sale added successfully!');
                $('.add_sale_list').prepend(response.row)
                $('#sale_form')[0].reset();
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState)
            },
        });
    });

    $(document).on('click', '.edit-btn', function(e){
        e.preventDefault();

        // Get the ID of the sale item to edit
        let id = $(this).data('id');
        let row = $(`#edit-${id}`).closest('tr');

        // Store the original HTML of the row to revert back later
        // This is necessary to restore the row if the user cancels the edit
        const originalHTML = row.html();
        row.data('original-html', originalHTML);

        let product = row.find('.product').text();
        let quantity = parseInt(row.find('.quantity').text());
        let price = parseFloat(row.find('.sale_price').text());

        row.find('.product').text(product); // Ensure product name is set correctly
        row.find('.quantity').html(`<input type="number" name="quantity" value="${quantity}" required>`);
        row.find('.sale_price').html(`<input type="number" name="price" value="${price.toFixed(2)}" step="0.01" required>`);
        row.find('.action').html(`<button class="save-btn" data-id="${id}">Save</button> <button class="cancel-btn" data-id="${id}">Cancel</button>`);
    });

    $(document).on('click', '.cancel-btn', function(e){
        e.preventDefault();
        // Restore the original HTML of the row
        // This will revert the row back to its original state before editing

        const row = $(this).closest('tr');
        const originalHTML = row.data('original-html');

        if (originalHTML) {
            row.html(originalHTML); 
        }
    });

    // --- Save Button ---
    $(document).on('click', '.save-btn', function(e){
        e.preventDefault();
        // Get the ID of the sale item to save
        
        let id = $(this).data('id');
        // The previous code used $(`#edit-${id}`).closest('tr'), but after editing, the row's structure may change,
        // and the input fields may not be found as expected, resulting in undefined and NaN values.
        // Instead, use $(this).closest('tr') to reliably get the row and its input values.
        let row = $(this).closest('tr');
        let quantity = parseInt(row.find('input[name="quantity"]').val());
        let price = parseFloat(row.find('input[name="price"]').val());
        console.log(`Saving sale with ID: ${id}, Quantity: ${quantity}, Price: ${price}`);

        $.ajax({
            type: 'POST',
            url:`/sales/edit/${id}/`,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data:{
                id: id,
                quantity: quantity,
                price: price
            },
            success:function(response){
                alert(response.message || 'Sale updated successfully!');
                // Update the row with the new values
                row.find('.quantity').text(quantity);
                row.find('.sale_price').text(price.toFixed(2));
                row.find('.action').html(`<button class="edit-btn" id="edit-${id}" data-id="${id}">Edit</button> <button class="delete-btn" id="delete-${id}" data-id="${id}">Delete</button>`);
            },
            error:function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Failed to update sale');
            }
        });
    });



    $(document).on('click', '.delete-btn', function(e){
        e.preventDefault();
         if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }
        const id = $(this).data('id')
        
        $.ajax({
            type: 'POST',
            url:`/sales/delete/${id}/`,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response){
                alert(response.message)
                $(`#delete-${id}`).closest('tr').remove();
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Failed to delete item');
            }
        });

    });
});