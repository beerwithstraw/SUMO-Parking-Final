
import React, { useLayoutEffect, useState, useEffect } from 'react'
import { ScrollView, SafeAreaView, StyleSheet, Text, View, TouchableOpacity } from 'react-native'
import { Avatar, Image, Button} from 'react-native-elements'
import { AntDesign, SimpleLineIcons } from '@expo/vector-icons'
import { auth, database, db } from '../firebase'
import CustomListItem from '../components/CustomListItem'
import { KeyboardAvoidingView } from 'react-native';
import { StatusBar } from 'react-native'
import { ToastAndroid } from 'react-native'


const HomeScreen = ({ navigation }) => {

    const signOutUser = () => {
        auth.signOut().then(() => {
            navigation.replace('Login')
        })
    }

    useLayoutEffect(() => {
        navigation.setOptions({
            title: "Welcome to Smart Park!",
            headerStyle: { backgroundColor: "#fff" },
            headerTitleStyle: { color: "black"},
            headerTintColor: "black",
            headerLeft: () => (
                <View style={{marginLeft: 15, backgroundColor: 'gray'}}>
                    <TouchableOpacity onPress={signOutUser} activeOpacity={0.5}>
                        <Avatar rounded source={{ uri: auth?.currentUser?.photoURL}}/>
                    </TouchableOpacity>
                </View>
            )
        })
    }, [navigation])

    database.ref("Users/Vinny/carstatus").get().then(function(snapshot) {
        if (snapshot.exists()) {
            console.log(snapshot.val());
        }
        else {
          console.log("No data available");
        }
      }).catch(function(error) {
        console.error(error);
      });

      const bookSlot = () => {
        database.ref('Users/Vinny' ).update({
            carstatus: 'booked',
      })
        navigation.navigate('Directions')
    }
        function stat() {
            database.ref("Users/Vinny").on('value', function(snapshot) {
            var carstatu = snapshot.val().carstatus
            console.log(carstatu)
            return (1)
        });   
        }
      
        let status = stat()
        console.log(status)
       
    return (
        <KeyboardAvoidingView behavior='padding' style={styles.container}>
            <StatusBar style="light" /> 
            <Image 
                source={{
                    uri: "https://i.pinimg.com/originals/cd/9d/a2/cd9da2bdbdcc280b6702239df7837d1e.png",
                }}  
                style={{width: 200, height: 200}}
            />
            <Text>{status}</Text>
            <Button raised containerStyle={styles.button} onPress={bookSlot} title="Book a Slot"/>
            <View style={{height: 100}}/>

        </KeyboardAvoidingView>
    )
}

export default HomeScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'white', 
        alignItems: 'center',
        justifyContent: 'center',
        padding: 10,
    },
    inputContainer: {
        width: 300,
    },
    button: {
        width: 200,
        marginTop: 10,
    },
})
