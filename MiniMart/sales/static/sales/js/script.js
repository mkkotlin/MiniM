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
        console.log('edit')
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