//Gourav(member-5) firebase configuration file


import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, signOut, onAuthStateChanged, updateProfile } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore, collection, addDoc, doc, setDoc, getDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

//Firebase configuration
const firebaseConfig = {
  apiKey: "API_KEY",
  authDomain: "binbot-0.firebaseapp.com",
  projectId: "binbot-0",
  storageBucket: "binbot-0.firebasestorage.app",
  messagingSenderId: "483195794662",
  appId: "1:483195794662:web:4462980eee948e11127727",
  measurementId: "G-KRL23C0EV8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const db = getFirestore(app);

export { 
    auth, 
    googleProvider, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signInWithPopup, 
    signOut, 
    onAuthStateChanged,
    updateProfile,
    db,
    collection,
    addDoc,
    doc,
    setDoc,
    getDoc,
    serverTimestamp
};
