import React, { Component } from "react";
import MyMap from "./components/MyMap";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import Test from "./components/Test";
import { Provider } from "react-redux";
import configureStore from "./redux/Store";
import LeafletMap from "./components/LeafletMap";
import Chat from "./components/Chat";
import { UserMap } from "./components/UserMap";
import { AdminMap } from "./components/AdminMap";
import SideNavBar from "./components/SideNavBar";

const Store = configureStore();

class App extends Component {
  render() {
    return (
      <Provider store={Store}>
        <div id="leafletmap">
          <SideNavBar />
          {/* <AdminMap /> */}
          {/* <LeafletMap /> */}
          {/* <Chat /> */}
        </div>
      </Provider>
    );
  }
}

export default App;
// I WILL DO MY BEST
