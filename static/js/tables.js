$(document).ready(function() {
    $('#userTable').DataTable({
        pageLength: 10,
        ordering: true,
        responsive: true,
        columnDefs: [
            {
                targets: -1,  // Last column (Actions)
                orderable: false  // Disable sorting for Actions column
            }
        ]
    });
});
