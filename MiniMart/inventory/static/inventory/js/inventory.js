$(document).ready(function () {
    //strat of hide and show
    $('#add_product').click(function (e){
    $('#add_p_form').slideToggle(); //hide and show

    const text = $(this).text();
    $(this).text(text === '➕Add Items'? '➖Hide Form':'➕Add Items')
    });
    //end of hide and show

    // start of form submit
    $('#submit').click(function (e){
        e.preventDefault();


            let isValid = true;

        // Loop through all input fields inside the form
        $("#form_data :input[required]").each(function () {
        if (!$(this).val().trim()) {
            isValid = false;
            $(this).css("border", "1px solid red"); // Optional: visual cue
        } else {
            $(this).css("border", ""); // Reset if filled
        }
        });

        if (!isValid) {
        alert("Please fill in all required fields.");
        return;
        }
        
        $.ajax({
            type: 'POST',
            url: "/inventory/add/",
            data:$('#form_data').serialize(),  //direct data from form
            success: function(response){
                alert(response.success)
                $('.add_update').prepend(response.row_html) //prepend to add new row at the top
                $("#form_data")[0].reset(); //reset field to none
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);  //to read message
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState) //to read status and cycle of ajax
            }
        })
    });
     // end of form submit


    // start of delete button
        $(document).on('click','.delete-btn',function(e){
        e.preventDefault(); // Prevent default action of the button
        const pId = $(this).data('id')
        if (!confirm('Are you sure you want to delete this item?')) {
            return; // Exit if user cancels
        }
        // delete url request
        $.ajax({
            type: 'POST',
            url: `/inventory/delete/${pId}/`,
            headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
            alert(response.success || 'Item deleted successfully');
            // Remove the row of the deleted product
            $(`#delete-${pId}`).closest('tr').remove();   //close the row of the deleted product closest() it finds the row that contains the button 
            },
            error: function(xhr) {
            const err = JSON.parse(xhr.responseText);
            alert(err.message || 'Failed to delete item');
            }
        });
    })
    // start of delete button
});

