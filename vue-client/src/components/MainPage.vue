<template>
    <div class="parent">
        <div class="panel">
            <br>
            <button @click="goToGraphView" class="graphButton"></button>
            <br>
            <button @click="goToFilterView" class="filterButton"></button>

        </div>
        <router-view :selected="this.selected" @changeSelected="newSelected" class="page" />
    </div>
</template>

<script>
import router from '@/router';

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
        goToGraphView() {
            router.push("/app/graph");
        },
        goToFilterView() {
            router.push("/app/filter");
        }
    }
}
</script>

<style>
.parent {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;

}

.panel {
    width: 10%;
    background-color: blueviolet;
    flex-direction: column;
    display: flex;

}

.page {
    width: 90%;
    display: flex;

}

.graphButton {
    align-self: center center;
    margin-left: 20px;
    width: 90px;
    height: 90px;
    cursor: pointer;
    text-align: center;
    font-family: Open Sans;
    font-size: 18px;
    font-weight: 300;
    color: rgb(226, 226, 226);
    border-color: rgb(226, 226, 226);
    border-radius: 5px;
    background-image: url(..\\assets\\presentation.png);
    background-size: 88px;

}

.graphButton:hover {
    font-size: 20px;
    font-weight: 400;
    color: rgb(255, 255, 255);
}
.filterButton {
    align-self: center center;
    margin-left: 20px;
    width: 90px;
    height: 90px;
    cursor: pointer;
    text-align: center;
    font-family: Open Sans;
    font-size: 18px;
    font-weight: 300;
    color: rgb(226, 226, 226);
    border-radius: 5px;
    border-color: rgb(226, 226, 226);
    background-image: url(..\\assets\\filter.png);
    background-size: 88px;

}

.filterButton:hover {
    font-size: 20px;
    font-weight: 400;
    color: rgb(255, 255, 255);
}
</style>