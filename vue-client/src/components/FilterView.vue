<template>
    <div>
        <h1> I am the Filter View</h1>
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
  components: {

  },
  data(){
    return {
        filter:{
            filterName: "",
            activityName: "",
            previousOperations: [], 
            id: 0
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
          this.$emit('newFilter')
        })
      }
      catch (e) {
        console.log(e);
      }
    }
  },
}
</script>
