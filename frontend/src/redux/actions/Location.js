import {
  SET_LOCATION,
  SET_MARKER,
  SET_START_LOCATION,
  SET_END_LOCATION,
} from "./Types";

export const setLocation = (data) => ({
  type: SET_LOCATION,
  data: data,
});

export const setMarker = (data) => ({
  type: SET_MARKER,
  data: data,
});

export const setStartLocation = (data) => ({
  type: SET_START_LOCATION,
  data: data,
});

export const setEndLocation = (data) => ({
  type: SET_END_LOCATION,
  data: data,
});
