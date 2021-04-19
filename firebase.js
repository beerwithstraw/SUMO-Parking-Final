import { firebase } from '@firebase/app'

import "firebase/firestore"
import "firebase/auth"
import "firebase/database"
const firebaseConfig = {
    apiKey: "AIzaSyDYQXZjbRQ9wLOaqXH-MMgef4mnATIsS_8",
    authDomain: "parking-sumo.firebaseapp.com",
    databaseURL: "https://parking-sumo-default-rtdb.firebaseio.com",
    projectId: "parking-sumo",
    storageBucket: "parking-sumo.appspot.com",
    messagingSenderId: "1013612292554",
    appId: "1:1013612292554:web:795bfcf04a9744b4828733",
    measurementId: "G-XFP4JR8QTY"
  };

  const app = firebase.initializeApp(firebaseConfig)
 
  const db = app.firestore();
  const auth = firebase.auth();
  const database = app.database();

  export { db, auth, database }
