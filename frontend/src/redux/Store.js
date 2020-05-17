import { createStore, combineReducers } from "redux";

// import { syncHistoryWithStore } from "react-router-redux";
// import { browserHistory } from "react-router";
// import { routerReducer } from "react-router-redux";

import { LocationReducer } from "./reducers/LocationReducer";

const rootReducer = combineReducers({
  LocationReducer: LocationReducer,
  // routing: routerReducer,
});

const configureStore = () =>
  createStore(
    rootReducer /* preloadedState, */,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );
//if we want we can make a default state object
//add later

// const configureStore = () => createStore(rootReducer);

// export const history = syncHistoryWithStore(browserHistory, configureStore);

export default configureStore;
