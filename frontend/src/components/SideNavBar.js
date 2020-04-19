import React, { Component } from "react";
import SideNav, {
  Toggle,
  Nav,
  NavItem,
  NavIcon,
  NavText,
} from "@trendmicro/react-sidenav";

// Be sure to include styles at some point, probably during your bootstraping
import "@trendmicro/react-sidenav/dist/react-sidenav.css";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import MyMap from "./MyMap";
import Test from "./Test";
import { FaHome, FaMapMarkerAlt, FaPhone } from "react-icons/fa";
import { IoIosChatbubbles } from "react-icons/io";
import Home from "./Home";
import PhoneBook from "./PhoneBook";
import Chat from "./Chat";

export class SideNavBar extends Component {
  render() {
    return (
      <div>
        <Router>
          <Route
            render={({ location, history }) => (
              <React.Fragment>
                <SideNav
                  onSelect={(selected) => {
                    const to = "/" + selected;
                    if (location.pathname !== to) {
                      history.push(to);
                    }
                  }}
                >
                  <SideNav.Toggle />
                  <SideNav.Nav defaultSelected="home">
                    <NavItem eventKey="">
                      <NavIcon>
                        <FaHome style={{ fontSize: "1.75em" }} />
                      </NavIcon>
                      <NavText>Home</NavText>
                    </NavItem>
                    <NavItem eventKey="map">
                      <NavIcon>
                        <FaMapMarkerAlt style={{ fontSize: "1.75em" }} />
                      </NavIcon>
                      <NavText>Map</NavText>
                    </NavItem>
                    <NavItem eventKey="phonebook">
                      <NavIcon>
                        <FaPhone style={{ fontSize: "1.75em" }} />
                        {/* IoIosChatbubbles */}
                      </NavIcon>
                      <NavText>Phone Book</NavText>
                    </NavItem>{" "}
                    <NavItem eventKey="chat">
                      <NavIcon>
                        <IoIosChatbubbles style={{ fontSize: "1.75em" }} />
                      </NavIcon>
                      <NavText>Chat</NavText>
                    </NavItem>
                  </SideNav.Nav>
                </SideNav>
                <main>
                  <Route path="/" exact component={(props) => <Home />} />
                  <Route path="/map" component={(props) => <MyMap />} />
                  <Route
                    path="/phonebook"
                    component={(props) => <PhoneBook />}
                  />
                  <Route path="/chat" component={(props) => <Chat />} />
                </main>
              </React.Fragment>
            )}
          />
        </Router>
      </div>
    );
  }
}

export default SideNavBar;
