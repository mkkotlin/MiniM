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
                $('#sale_form')[0].reset();
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState)
            },
        });
    });
});