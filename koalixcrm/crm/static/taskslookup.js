<script charset="utf-8" type="text/javascript">
  $(function(){
    $("select#id_project").change(function(){
      $.getJSON("/tasks/",{id: $(this).val(), view: 'json'}, function(tasks) {
        var options = '<option value="">--------&nbsp;</option>';
        for (var i = 0; i < tasks.length; i++) {
          options += '<option value="' + tasks[i].optionValue + '">' + tasks[i].optionDisplay + '</option>';
        }
        $("#id_item").html(options);
        $("#id_item option:first").attr('selected', 'selected');
      })
      $("#id_project").attr('selected', 'selected');
    })
  })
</script>