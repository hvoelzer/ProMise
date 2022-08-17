import React, {useState, useEffect} from "react";
import {Form, Input, Button} from "semantic-ui-react"

function App() {
  const [file, setFile] = useState();
  const [timeStampString, setTimeStampString] = useState();
  const [timeStampColumn, setTimeStampColumn] = useState();
  const [activityColumn, setActivityColumn] = useState();
  const [traceColumn, setTraceColumn] = useState();
  const [separator, setSeparator] = useState();
  const [array, setArray] = useState([]);

  const fileReader = new FileReader();

  const handleOnChangeFile = (e) => {
    setFile(e.target.files[0]);
  };

  const handleOnChangeTimeStampString = (e) => {
    console.log(e.target.value)
    setTimeStampString(e.target.value);
  };

  const handleOnChangeTimeStampColumn = (e) => {
    console.log(e.target.value)
    setTimeStampColumn(e.target.value);
  };

  const handleOnChangeActivityColumn = (e) => {
    console.log(e.target.value)
    setActivityColumn(e.target.value);
  };

  const handleOnChangeTraceColumn = (e) => {
    console.log(e.target.value)
    setTraceColumn(e.target.value);
  };

  const handleOnChangeSeparator = (e) => {
    console.log(e.target.value)
    setSeparator(e.target.value);
  };

  const csvFileToArray = string => {
    const csvHeader = string.slice(0, string.indexOf("\n")).split(separator);
    const csvRows = string.slice(string.indexOf("\n") + 1).split("\n");

    const array = csvRows.map(i => {
      const values = i.split(separator);
      const obj = csvHeader.reduce((object, header, index) => {
        object[header] = values[index];
        return object;
      }, {});
      return obj;
    });

    setArray(array);
  };

  const handleOnSubmit = (e) => {
    e.preventDefault();

    if (file) {
      fileReader.onload = function (event) {
        const text = event.target.result;
        csvFileToArray(text);
      };

      fileReader.readAsText(file);
    }
  };

  const headerKeys = Object.keys(Object.assign({}, ...array));

  return (
    <div style={{ textAlign: "center" }}>
      <h1>REACTJS CSV IMPORT EXAMPLE </h1>
      <Form>
        <Form.Field>
          <Input
            type={"file"}
            id={"csvFileInput"}
            accept={".csv"}
            onChange={handleOnChangeFile}
          />
        </Form.Field>
        <Form.Field>
          <Input
            type={"text"}
            id={"timeStampInput"}
            placeholder="Timestamp Formatting String"
            onChange={handleOnChangeTimeStampString}
          />
        </Form.Field>
        <Form.Field>
          <Input
              type={"number"}
              id={"timeStampColumn"}
              placeholder="Timestamp Column"
              onChange={handleOnChangeTimeStampColumn}
            />
        </Form.Field>
        <Form.Field>
          <Input
              type={"number"}
              id={"activityColumn"}
              placeholder="Activity Column"
              onChange={handleOnChangeActivityColumn}
            />
        </Form.Field>
        <Form.Field>
          <Input
              type={"number"}
              id={"traceColumn"}
              placeholder="Trace Column"
              onChange={handleOnChangeTraceColumn}
            />
        </Form.Field>
        <Form.Field>
          <Input
              type={"text"}
              id={"separator"}
              placeholder="Separator"
              onChange={handleOnChangeSeparator}
            />
        </Form.Field>
        <Form.Field>
          <Button
            onClick={(e) => {
              handleOnSubmit(e);
            }}
          >
            IMPORT CSV
          </Button>
        </Form.Field>
      </Form>

      <br />

      <table>
        <thead>
          <tr key={"header"}>
            {headerKeys.map((key) => (
              <th>{key}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {array.map((item) => (
            <tr key={item.id}>
              {Object.values(item).map((val) => (
                <td>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


export default App