import React, { Component } from "react";
import axios from "axios";
import {
  Map,
  TileLayer,
  Marker,
  Popup,
  CircleMarker,
  Circle,
} from "react-leaflet";
import { Button, OverlayTrigger, Tooltip, ButtonGroup } from "react-bootstrap";
import {
  FaLocationArrow,
  FaLayerGroup,
  FaDirections,
  FaComment,
  FaFlag,
  FaBullhorn,
  FaBan,
  FaAmbulance,
  FaCarCrash,
  FaMapMarkerAlt,
  FaMapMarker,
} from "react-icons/fa";
import L from "leaflet";
import "./styles/MyMap.css";
import circle_icon from "./img/marker-circle.png";
import red_icon from "./img/marker-red.png";
import Message from "./Message";

const marker_data = {
  markerId: "1",
  userId: "2",
  type: "accident",
};

var myIcon = L.icon({
  iconUrl: circle_icon,
  // "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAApCAYAAADAk4LOAAAFgUlEQVR4Aa1XA5BjWRTN2oW17d3YaZtr2962HUzbDNpjszW24mRt28p47v7zq/bXZtrp/lWnXr337j3nPCe85NcypgSFdugCpW5YoDAMRaIMqRi6aKq5E3YqDQO3qAwjVWrD8Ncq/RBpykd8oZUb/kaJutow8r1aP9II0WmLKLIsJyv1w/kqw9Ch2MYdB++12Onxee/QMwvf4/Dk/Lfp/i4nxTXtOoQ4pW5Aj7wpici1A9erdAN2OH64x8OSP9j3Ft3b7aWkTg/Fm91siTra0f9on5sQr9INejH6CUUUpavjFNq1B+Oadhxmnfa8RfEmN8VNAsQhPqF55xHkMzz3jSmChWU6f7/XZKNH+9+hBLOHYozuKQPxyMPUKkrX/K0uWnfFaJGS1QPRtZsOPtr3NsW0uyh6NNCOkU3Yz+bXbT3I8G3xE5EXLXtCXbbqwCO9zPQYPRTZ5vIDXD7U+w7rFDEoUUf7ibHIR4y6bLVPXrz8JVZEql13trxwue/uDivd3fkWRbS6/IA2bID4uk0UpF1N8qLlbBlXs4Ee7HLTfV1j54APvODnSfOWBqtKVvjgLKzF5YdEk5ewRkGlK0i33Eofffc7HT56jD7/6U+qH3Cx7SBLNntH5YIPvODnyfIXZYRVDPqgHtLs5ABHD3YzLuespb7t79FY34DjMwrVrcTuwlT55YMPvOBnRrJ4VXTdNnYug5ucHLBjEpt30701A3Ts+HEa73u6dT3FNWwflY86eMHPk+Yu+i6pzUpRrW7SNDg5JHR4KapmM5Wv2E8Tfcb1HoqqHMHU+uWDD7zg54mz5/2BSnizi9T1Dg4QQXLToGNCkb6tb1NU+QAlGr1++eADrzhn/u8Q2YZhQVlZ5+CAOtqfbhmaUCS1ezNFVm2imDbPmPng5wmz+gwh+oHDce0eUtQ6OGDIyR0uUhUsoO3vfDmmgOezH0mZN59x7MBi++WDL1g/eEiU3avlidO671bkLfwbw5XV2P8Pzo0ydy4t2/0eu33xYSOMOD8hTf4CrBtGMSoXfPLchX+J0ruSePw3LZeK0juPJbYzrhkH0io7B3k164hiGvawhOKMLkrQLyVpZg8rHFW7E2uHOL888IBPlNZ1FPzstSJM694fWr6RwpvcJK60+0HCILTBzZLFNdtAzJaohze60T8qBzyh5ZuOg5e7uwQppofEmf2++DYvmySqGBuKaicF1blQjhuHdvCIMvp8whTTfZzI7RldpwtSzL+F1+wkdZ2TBOW2gIF88PBTzD/gpeREAMEbxnJcaJHNHrpzji0gQCS6hdkEeYt9DF/2qPcEC8RM28Hwmr3sdNyht00byAut2k3gufWNtgtOEOFGUwcXWNDbdNbpgBGxEvKkOQsxivJx33iow0Vw5S6SVTrpVq11ysA2Rp7gTfPfktc6zhtXBBC+adRLshf6sG2RfHPZ5EAc4sVZ83yCN00Fk/4kggu40ZTvIEm5g24qtU4KjBrx/BTTH8ifVASAG7gKrnWxJDcU7x8X6Ecczhm3o6YicvsLXWfh3Ch1W0k8x0nXF+0fFxgt4phz8QvypiwCCFKMqXCnqXExjq10beH+UUA7+nG6mdG/Pu0f3LgFcGrl2s0kNNjpmoJ9o4B29CMO8dMT4Q5ox8uitF6fqsrJOr8qnwNbRzv6hSnG5wP+64C7h9lp30hKNtKdWjtdkbuPA19nJ7Tz3zR/ibgARbhb4AlhavcBebmTHcFl2fvYEnW0ox9xMxKBS8btJ+KiEbq9zA4RthQXDhPa0T9TEe69gWupwc6uBUphquXgf+/FrIjweHQS4/pduMe5ERUMHUd9xv8ZR98CxkS4F2n3EUrUZ10EYNw7BWm9x1GiPssi3GgiGRDKWRYZfXlON+dfNbM+GgIwYdwAAAAASUVORK5CYII=",
  // iconSize: [25, 41],
  // iconAnchor: [12.5, 41],
  // popupAnchor: [0, -41],
  iconSize: [41, 41],
  iconAnchor: [20.5, 20.5],
  // popupAnchor: [0, -41],
});
var redIcon = L.icon({
  iconUrl: red_icon,
  iconSize: [41, 41],
  iconAnchor: [20.5, 41],
  popupAnchor: [0, -41],
});
// var options = {
//   enableHighAccuracy: true,
//   timeout: 5000,
//   maximumAge: 0
// };

