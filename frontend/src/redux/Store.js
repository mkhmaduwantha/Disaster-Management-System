import { createStore, combineReducers } from "redux";
import { LocationReducer } from "./reducers/LocationReducer";

const rootReducer = combineReducers({
  LocationReducer: LocationReducer,
});

const configureStore = () =>
  createStore(
    rootReducer /* preloadedState, */,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );
export default configureStore;
