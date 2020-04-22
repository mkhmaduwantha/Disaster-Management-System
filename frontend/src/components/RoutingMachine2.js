import { MapLayer } from "react-leaflet";
import L from "leaflet";
import "leaflet-routing-machine";
import { withLeaflet } from "react-leaflet";
import { connect } from "react-redux";

class Routing extends MapLayer {
  createLeafletElement() {
    const { map } = this.props;
    let leafletElement = L.Routing.control({
      waypoints: [
        L.latLng(this.props.location.lat, this.props.location.lng),
        L.latLng(this.props.location.lat, this.props.location.lng),
      ],
      routeWhileDragging: true,
      fitSelectedRoutes: false,
      zoom: 10,
    }).addTo(map.leafletElement);
    return leafletElement.getPlan();
  }
}

const mapStateToProps = (state) => {
  return {
    location: state.LocationReducer.location,
    marker: state.LocationReducer.marker,
  };
};

export default connect(mapStateToProps)(withLeaflet(Routing));
