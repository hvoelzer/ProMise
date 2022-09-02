<template>
    <div class="parent">
        <div class="panel">
            <ol>
                <li>
                    <router-link :to="{ name: 'GraphView' }">Graph View</router-link>
                </li>
                <li>
                    <router-link :to="{ name: 'FilterView' }">Filter View</router-link>
                </li>
            </ol>
        </div>
        <router-view :selected="this.selected" @changeSelected="newSelected" class="page"/>
    </div>
</template>

<script>

export default {
    data() {
        return {
            selected: 0
        }
    },
    methods: {
        newSelected(id) {
            this.selected = id
        },
    }
}
</script>

<style>
.parent {
  height: 100%;
  width: 100%;
  border: 1px solid red;
  display: flex;
  flex-direction: row;

}
.panel {
  width: 10%;
  border: 1px solid red;
  display: flex;

}
.page {
    width: 90%;
  display: flex;
  border: 1px solid red;

}
</style>