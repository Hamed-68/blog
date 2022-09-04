// import axios from 'axios';
import React, { useEffect, useLayoutEffect } from 'react';
import { useHistory } from 'react-router-dom';

const Main = () => {

    // useEffect(() => {
    //     const token = async () => {
    //         await axios.get('http://127.0.0.1:8000/').then(res => console.log(res)).catch(err => console.log(err))
    //     }
    //     token()
    // }, [])

    const token = localStorage.getItem('token')
    const history = useHistory()
    useLayoutEffect(() => {
        if (!token) history.push('/login')
    }, [token, history])

    const handleLogout = () => {
        localStorage.removeItem('token')
        history.push('/login')
    }
    return (
        <>
            <h2>Dashbord</h2>
            <button onClick={handleLogout}>Log out</button>
        </>

    );
};

export default Main;