<template>
  <div class="frame">
      <h1 class="topmenu" >APPLICATION NAME</h1>
      <router-view />
    </div>
</template>

<script>
</script>

<style>
.frame{
  position: absolute;
  height: 100%;
  width: 100%;
  
}
.topmenu{
  margin: 0px;
  width: initial; 
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 8px;
  left: 0px; 
  right: 0px; 
  top: 0px;

  height: 50px;
  max-height: calc(100% - 0px); 
  
  color: #1cd48a;
  background-color: rgb(10, 48, 0); 
  display: flex;
  flex-direction:row; 
  align-items: center;

  }
</style>
