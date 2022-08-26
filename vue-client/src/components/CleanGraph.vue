<template>
    <div>
        <h3> I am the Clean Graph View</h3>
        <h4> HERE {{edges.data}} HERE</h4>
        <svg viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="5"/>
        </svg>
    </div>
</template>

<script>
export default{
    name: 'CleanGraph',
    props: ['edges'],

    mounted(){
    }
}
</script>