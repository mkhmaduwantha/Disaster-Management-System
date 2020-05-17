import React, { Component } from "react";
import MyMap from "./components/MyMap";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { SideNavBar } from "./components/SideNavBar";
import Test from "./components/Test";
import { Provider } from "react-redux";
import configureStore from "./redux/Store";
import LeafletMap from "./components/LeafletMap";

const Store = configureStore();

class App extends Component {
  render() {
    return (
      <Provider store={Store}>
        <div id="leafletmap">
          {/* <SideNavBar /> */}
          <LeafletMap/>
        </div>
      </Provider>
    );
  }
}

export default App;
// I WILL DO MY BEST
