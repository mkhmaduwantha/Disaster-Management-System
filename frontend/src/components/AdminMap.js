import React, { Component, createRef } from "react";
import {
  Modal,
  Button,
  Card,
  Row,
  Col,
  Carousel,
  Spinner,
} from "react-bootstrap";
import { FaPhoneAlt } from "react-icons/fa";
import {
  Map,
  TileLayer,
  Marker,
  Popup,
  withLeaflet,
  MapControl,
  Polyline,
  Path,
  Circle,
} from "react-leaflet";

import axios from "axios";
import "./styles/MyMap.css";
import L, { map, Control, control } from "leaflet";
import iconFixed from "leaflet/dist/images/marker-icon.png";
import iconDrag from "leaflet/dist/images/drag-location.png";
import iconUser from "leaflet/dist/images/marker-icon.png";
import templeIcon from "leaflet/dist/images/temple.png";
import schoolIcon from "leaflet/dist/images/school.png";
import militaryIcon from "leaflet/dist/images/military.png";
import otherIcon from "leaflet/dist/images/other.png";
import AntPath from "react-leaflet-ant-path";
import { antPath } from "leaflet-ant-path";
import "leaflet-routing-machine";
import { setLocation, setMarker } from "../redux/actions/Location";
import Routing from "./RoutingMachine";
import { storage, firebasedb } from "../config/firebasedb";
import LeafltMapModal from "./LeafltMapModal";
import EditSafeLocation from "./EditSafeLocation";

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

var iconSchool = L.icon({
  iconUrl: schoolIcon,
  iconSize: [60, 51],
  iconAnchor: [28, 41],
  popupAnchor: [0, -41],
});

var iconTemple = L.icon({
  iconUrl: templeIcon,
  iconSize: [60, 51],
  iconAnchor: [28, 41],
  popupAnchor: [0, -41],
});

var iconMilitary = L.icon({
  iconUrl: militaryIcon,
  iconSize: [60, 51],
  iconAnchor: [28, 41],
  popupAnchor: [0, -41],
});

var iconOther = L.icon({
  iconUrl: otherIcon,
  iconSize: [60, 51],
  iconAnchor: [28, 41],
  popupAnchor: [0, -41],
});

export class AdminMap extends Component {
  constructor(props) {
    super(props);

    this.state = {
      haveUsersLocation: false,
      zoom: 2,
      userMessage: {
        name: "",
        message: "",
      },
      draggable: true,
      isMapInit: false,
      currentPos: null,
      modalShow: false,
      editModalShow: false,
      detailsmodalShow: false,
      safeLocations: [],
      currentSafeLocation: {},
      isLoadingImages: true,
      currentSafeLocation: null,
    };
  }

  handleClick = (e) => {
    this.setState({ isPopUp: true, currentPos: e.latlng });
  };

  saveMap = (map) => {
    this.map = map;
    this.setState({
      isMapInit: true,
    });
  };

  componentDidMount() {
    firebasedb.ref("/places").on("value", (querySnapshot) => {
      let data = querySnapshot.val() ? querySnapshot.val() : {};
      let safeLocations = { ...data };
      let newState = [];
      for (let location in safeLocations) {
        newState.push({
          id: location,
          name: safeLocations[location].name,
          phoneNo: safeLocations[location].phoneNo,
          category: safeLocations[location].category,
          noOfRefugees: safeLocations[location].noOfRefugees,
          imagesUrls: safeLocations[location].imagesUrls,
          position: safeLocations[location].position,
        });
      }
      this.setState(
        {
          safeLocations: newState,
        },
        () => console.log(this.state.safeLocations)
      );
    });

    //////////////////
    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.setState({
          currentPos: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
          haveUsersLocation: true,
          zoom: 13,
        });
        console.log(position.coords.latitude, position.coords.longitude);
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
    return (
      <div className="map-container">
        <Map
          center={this.state.currentPos}
          zoom={this.state.zoom}
          ref={this.saveMap}
          onClick={this.handleClick}
        >
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
          />

          {/* {this.state.isMapInit && <Routing name="ishara" map={this.map} />} */}

          {/* Position On click on map  */}
          {this.state.currentPos && (
            <Marker
              position={this.state.currentPos}
              draggable={true}
              icon={myIcon}
            >
              <Popup position={this.state.currentPos}>
                <Button
                  variant="primary"
                  onClick={() => this.setState({ modalShow: true })}
                >
                  Set This Place As A Safe Location
                </Button>
                {/* Current location:{" "} */}
                {/* <pre>{JSON.stringify(this.state.currentPos, null, 2)}</pre> */}
              </Popup>
            </Marker>
          )}

          {/* Show Safe Locations on the Map  */}
          {this.state.safeLocations &&
            this.state.safeLocations.map((location) => {
              let icon = null;
              if (location.category == "Temple") {
                icon = iconTemple;
              } else if (location.category == "School") {
                icon = iconSchool;
              } else if (location.category == "Military Camp") {
                icon = iconMilitary;
              } else {
                icon = iconOther;
              }
              return (
                <Marker
                  position={location.position}
                  icon={icon}
                  onclick={() =>
                    this.setState({ currentSafeLocation: location }, () =>
                      this.setState({ editModalShow: true })
                    )
                  }
                >
                  {/* <Popup>
                    <div>
                      <h5 style={{ width: "300px", textAlign: "center" }}>
                        {location.name}
                      </h5>
                      {location.phoneNo} <br />
                      No. of refugees that can be retained :{" "}
                      {location.noOfRefugees}
                      <Carousel>
                        {location.imagesUrls.map((url) => {
                          return (
                            <Carousel.Item>
                              <div
                                style={{
                                  width: "300px",
                                  height: "200px",
                                  textAlign: "center",
                                }}
                              >
                                <img
                                  width="100%"
                                  className="d-block w-100"
                                  src={url}
                                  alt="First slide"
                                />
                              </div>

                              <Carousel.Caption></Carousel.Caption>
                            </Carousel.Item>
                          );
                        })}
                      </Carousel>
                    </div>
                  </Popup> */}
                </Marker>
              );
            })}
        </Map>

        {/* Modal */}
        {this.state.editModalShow && (
          <EditSafeLocation
            position={this.state.currentPos}
            // show={this.state.modalShow}
            currentSafeLocation={this.state.currentSafeLocation}
            show={true}
            onHide={() => this.setState({ editModalShow: false })}
            currentSafeLocation={this.state.currentSafeLocation}
          />
        )}

        <LeafltMapModal
          position={this.state.currentPos}
          show={this.state.modalShow}
          onHide={() => this.setState({ modalShow: false })}
        />
      </div>
    );
  }
}

export default AdminMap;