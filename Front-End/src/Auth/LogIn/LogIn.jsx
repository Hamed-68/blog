import React, { useState } from 'react';
import openEye from '../images/openEye.svg'
import closeEye from '../images/closeEye.svg'
import styles from './LogIn.module.css'
import { postUser } from '../PostData';
import { ToastContainer } from 'react-toastify';
import notify from '../toast'
import error from '../error'
import { Link, useHistory } from 'react-router-dom';

const LogIn = () => {
    const history = useHistory()
    const [showHidePass, setShowHidePass] = useState(false)
    const [userInfo, setUserInfo] = useState({ username: '', password: '' })
    const [touch, setTouch] = useState({})
    const errors = error(userInfo, 'login');
    const handleShowHide = () => {
        setShowHidePass(prev => !prev)
    }
    const handleChange = event => {
        setUserInfo(prev => {
            return {
                ...prev,
                [event.target.name]: event.target.value.trim()
            }
        })
    }
    const handleSubmit = async event => {
        event.preventDefault();
        if (Object.keys(errors).length) {
            setTouch({ username: true, password: true })
            return
        } else {
            const response = await postUser(userInfo)
            if (response.status) {
                localStorage.setItem('token',response.token)
                notify('success','Log In Successfully.')
                history.push('/dashbord')
            } else {
                notify('error','username or password is wrong.')
            }
        }
    }
    const handleTouch = event => {
        setTouch(prev => {
            return {
                ...prev,
                [event.target.name]: true
            }
        })
    }

    return (
        <div className={styles.main}>
            <div className={styles.formSignIn}>
                <h4>Log In</h4>
                <form className={styles.form} method='POST' onSubmit={handleSubmit}>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type="text"
                            name="username" id='username' onChange={handleChange} value={userInfo.username} onFocus={handleTouch} />
                        <label htmlFor="username">User Name :</label>
                        {touch.username && errors.username && <span className={styles.error}>{errors.username}</span>}
                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type={showHidePass ? 'type' : 'password'}
                            name='password' id='password' onChange={handleChange} value={userInfo.password} onFocus={handleTouch} />
                        <label htmlFor="password">Password :</label>
                        <img onClick={handleShowHide} className={styles.imgPass} src={showHidePass ? openEye : closeEye} alt="show-hide" />
                        {touch.password && errors.password && <span className={styles.error}>{errors.password}</span>}

                    </div>
                    <button className={styles.btn} type="submit">Log In</button>

                    <Link to='/signin' className={styles.logIn}>You Don't Have Account ?</Link>
                </form>
            </div>
            <ToastContainer />
        </div>
    );
};

export default LogIn;