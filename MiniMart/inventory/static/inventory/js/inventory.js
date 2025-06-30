  $(document).ready(function () {
    console.log('jQuery');
    $('#add_product').click(function (e){
        $('#add_p_form').slideToggle();

        const text = $(this).text();
        console.log(text);
        $(this).text(text === '➕Add Items'? '➖Hide Form':'➕Add Items')
    })
  });

console.log('js')