<!--JavaScript Start-->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
 $('.dataframe').DataTable( {
     scrollX: true,
     lengthMenu: [[10, 25, 50, 100, 200, -1], [10, 25, 50, 100, 200, "All"]],
     initComplete: function () {
       this.api().columns().every( function () {
         var column = this;
         var select = $('<select><option value=""></option></select>')
           .appendTo( $(column.header()))
           .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                   $(this).val()
               );

               column
                   .search( val ? '^'+val+'$' : '', true, false )
                   .draw();
           });
           column.cells('', column[0]).render('display').sort().unique().each( function ( d, j ) {
             if(column.search() === '^'+d+'$'){
                 select.append( '<option value="'+d+'" selected="selected">'+d+'</option>' )
             }
             else {
                 select.append( '<option value="'+d+'">'+d+'</option>' )
             }
           });
       });
     }
 });
});
</script>
<!--JavaScript End-->
