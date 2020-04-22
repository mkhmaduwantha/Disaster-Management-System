import { createStore, combineReducers } from "redux";
import { LocationReducer } from "./reducers/LocationReducer";

const rootReducer = combineReducers({
  LocationReducer: LocationReducer,
});

const configureStore = () => createStore(rootReducer);
export default configureStore;
