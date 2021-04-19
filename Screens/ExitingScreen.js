import React, { useLayoutEffect } from 'react'
import { StatusBar } from 'react-native'
import { StyleSheet, Text, View } from 'react-native'
import { KeyboardAvoidingView } from 'react-native';
import { Button } from 'react-native-elements'



const ExitingScreen = ({ navigation }) => {
    const switchDir = () => {
        navigation.navigate('Exiting2')
    }

    useLayoutEffect(() => {
        navigation.setOptions({
            title: "Exiting Directions",
            headerStyle: { backgroundColor: "#fff" },
            headerTitleStyle: { color: "black"},
            headerTintColor: "black",
        })
    }, [navigation])
    
    return (
        <KeyboardAvoidingView behavior='padding' style={styles.container}>
            <StatusBar style="light" /> 
            <Text><h2>EXIT</h2></Text>

            <Text><h3>Turn RIGHT, move straight ahead and take a U-Turn.</h3></Text>
            <Button containerStyle={styles.button} onPress={switchDir} type="outlined" title=" "/>

        </KeyboardAvoidingView>
    )
}

export default ExitingScreen

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
        padding: 50,
        width: 200,
        height: 100,
        marginTop: 200,
    },
})
