let icon = $('#arrowIcon');

$('#toggleButton').click(function (){
    icon.removeClass('bi-chevron-compact-down').addClass('bi-chevron-compact-up');
})

$('#settingsModal').on('hidden.bs.modal', function (){
    icon.removeClass('bi-chevron-compact-up').addClass('bi-chevron-compact-down');
})
