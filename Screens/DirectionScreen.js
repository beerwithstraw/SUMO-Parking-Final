import React, { useLayoutEffect } from 'react'
import { StatusBar } from 'react-native'
import { StyleSheet, Text, View } from 'react-native'
import { KeyboardAvoidingView } from 'react-native';
import { Button } from 'react-native-elements'



const DirectionScreen = ({ navigation }) => {
    const switchDir = () => {
        navigation.navigate('Directions2')
    }

    useLayoutEffect(() => {
        navigation.setOptions({
            title: "Parking Directions",
            headerStyle: { backgroundColor: "#fff" },
            headerTitleStyle: { color: "black"},
            headerTintColor: "black",
        })
    }, [navigation])
    
    return (
        <KeyboardAvoidingView behavior='padding' style={styles.container}>
            <StatusBar style="light" /> 
            <Text><h2>Parking Lot: 4</h2></Text>

            <Text><h3>Move straight ahead.</h3></Text>
            <Button containerStyle={styles.button} onPress={switchDir} type="outlined" title=" "/>

        </KeyboardAvoidingView>
    )
}

export default DirectionScreen

const styles = StyleSheet.create({
    container: {
        backgroundColor: 'red',
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
