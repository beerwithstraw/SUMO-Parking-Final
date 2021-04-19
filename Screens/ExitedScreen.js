import React, { useLayoutEffect } from 'react'
import { StatusBar } from 'expo-status-bar'
import { KeyboardAvoidingView } from 'react-native'
import { StyleSheet, Text, View } from 'react-native'
import { Button } from 'react-native'
import { database } from '../firebase'

const ParkedScreen = ({ navigation }) => {

    const exitedParking = () => {
      navigation.navigate('Home')
    }

    useLayoutEffect(() => {
        navigation.setOptions({
            title: "Parked Screen",
            headerStyle: { backgroundColor: "#fff" },
            headerTitleStyle: { color: "black"},
            headerTintColor: "black",
        })
    }, [navigation])

    return (

        <KeyboardAvoidingView behavior='padding' style={styles.container}>
            <StatusBar style="light" /> 
            <Text><h3>Thank you for parking with us!</h3></Text>
            <Text><h3>Have a safe journey.</h3></Text>
            <View style={{height: 20}}/>
            <Button raised containerStyle={styles.button} onPress={exitedParking} title="Go to Home"/>
            <View style={{height: 100}}/>

        </KeyboardAvoidingView>
    )
}

export default ParkedScreen

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
