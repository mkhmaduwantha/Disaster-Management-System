import { SET_LOCATION, SET_MARKER } from "../actions/Types";

const initialState = {
  location: {
    lat: 6.038171,
    lng: 80.483939,
  },
  marker: {
    lat: 7.445866,
    lng: 79.99842,
  },
};

export const LocationReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_LOCATION:
      return {
        ...state,
        location: {
          lat: action.data.location.lat,
          lng: action.data.location.lng,
        },
      };
    case SET_MARKER:
      return {
        ...state,
        marker: {
          lat: action.data.marker.lat,
          lng: action.data.marker.lng,
        },
      };
    default:
      return state;
  }
};
