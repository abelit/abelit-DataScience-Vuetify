<template>
  <div class="demo">
    <datepicker :readonly="true" format="YYYY-MM-DD" name="date1"></datepicker>
    <datepicker value="2018-9-5" format="YYYY-M-D" name="date2"></datepicker>
    <datepicker :readonly="true" format="MMM/D/YYYY" name="date3"></datepicker>
  </div>
</template>

<script>
import datepicker from 'vue-date-picker'

export default {
  name: 'DatePicker',
  components: {
    datepicker
  }
}
</script>
