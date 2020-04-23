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
import axios from "axios";
import "./styles/MyMap.css";
import L, { map, Control } from "leaflet";
import iconFixed from "leaflet/dist/images/marker-icon.png";
import iconDrag from "leaflet/dist/images/marker-icon.png";
import iconUser from "leaflet/dist/images/marker-icon.png";
import AntPath from "react-leaflet-ant-path";
import { antPath } from "leaflet-ant-path";
import "leaflet-routing-machine";
import { setLocation, setMarker } from "../redux/actions/Location";
import { connect } from "react-redux";
import Routing from "./RoutingMachine2";

//Icons
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

export class LeafletMap extends Component {
  state = {
    haveUsersLocation: false,
    zoom: 2,
    userMessage: {
      name: "",
      message: "",
    },
    draggable: true,
    isMapInit: false,
  };

  saveMap = (map) => {
    this.map = map;
    this.setState({
      isMapInit: true,
    });
  };

  componentDidMount() {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.props.setLocation({
          location: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
        });
        this.props.setMarker({
          marker: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
        });
        this.setState({
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
            this.props.setLocation({
              location: {
                lat: location.latitude,
                lng: location.longitude,
              },
            });
            this.props.setMarker({
              marker: {
                lat: location.latitude,
                lng: location.longitude,
              },
            });
            this.setState({
              haveUsersLocation: true,
              zoom: 10,
            });
          });
      }
    );
  }

  // $FlowFixMe: ref
  refmarker = createRef();

  toggleDraggable = () => {
    this.setState({ draggable: !this.state.draggable });
  };

  updatePosition = () => {
    const marker = this.refmarker.current;
    if (marker != null) {
      this.props.setMarker({ marker: marker.leafletElement.getLatLng() });
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
    const position = [this.props.location.lat, this.props.location.lng];
    const markerPosition = [this.props.marker.lat, this.props.marker.lng];
    return (
      <div>
        <Map
          center={position}
          zoom={this.state.zoom}
          ref={this.saveMap}
        >
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
          />

          {this.state.isMapInit && <Routing map={this.map} />}
        </Map>
        {/* <Card body className="message-form">
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
        </Card> */}
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    location: state.LocationReducer.location,
    marker: state.LocationReducer.marker,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    setLocation: (data) => dispatch(setLocation(data)),
    setMarker: (data) => dispatch(setMarker(data)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(LeafletMap);
