import React, { Component } from "react";
import { Layout, Typography, Menu } from "antd";
import "./NavigationBar.css";

const { Header } = Layout;
const { Title } = Typography;
export default class NavigationBar extends Component {
  render() {
    return (
      <div>
        <Header
          style={{
            zIndex: 1,
            width: "100%",
          }}
        >
          <div className="logo">
            <Title style={{ color: "#0ff", cursor: "pointer" }}>
              AutomatedTaggerApp
            </Title>
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            style={{ float: "right", marginRight: 24 }}
            defaultSelectedKeys={["1"]}
          >
            <Menu.Item key="1" onClick={this.props.onClickExtract}>
              {this.props.itemName}
            </Menu.Item>
          </Menu>
        </Header>
      </div>
    );
  }
}
