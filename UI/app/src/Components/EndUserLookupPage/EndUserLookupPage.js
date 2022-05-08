import axios from "axios";
import React, { Component } from "react";
import { Input } from "antd";
import Output from "../Ouput/Output";
import "./EndUserLookupPage.css";

const { Search } = Input;

export default class EndUserLookupPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
    this.tableElement = React.createRef();
  }

  loadRows = (query) => {
    axios.get("http://127.0.0.1:5000/results?q=" + query).then((res) => {
      this.setState({ data: res.data.results });
      this.tableElement.current.updateData(res.data.results);
    });
  };
  render() {
    return (
      <div>
        <div className="search-bar">
          <Search
            placeholder="Input text"
            onSearch={(value) => this.loadRows(value)}
            enterButton
          />
        </div>
        <Output ref={this.tableElement} data={this.state.data} />
      </div>
    );
  }
}
