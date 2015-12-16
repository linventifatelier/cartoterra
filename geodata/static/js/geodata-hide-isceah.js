$('.geodata-toggle-isceah').change( function () {
    if ($(this).is(':checked')) {
        $('.geodata-isceah').closest('fieldset').removeClass('geodata-isceah-fieldset');
    } else {
        $('.geodata-isceah').closest('fieldset').addClass('geodata-isceah-fieldset');
    };
});
