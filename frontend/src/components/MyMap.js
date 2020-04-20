import React, { Component, createRef } from "react";
import {
  Map,
  TileLayer,
  Marker,
  Popup,
  withLeaflet,
  MapControl,
  Polyline,
  Path,
} from "react-leaflet";
import axios from "axios";
import L, { map, Control } from "leaflet";

import {
  Card,
  Button,
  CardTitle,
  CardText,
  Form,
  FormGroup,
  Label,
  Input,
} from "reactstrap";
import "./styles/MyMap.css";
import iconFixed from "leaflet/dist/images/fixed-location.png";
import iconDrag from "leaflet/dist/images/drag-location.png";
import iconUser from "leaflet/dist/images/user-location.png";
import AntPath from "react-leaflet-ant-path";
import { antPath } from "leaflet-ant-path";
import "leaflet-routing-machine";
import RoutingMachine from "./RoutingMachine";

var myIcon = L.icon({
  iconUrl: iconDrag,
  iconSize: [25, 41],
  iconAnchor: [12.5, 41],
  popupAnchor: [0, -41],
});

var myIconFixed = L.icon({
  iconUrl: iconFixed,
  iconSize: [25, 41],
  iconAnchor: [12.5, 41],
  popupAnchor: [0, -41],
});

var myIconUser = L.icon({
  iconUrl: iconUser,
  iconSize: [25, 41],
  iconAnchor: [12.5, 41],
  popupAnchor: [0, -41],
});

export class MyMap extends Component {
  state = {
    location: {
      lat: 6.016255,
      lng: 80.647191,
    },
    marker: {
      lat: 7.426861,
      lng: 80.504022,
    },
    haveUsersLocation: false,
    zoom: 2,
    userMessage: {
      name: "",
      message: "",
    },
    draggable: true,
    isMapInit: false,
  };

  componentDidMount() {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.setState({
          location: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
          marker: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
          haveUsersLocation: true,
          zoom: 13,
        });
        console.log(position);
      },
      () => {
        console.log("no given location!");
        fetch("https://ipapi.co/json")
          .then((res) => res.json())
          .then((location) => {
            console.log(location);
            this.setState({
              location: {
                lat: location.latitude,
                lng: location.longitude,
              },
              haveUsersLocation: true,
              zoom: 13,
            });
          });
      }
    );
  }

  createLeafletElement() {
    const { map } = this.props;
    let leafletElement = L.Routing.control({
      waypoints: [
        L.latLng(16.506, 80.648),
        L.latLng(17.384, 78.4866),
        L.latLng(12.971, 77.5945),
      ],
      // router: new L.Routing.Google(),
      lineOptions: {
        styles: [
          {
            color: "blue",
            opacity: 0.6,
            weight: 4,
          },
        ],
      },
      addWaypoints: false,
      draggableWaypoints: false,
      fitSelectedRoutes: false,
      showAlternatives: false,
    }).addTo(map.leafletElement);
    return leafletElement.getPlan();
  }

  saveMap = (map) => {
    this.map = map;
    this.setState({
      isMapInit: true,
    });
  };

  // $FlowFixMe: ref
  refmarker = createRef();

  toggleDraggable = () => {
    this.setState({ draggable: !this.state.draggable });
  };

  updatePosition = () => {
    const marker = this.refmarker.current;
    if (marker != null) {
      this.setState({
        marker: marker.leafletElement.getLatLng(),
      });
    }
  };

  formSubmitted = (event) => {
    //page doesn't refreshed
    event.preventDefault();
    console.log(this.state.userMessage);

    axios.get("http://lcoalhost:5000/map/Message").then((res) => {
      console.log(res.data);
    });
  };

  valueChanged = (event) => {
    const { name, value } = event.target;
    this.setState((prevState) => ({
      userMessage: {
        ...prevState.userMessage,
        [name]: value,
      },
    }));
  };

  render() {
    const position = [this.state.location.lat, this.state.location.lng];
    const markerPosition = [this.state.marker.lat, this.state.marker.lng];

    return (
      <div style={{ marginLeft: 64 }} id="map">
        <Map
          ref={this.saveMap}
          className="map"
          id="mapid"
          center={position}
          zoom={this.state.zoom}
        >
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* {this.state.isMapInit && (
            <RoutingMachine
              map={this.map}
              location={this.state.location}
              marker={this.state.marker}
            />
          )} */}
          {/* <AntPath
            positions={[
              [this.state.location.lat, this.state.location.lng],
              [this.state.marker.lat, this.state.marker.lng],
            ]}
          /> */}

          {this.state.haveUsersLocation ? (
            <div>
              <Marker
                position={position}
                ref={this.refmarker}
                icon={myIconUser}
              >
                <Popup>MY LOCATION</Popup>
              </Marker>
              <Marker
                draggable={this.state.draggable}
                ondragend={this.updatePosition}
                position={markerPosition}
                ref={this.refmarker}
                icon={myIcon}
              >
                <Popup></Popup>
              </Marker>
              <Marker
                draggable={this.state.draggable}
                ondragend={this.updatePosition}
                position={markerPosition}
                ref={this.refmarker}
                icon={this.state.draggable ? myIcon : myIconFixed}
              >
                <Popup>
                  {/* A pretty CSS3 popup. <br /> Easily customizable. */}
                  <span onClick={this.toggleDraggable}>
                    {this.state.draggable
                      ? "DRAG AND SET (Click to fix)"
                      : "LOCATION FIXED! (Click to drag)"}
                  </span>
                </Popup>
              </Marker>
            </div>
          ) : (
            ""
          )}
        </Map>
        <Card body className="message-form">
          <CardTitle>Welcome to EmergencyAssistant!</CardTitle>
          <CardText>Leave a message with your location</CardText>
          <CardText>Thanks for stopping by!</CardText>
          <Form onSubmit={this.formSubmitted}>
            <FormGroup>
              <Label for="name">Name</Label>
              <Input
                onChange={this.valueChanged}
                type="text"
                name="name"
                id="name"
                placeholder="Enter your name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="message">Message</Label>
              <Input
                onChange={this.valueChanged}
                type="textarea"
                name="message"
                id="message"
                placeholder="Enter a Message"
              />
            </FormGroup>
            <Button
              type="submit"
              disabled={!this.state.haveUsersLocation}
              color="info"
            >
              Send
            </Button>
          </Form>
        </Card>
      </div>
    );
  }
}

export default MyMap;
