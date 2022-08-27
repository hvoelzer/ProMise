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
        <table style="width: 100%;">
            <thead>
                <tr>
                    <th v-for = "(header, key) in eventLog.headers"
                        v-bind:key = "'header-' + key">
                        {{ header }}
                    </th>
                </tr>
            </thead>
            <tbody>
                
            </tbody>
        </table>
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
            },
        eventLog: {}
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
          this.getEventLog();
          console.log("FILTER SUCCEEDED");
        })
      }
      catch (e) {
        console.log(e);
      }
    },
    getEventLog(){
        try {
            this.axios.get(this.$backend.getEventLog())
            .then((json) => {
            
                this.eventLog = json.data.eventLog;
                this.$emit('changeSelected', this.eventLog.logId)
                this.filter.id = this.eventLog.logId
                console.log(this.eventLog.headers)
                console.log("GET EVENTLOG SUCCESS");
            })
        }
        catch (e) {
            console.log(e);
        }
    }
  },
  mounted(){
    this.getEventLog();
  }
}
</script>
