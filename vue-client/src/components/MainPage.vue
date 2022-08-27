<template>
    <div>
        <h3>Views</h3>
        <ol>
            <li><router-link :to="{ name: 'GraphView' }">Graph View</router-link></li>
            <li><router-link :to="{ name: 'FilterView' }">Filter View</router-link></li>
        </ol>
        <router-view :selected="this.selected"
        @changeSelected="newSelected"
        />
    </div>
</template>

<script>

export default{
    data(){
        return {
            selected: 0
        }
    },
    methods:{
        newSelected(id){
            this.selected = id
        },
    }
}
</script>