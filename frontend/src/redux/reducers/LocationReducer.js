import { SET_LOCATION } from "../actions/Types";

import React, { Component } from "react";

class LocationReducer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      location: {
        lat: 51.505,
        lng: -0.09,
      },
      marker: {
        lat: 51.505,
        lng: -0.09,
      },
    };
  }

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
  render() {
    return <div></div>;
  }
}
const initialState = {
  location: {
    lat: 51.505,
    lng: -0.09,
  },
  marker: {
    lat: 51.505,
    lng: -0.09,
  },
};

export const LocationReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_LOCATION:
  }
};
