<template>
    <div>
        <h3>Views</h3>
        <ol>
            <li><router-link :to="{ name: 'GraphView' }">Graph View</router-link></li>
            <li><router-link :to="{ name: 'FilterView' }">Filter View</router-link></li>
        </ol>
        <router-view/>
    </div>
</template>

<script>
</script>