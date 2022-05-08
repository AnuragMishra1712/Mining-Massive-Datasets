import React, { Component } from "react";
import { Input } from "antd";
import "./LookupBar.css";

const { Search } = Input;

export default class LookupBar extends Component {
  render() {
    return (
      <div className="search-bar">
        <Search
          placeholder="Input query term"
          enterButton="Extract"
          size="large"
          onSearch={(value) => this.props.onSearch(value)}
        />
      </div>
    );
  }
}
