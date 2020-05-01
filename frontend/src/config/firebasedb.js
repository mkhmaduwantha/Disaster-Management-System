import firebase from "firebase";
import "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyCtJraEpiuqHT7HhiCw6hq1pR2GtzkknbA",
  authDomain: "disaster-management-syst-3c9f8.firebaseapp.com",
  databaseURL: "https://disaster-management-syst-3c9f8.firebaseio.com",
  projectId: "disaster-management-syst-3c9f8",
  storageBucket: "disaster-management-syst-3c9f8.appspot.com",
  messagingSenderId: "541065908693",
  appId: "1:541065908693:web:069e2b00ae1ab4916ead5c",
  measurementId: "G-ZLNM9QT6N3"
};

const app = firebase.initializeApp(firebaseConfig);

export const firebasedb = app.database();

const storage = firebase.storage();

export { storage, firebase as default };
