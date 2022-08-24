<template>
    <div>
        <h1> I am the Graph View</h1>
        
    </div>
</template>

<script>
export default {
  name: 'App',
  components: {

  },
  data(){
    return{
        edges: {}
    }
  },
  methods: {
    getGraph(){
        try {
            this.axios.get(this.$backend.getGraph())
            .then((json) => {
            this.edges = json;
            console.log("SUCCESS");
            console.log(json.data);
            })
        }
        catch (e) {
            console.log(e);
        }
    },
  },
  mounted(){
    this.getGraph();
  }

}
</script>