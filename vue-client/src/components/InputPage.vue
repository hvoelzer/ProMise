<template>
  <div class="centerInput">
    <h1>IMPORT RAW EVENTLOG </h1>
    <form v-on:submit.prevent="submitForm">
      <table>
        <tr>
          <td><label> CSV File </label></td>
          <td><input type="file" accept=".csv" @change="handleFileUpload( $event )" /></td>
        </tr>

        <tr>
          <label> Timestamp formatting String </label>
          <td><input type="text" v-model="form.timestampformat" placeholder="H:M:S" /></td>
          <td>
            <input type="button" onclick="location.href='https://pynative.com/python-datetime-format-strftime/#:~:text=Use%20datetime.,hh%3Amm%3Ass%20format.';" value="How to set timestamp string" />
          </td>
        </tr>
        <tr>
          <label> Timestamp Column </label>
          <td><input type="number" v-model="form.timestampcolumn" /></td>
          <td>All indexes start from 0. E.g. if the second column in you log holds timestamps, use index 1.</td>
        </tr>
        <tr>
          <label> Activity Column </label>
          <td><input type="number" v-model="form.activitycolumn" /></td>
        </tr>
        <tr>
          <label> Trace Column </label>
          <td><input type="number" v-model="form.tracecolumn" /></td>
        </tr>
        <tr>
          <label> True Data Graph </label>
          <td><input type="checkbox"  v-model="form.truedatagraph" />
            <label for="checkbox">{{ form.
            truedatagraph }}</label>
          </td>
          <td>We are using an abstraction layer to determine whether two logs are equal. If you want to see if logs are equal without abstraction, tick this box.</td>
        </tr>
        <label> </label>
        <td><button type="submit">Submit</button></td>
      </table>
    </form>

  </div>
</template>

<script>
import router from '@/router';
import Papa from 'papaparse';


export default {
  name: 'App',
  components: {

  },
  data() {
    return {
      form: {
        truedatagraph: false,
        timestampformat: "%Y-%m-%dT%H:%M:%S",
        tracecolumn: 0,
        activitycolumn: 2,
        timestampcolumn: 1,
        file: "",
        content: [],
        parsed: false
      }
    }
  },
  methods: {
    
    parseFile() {
      Papa.parse(this.form.file, {
        header: true,
        skipEmptyLines: true,
        complete: function (results) {
          this.form.content = results;
          this.form.parsed = true;
        }.bind(this)
      });
    },
    handleFileUpload(event) {
      this.form.file = event.target.files[0];
      this.parseFile();
      console.log("FILE PARSED");
      setTimeout(function () { this.submitForm() }.bind(this), 30000)
    },
    submitForm() {
      try {
        console.log(this.form.file)
        this.axios.post(this.$backend.getUrlData(), this.form, { headers: { "Access-Control-Allow-Origin": "http://127.0.0.1:5000"} })
          .then(() => {
            
            console.log("IMPORT SUCCEEDED");
            router.push({name:"GraphView", params: { truedatagraph: this.form.truedatagraph}});
          })
          .catch((reason) => {
            if (reason.response.status === 402) {
              alert("Timestamp or Timestamp column wrong")
            } else {
              alert("Something went wrong")
            }
          })
      }
      catch (e) {
        console.log(e);
      }
    }
  },
}
</script>

<style>
.centerInput {
  margin: 0px;
  width: initial;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 8px;

  max-height: calc(100% - 0px);

  color: rgb(10, 48, 0);

  display: flex;
  flex-direction: column;
  align-items: center;

}
</style>

<!-- Comment 

<br />

     <table v-if="form.parsed" style="width: 100%;">
    <thead>
        <tr>
            <th v-for="(header, key) in form.content.meta.fields"
                v-bind:key="'header-'+key">
                {{ header }}
            </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(row, rowKey) in form.content.data"
            v-bind:key="'row-'+rowKey">
                <td v-for="(column, columnKey) in form.content.meta.fields"
                    v-bind:key="'row-'+rowKey+'-column-'+columnKey">
                        <input v-model="form.content.data[rowKey][column]"/>
                </td>
        </tr>
    </tbody>
</table>

-->