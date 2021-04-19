import React from 'react';
import 'react-native-gesture-handler';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import LoginScreen from './Screens/LoginScreen'
import RegisterScreen from './Screens/RegisterScreen';
import HomeScreen from './Screens/HomeScreen'
import DirectionScreen from './Screens/DirectionScreen';
import DirectionScreen2 from './Screens/DirectionScreen2';
import DirectionScreen3 from './Screens/DirectionScreen3';

import ParkedScreen from './Screens/ParkedScreen';

import ExitingScreen from './Screens/ExitingScreen';
import ExitingScreen2 from './Screens/ExitingScreen2';
import ExitingScreen3 from './Screens/ExitingScreen3';
import ExitingScreen4 from './Screens/ExitingScreen4';

import ExitedScreen from './Screens/ExitedScreen';


import { database } from './firebase'

const Stack = createStackNavigator(); 
const globalScreenOptions = {
  headerStyle: {backgroundColor: "#2C6BED"},
  headerTitleScreen: {color: "white"},
  headerTintColor: "white"
}
function getStatus() {
  database.ref("Users/username1").on('value', function(snapshot) {
    carstatus = snapshot.val().carstatus
    return carstatus
  });
}


export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={globalScreenOptions} >

        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name='Register' component={RegisterScreen} />

        <Stack.Screen name='Home' component={HomeScreen} />

        <Stack.Screen name='Directions' component={DirectionScreen} />
        <Stack.Screen name='Directions2' component={DirectionScreen2} />
        <Stack.Screen name='Directions3' component={DirectionScreen3} />

        <Stack.Screen name='Parked' component={ParkedScreen} />

        <Stack.Screen name='Exiting' component={ExitingScreen} />
        <Stack.Screen name='Exiting2' component={ExitingScreen2} />
        <Stack.Screen name='Exiting3' component={ExitingScreen3} />
        <Stack.Screen name='Exiting4' component={ExitingScreen4} />
        
        <Stack.Screen name='Exited' component={ExitedScreen} />



      </Stack.Navigator>
    </NavigationContainer>

  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
