<template>
    <div>
        <h1>Filter View</h1>
        <h3>Working on EventLog {{filter.id}}</h3>
        <button @click = "submitFilter('filterOut')"> filter out </button>
        <input
          type="text"
          v-model="filter.activityName"
          placeholder="Activity"
        />
    </div>
</template>

<script>export default {
  name: 'App',
  props: ['selected'],
  components: {

  },
  data(){
    return {
        filter:{
            filterName: "",
            activityName: "",
            previousOperations: [], 
            id: this.selected
            }
    }
  },
  methods: {
    submitFilter(filterName){
        this.filter.filterName = filterName
      try {

        this.axios.post(this.$backend.filter(), this.filter)
        .then(() => {
          this.filter.activityName = "";
          this.filter.filterName = "";
          console.log("SUCCESS"); 
        })
      }
      catch (e) {
        console.log(e);
      }
    },
    getEventLog(){
        
    }
  },
}
</script>
