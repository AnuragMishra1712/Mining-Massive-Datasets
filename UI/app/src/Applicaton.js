import "antd/dist/antd.css";
import React, { Component } from "react";
import "./Application.css";
import ExtractionPage from "./Components/ExtractionPage/ExtractionPage";
import NavigationBar from "./Components/NavigationBar/NavigationBar";
import EndUserLookupPage from "./Components/EndUserLookupPage/EndUserLookupPage";

export default class Application extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      showExtract: false,
      menuItem: "Extract",
    };
  }

  toggleExtract = () => {
    let currentState = this.state.showExtract;
    this.setState({
      showExtract: !currentState,
      menuItem: currentState ? "Extract" : "Search",
    });
  };

  render() {
    return (
      <div className="App">
        <NavigationBar
          itemName={this.state.menuItem}
          onClickExtract={this.toggleExtract}
        />
        <div className={this.state.showExtract ? "" : "hide"}>
          <ExtractionPage />
        </div>
        <div className={this.state.showExtract ? "hide" : ""}>
          <EndUserLookupPage />
        </div>
      </div>
    );
  }
}
