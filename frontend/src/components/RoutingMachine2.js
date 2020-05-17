import { MapLayer, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet-routing-machine";
import { withLeaflet } from "react-leaflet";
import { connect } from "react-redux";
import React, { Component } from "react";
import { MAPBOX_TOKEN, MAPBOX_SERVICE_URL } from "consts";
import { Button } from "react-bootstrap";

class Routing extends Component {
  constructor(props) {
    super(props);

    this.state = {
      routingPopUp: null,
    };
  }

  componentDidUpdate() {
    this.initializeRouting();
  }

  componentWillUnmount() {
    this.destroyRouting();
  }

  initializeRouting = () => {
    if (this.props.map && !this.routing) {
      const plan = new L.Routing.Plan([L.latLng(), L.latLng()], {
        routeWhileDragging: false,
        reverseWaypoints: true,
        geocoder: L.Control.Geocoder.nominatim(),
      });

      // this.routing = L.Routing.control({
      //   plan,
      //   serviceUrl: MAPBOX_SERVICE_URL,
      //   router: L.Routing.mapbox(MAPBOX_TOKEN),
      // });
      this.routing = L.Routing.control({
        plan,
        collapsible: true,
        // show: false,
        reverseWaypoints: true,
        fitSelectedRoutes: true,
        showAlternatives: true,
        lineOptions: {
          styles: [
            { color: "black", opacity: 0.15, weight: 9 },
            { color: "white", opacity: 0.8, weight: 6 },
            { color: "red", opacity: 1, weight: 2 },
          ],
        },
        altLineOptions: {
          styles: [
            { color: "red", opacity: 0.15, weight: 9 },
            { color: "white", opacity: 0.8, weight: 6 },
            { color: "blue", opacity: 0.5, weight: 2 },
          ],
        },
        fitSelectedRoutes: false,
        zoom: 10,
      });

      this.props.map.leafletElement.addControl(this.routing);
      L.DomEvent.on(
        this.props.map.leafletElement,
        "click",
        this.createPopupsHandler
      );
    }
  };

  createLeafletElement = () => {
    const { map } = this.props;
    let leafletElement = L.Routing.control({
      waypoints: [
        L.latLng(this.props.location.lat, this.props.location.lng),
        L.latLng(this.props.location.lat, this.props.location.lng),
      ],
      show: false,
      collapsible: true,
      reverseWaypoints: true,
      fitSelectedRoutes: true,
      showAlternatives: true,
      lineOptions: {
        styles: [
          { color: "black", opacity: 0.15, weight: 9 },
          { color: "white", opacity: 0.8, weight: 6 },
          { color: "red", opacity: 1, weight: 2 },
        ],
      },
      altLineOptions: {
        styles: [
          { color: "red", opacity: 0.15, weight: 9 },
          { color: "white", opacity: 0.8, weight: 6 },
          { color: "blue", opacity: 0.5, weight: 2 },
        ],
      },

      geocoder: L.Control.Geocoder.nominatim(),
      fitSelectedRoutes: false,
      zoom: "auto",
    })
      .on("routesfound", function (e) {
        var routes = e.routes;
        // alert("Found " + routes.length + " route(s).");
      })
      .addTo(map.leafletElement);

    return leafletElement.getPlan();
  };

  destroyRouting = () => {
    if (this.props.map) {
      this.props.map.leafletElement.removeControl(this.routing);
      L.DomEvent.off(
        this.props.map.leafletElement,
        "click",
        this.createPopupsHandler
      );
    }
  };

  createPopupsHandler = (e) => {
    const position = e.latlng;
    const startBtnOnClick = () => {
      this.routing.spliceWaypoints(0, 1, position);
      this.setRoutingPopUp(null);
    };
    const endBtnOnClick = () => {
      this.routing.spliceWaypoints(
        this.routing.getWaypoints().length - 1,
        1,
        position
      );
      this.setRoutingPopUp(null);
    };
    const startBtn = (
      <Button
        variant="primary"
        onClick={startBtnOnClick}
        size="sm"
        style={{ width: "100%" }}
      >
        Set begin position
      </Button>
    );
    const endBtn = (
      <Button
        onClick={endBtnOnClick}
        variant="primary"
        size="sm"
        style={{ width: "100%" }}
      >
        Set end position
      </Button>
    );
    const children = (
      <div>
        {startBtn}
        <br /> <br />
        {endBtn}
      </div>
    );
    const onClose = this.setRoutingPopUp;
    this.setRoutingPopUp({ children, position, onClose });
  };

  setRoutingPopUp = (routingPopUp) => {
    this.setState({ routingPopUp });
  };

  render() {
    const { routingPopUp } = this.state;
    if (routingPopUp) return <Popup {...this.state.routingPopUp} />;

    return null;
  }
}

const mapStateToProps = (state) => {
  return {
    location: state.LocationReducer.location,
    marker: state.LocationReducer.marker,
  };
};

export default connect(mapStateToProps)(withLeaflet(Routing));
