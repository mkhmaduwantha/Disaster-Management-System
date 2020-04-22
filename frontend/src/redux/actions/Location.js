import { SET_LOCATION, SET_MARKER } from "./Types";

export const setLocation = (data) => ({
  type: SET_LOCATION,
  data: data,
});

export const setMarker = (data) => ({
  type: SET_MARKER,
  data: data,
});
