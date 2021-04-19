import React, { useState, useEffect } from 'react'
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native'
import { Button, Input, Image } from 'react-native-elements';
import { KeyboardAvoidingView } from 'react-native';
import { auth, database } from '../firebase';

const LoginScreen = ({ navigation }) => {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    useEffect(() => {

        database.ref("Users/username1").on('value', function(snapshot) {
            var status = snapshot.val().carstatus
            console.log(status)
        })
        const unsubscribe = auth.onAuthStateChanged((authUser) => {
            if (authUser) {
                if (status == 'idle') {
                    navigation.replace("Home");
                }
                else if (status == 'to_parking') {
                    navigation.replace("Directions2")
                }
                else if (status == 'parked') {
                    navigation.replace('Parked')
                }
                else if (status == 'to_exiting') {
                    navigation.replace('Exiting2')
                }
                else {
                    navigation.replace('Home')
                }
            }
        })

        return unsubscribe;
    }, [])

    const SignIn = () => {  
        auth.signInWithEmailAndPassword(email, password)
            .catch(error => alert(error.message))
    }


    return (
        <KeyboardAvoidingView behavior='padding' style={styles.container}>
            <StatusBar style="light" /> 
            <Image 
                source={{
                    uri: "https://i.pinimg.com/originals/cd/9d/a2/cd9da2bdbdcc280b6702239df7837d1e.png",
                }}  
                style={{width: 200, height: 200}}
            />
            <View style={styles.inputContainer}>
                <Input 
                    placeholder="Email Address" 
                    autoFocus 
                    type="email" 
                    value={email} 
                    onChangeText={text => setEmail(text)}
                />
                <Input 
                    placeholder="Password" 
                    secureTextEntry 
                    type="password"
                    value={password} 
                    onChangeText={text => setPassword(text)}
                    onSubmitEditing={SignIn}
                />
            </View>
             
            <Button raised containerStyle={styles.button} onPress={SignIn} title="Login"/>
            <Button raised onPress={() => navigation.navigate("Register")} containerStyle={styles.button} type="outline" title="Register"/>

            <View style={{height: 100}}/>
        </KeyboardAvoidingView>
    )
}

export default LoginScreen

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
