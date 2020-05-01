import {
  SET_LOCATION,
  SET_MARKER,
  SET_START_LOCATION,
  SET_END_LOCATION,
} from "../actions/Types";

const initialState = {
  location: {
    lat: 6.038171,
    lng: 80.483939,
  },
  marker: {
    lat: 7.445866,
    lng: 79.99842,
  },
  startLocation: {
    lat: 6.038171,
    lng: 80.483939,
  },
  endLocation: {
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
    case SET_START_LOCATION:
      return {
        ...state,
        startLocation: {
          lat: action.data.lat,
          lng: action.data.lng,
        },
      };

    case SET_END_LOCATION:
      return {
        ...state,
        endLocation: {
          lat: action.data.lat,
          lng: action.data.lng,
        },
      };
    default:
      return state;
  }
};
