$(document).ready(function () {
    console.log('jQuery');
    $('#add_product').click(function (e){
    $('#add_p_form').slideToggle();

    const text = $(this).text();
    $(this).text(text === '➕Add Items'? '➖Hide Form':'➕Add Items')
    });

    
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
            data:$('#form_data').serialize(),
            success: function(response){
                alert(response.success)
                $("#form_data")[0].reset();
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState)
            }
        })
    });
});