// function success(pos) {
//   var crd = pos.coords;

//   console.log('Your current position is:');
//   console.log(`Latitude : ${crd.latitude}`);
//   console.log(`Longitude: ${crd.longitude}`);
//   console.log(`More or less ${crd.accuracy} meters.`);
// }

// function error(err) {
//   console.warn(`ERROR(${err.code}): ${err.message}`);
// }

// navigator.geolocation.getCurrentPosition(success, error, options);

class Chat extends Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {
      showPopup1: false,
      showPopup2: false,
      showPopup3: false,
      ShowPopup4: false,
      ShowPopup5: false,
      location: {
        lat: 51.505,
        lng: -0.09,
      },
      haveUsersLocation: false,
      zoom: 2,
      userMessage: {
        name: "",
        message: "",
      },
      showDetailBar: false,
    };
  }
  togglePopup(name) {
    switch (name) {
      case "showPopup1":
        this.setState({ showPopup1: !this.state.showPopup1 });
        break;
      case "showPopup2":
        this.setState({ showPopup2: !this.state.showPopup2 });
        break;
      case "showPopup3":
        this.setState({ showPopup3: !this.state.showPopup3 });
        break;
      case "showPopup4":
        this.setState({ showPopup4: !this.state.showPopup4 });
        break;
      case "showPopup5":
        this.setState({ showPopup5: !this.state.showPopup5 });
        break;
      default:
        return null;
    }
    console.log(name, "hello");
  }

  componentDidMount() {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.setState({
          location: {
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
  //no need to bind since we use arrow functions
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

  getPosition = (event) => {
    console.log(`lat: ${event.latlng.lat} , lng: ${event.latlng.lng}`);
  };

  showMarkerDetails = (event) => {
    console.log(event.target.options);
    this.setState({ showDetailBar: !this.state.showDetailBar });
  };

  render() {
    const position = [this.state.location.lat, this.state.location.lng];

    const {
      showPopup1,
      showPopup2,
      showPopup3,
      showPopup4,
      showPopup5,
    } = this.state;
    return (
      <div className="map-container">
        <div className="button-bar">
          <ButtonGroup vertical size="lg">
            {[
              {
                name: "showPopup1",
                value: "notify nearby",
                icon: <FaBullhorn />,
              },
              {
                name: "showPopup2",
                value: "tile layers",
                icon: <FaLayerGroup />,
              },
              {
                name: "showPopup3",
                value: "add a comment",
                icon: <FaComment />,
              },
              {
                name: "showPopup4",
                value: "add a flag",
                icon: <FaFlag />,
              },
              {
                name: "showPopup5",
                value: "find directions",
                icon: <FaDirections />,
              },
            ].map((data, idx) => (
              <>
                <OverlayTrigger
                  key={idx}
                  placement="left"
                  overlay={
                    <Tooltip className="tooltip-right" id="tooltip-top">
                      <strong>{data["value"]}</strong>.
                    </Tooltip>
                  }
                >
                  <Button
                    onClick={() => this.togglePopup(data["name"])}
                    variant="secondary"
                    style={{ height: "3.75em" }}
                  >
                    {data["icon"]}
                    {/* Tooltip on {data["value"]} */}
                  </Button>
                </OverlayTrigger>{" "}
              </>
            ))}
          </ButtonGroup>
        </div>

        {this.state.showDetailBar ? (
          <div className={"detail-bar"}>
            <h1>HEllo I am new DIV</h1>
          </div>
        ) : null}
        <Map
          className="map"
          center={position}
          zoom={this.state.zoom}
          onclick={this.getPosition}
          minZoom={3}
        >
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {this.state.haveUsersLocation ? (
            <>
              {/* <Circle center={position} fillColor="blue" radius={200} /> */}
              <CircleMarker
                center={position}
                icon={myIcon}
                fillcolor="blue"
                radius={80}
              >
                <Popup>Popup in CircleMarker</Popup>
              </CircleMarker>
              <Marker position={position} icon={myIcon}>
                <Popup>
                  A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
              </Marker>
            </>
          ) : (
            ""
          )}
          <Marker
            position={[6.245681049537433, 80.34301757812501]}
            icon={redIcon}
            props={marker_data}
            onClick={(e) => {
              this.showMarkerDetails(e);
            }}
          >
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker>
          {/* ///////////////////////////////////////////////////////////////////// */}

          {/* https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png
            https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png */}

          <LayersControl position="topright">
            <BaseLayer checked name="OpenStreetMap.Mapnik">
              <TileLayer
                attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
            </BaseLayer>
            <BaseLayer name="OpenStreetMap.BlackAndWhite">
              <TileLayer
                attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"
              />
            </BaseLayer>
            <Overlay name="Marker with popup">
              <Marker position={center}>
                <Popup>
                  A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
              </Marker>
            </Overlay>
            <Overlay checked name="Layer group with circles">
              <LayerGroup>
                <Circle center={center} fillColor="blue" radius={200} />
                <Circle
                  center={center}
                  fillColor="red"
                  radius={100}
                  stroke={false}
                />
                <LayerGroup>
                  <Circle
                    center={[51.51, -0.08]}
                    color="green"
                    fillColor="green"
                    radius={100}
                  />
                </LayerGroup>
              </LayerGroup>
            </Overlay>
            <Overlay name="Feature group">
              <FeatureGroup color="purple">
                <Popup>Popup in FeatureGroup</Popup>
                <Circle center={[51.51, -0.06]} radius={200} />
                <Rectangle bounds={rectangle} />
              </FeatureGroup>
            </Overlay>
          </LayersControl>
        </Map>

        {showPopup1 ? (
          <div className="message-form">
            <Message
              props={this.props}
              closePopup={this.togglePopup.bind(this, "showPopup1")}
            />
          </div>
        ) : null}
        {showPopup2 ? <div className="message-form"></div> : null}
        {showPopup3 ? <div className="message-form"></div> : null}
        {showPopup4 ? <div className="message-form"></div> : null}
        {showPopup5 ? <div className="message-form"></div> : null}
      </div>
    );
  }
}

export default Chat;
// I WILL DO MY BEST