<template>
  <div>
    <div class="panel">
      <h3>Working on EventLog {{ filter.id }}</h3>
      <button @click="submitFilter('filterOut')"> filter out </button>
      <input type="text" v-model="filter.activityName" placeholder="Activity" />
    </div>
    <div v-if="isEventLogReady" class="page">
      <table style="width: 100%;">
        <thead>
          <tr>
            <th v-for="(header, key) in eventLog.headers" v-bind:key="'header-' + key">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowKey) in eventLog.traces" v-bind:key="'row-' + rowKey">
            <td v-for="(column, columnKey) in eventLog.traces[rowKey]" v-bind:key="'row-' + rowKey + '-column-' + columnKey">
              {{ eventLog.traces[rowKey][columnKey] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="loader" v-else>
      <svg class="circular-loader" viewBox="25 25 50 50">
        <circle class="loader-path" cx="50" cy="50" r="20" fill="none" stroke="#70c542" stroke-width="2" />
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  props: ['selected'],
  components: {

  },
  data() {
    return {
      filter: {
        filterName: "",
        activityName: "",
        previousOperations: [],
        id: this.selected,
        
       
      },
      eventLog: {},
      array: [],
      isEventLogReady: false,
    }
  },
  methods: {
    submitFilter(filterName) {
      this.filter.filterName = filterName
      try {

        this.axios.post(this.$backend.filter(), this.filter)
          .then(() => {
            this.filter.activityName = "";
            this.filter.filterName = "";
            this.isEventLogReady = false;
            this.getEventLog();
            console.log("FILTER SUCCEEDED");
          })
      }
      catch (e) {
        console.log(e);
      }
    },
    getEventLog() {
      try {
        this.axios.get(this.$backend.getEventLog())
          .then((json) => {
            console.log(json.data)
            this.eventLog = json.data.eventLog;
            this.$emit('changeSelected', json.data.logId)
            this.filter.id = json.data.logId
            this.isEventLogReady = true;
            this.filter.previousOperations = json.data.history
            console.log("GET EVENTLOG SUCCESS");
          })
      }
      catch (e) {
        console.log(e);
      }
    },
  },
  mounted() {
    this.getEventLog();
    this.isEventLogReady = false
  }
}
</script>

<style>
.panel {
  width: 10%;
  border: 1px solid red;
  flex-direction: column;
  display: flex;

}
.page {
    width: 90%;
  display: flex;
  border: 1px solid red;

}
.profile-main-loader .loader {
  position: relative;
  margin: 0px auto;
  width: 200px;
  height: 200px;
}

.profile-main-loader .loader:before {
  content: '';
  display: block;
  padding-top: 100%;
}

.circular-loader {
  -webkit-animation: rotate 2s linear infinite;
  animation: rotate 2s linear infinite;
  height: 100%;
  -webkit-transform-origin: center center;
  -ms-transform-origin: center center;
  transform-origin: center center;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  margin: auto;
}

.loader-path {
  stroke-dasharray: 150, 200;
  stroke-dashoffset: -10;
  -webkit-animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
  animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
  stroke-linecap: round;
}

@-webkit-keyframes rotate {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes rotate {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@-webkit-keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }

  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }

  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}

@-webkit-keyframes color {
  0% {
    stroke: #70c542;
  }

  40% {
    stroke: #70c542;
  }

  66% {
    stroke: #70c542;
  }

  80%,
  90% {
    stroke: #70c542;
  }
}

@keyframes color {
  0% {
    stroke: #70c542;
  }

  40% {
    stroke: #70c542;
  }

  66% {
    stroke: #70c542;
  }

  80%,
  90% {
    stroke: #70c542;
  }
}
</style>