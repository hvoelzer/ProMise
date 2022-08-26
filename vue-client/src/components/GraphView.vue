<template>
    <div>
        <h1> I am the Graph View</h1>
        <CleanGraph :edges="this.edges"/>
    </div>
</template>

<script>
import CleanGraph from './CleanGraph.vue';
export default {
  name: 'App',
  components: {
    CleanGraph
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