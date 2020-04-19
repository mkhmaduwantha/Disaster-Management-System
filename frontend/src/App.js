import React, { Component } from "react";
import MyMap from "./components/MyMap";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { SideNavBar } from "./components/SideNavBar";
import Test from "./components/Test";

class App extends Component {
  render() {
    return (
      <div id="leafletmap">
        <SideNavBar />
      </div>
    );
  }
}

export default App;
// I WILL DO MY BEST
