 function handleFiles(files) {
      // Check for the various File API support.
       var form_data = new FormData(files[0])

    $.ajax({
  type: "POST",
  url: '/hello',
  data: form_data,
  success: null,
  dataType: 'csv'
});
    }