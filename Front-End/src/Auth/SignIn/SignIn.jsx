import React, { useState } from 'react';
import { postNewUser } from '../PostData';
import styles from './SignIn.module.css'
import openEye from '../images/openEye.svg'
import closeEye from '../images/closeEye.svg'
import error from '../error';
import { Link, useHistory } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import notify from '../toast'

const SignIn = () => {
    const history = useHistory();
    const [showHidePass, setShowHidePass] = useState(false)
    const [showHideCpass, setShowHideCpass] = useState(false)
    const [userInfo, setUserInfo] = useState({ username: '', first_name: '', last_name: '', email: '', password: '', confirm_password: '' })
    const [touch, setTouch] = useState({})
    const errors = error(userInfo, 'signin')

    const handleShowHide = event => {
        if (event.target.alt === 'show-hide') {
            setShowHidePass(prev => !prev)
        } else {
            setShowHideCpass(prev => !prev)
        }
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
            setTouch({ username: true, password: true, confirm_password: true, email: true })
            return
        } else {
            const { status, statusMsg } = await postNewUser(userInfo)
            status ? notify('success', statusMsg) : notify('error', statusMsg)
            status && history.push('/login')
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
                <h4>Sign In</h4>
                <form className={styles.form} onSubmit={handleSubmit}>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type="text"
                            name="username" id='username' onChange={handleChange} value={userInfo.username} onFocus={handleTouch} />
                        <label htmlFor="username">* User Name :</label>
                        {touch.username && errors.username && <span className={styles.error}>{errors.username}</span>}
                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type="text"
                            name='first_name' id='firstname' onChange={handleChange} value={userInfo.first_name} />
                        <label htmlFor="firstname">First Name :</label>
                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type="text"
                            name='last_name' id='lastname' onChange={handleChange} value={userInfo.last_name} />
                        <label htmlFor="lastname">Last Name :</label>
                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type="email"
                            name='email' id='email' onChange={handleChange} value={userInfo.email} onFocus={handleTouch} />
                        <label htmlFor="email">Email :</label>
                        {touch.email && errors.email && <span className={styles.error}>{errors.email}</span>}

                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type={showHidePass ? 'type' : 'password'}
                            name='password' id='password' onChange={handleChange} value={userInfo.password} onFocus={handleTouch} />
                        <label htmlFor="password">* Password :</label>
                        <img onClick={handleShowHide} className={styles.imgPass} src={showHidePass ? openEye : closeEye} alt="show-hide" />
                        {touch.password && errors.password && <span className={styles.error}>{errors.password}</span>}

                    </div>
                    <div className={styles.formInput}>
                        <input
                            className={styles.input}
                            type={showHideCpass ? 'type' : 'password'}
                            name='confirm_password' id='confirm_password' onChange={handleChange} value={userInfo.confirm_password} onFocus={handleTouch} />
                        <label htmlFor="confirm_password">* Confirm Password :</label>
                        <img onClick={handleShowHide} className={styles.imgPass} src={showHideCpass ? openEye : closeEye} alt="Cshow-hide" />
                        {touch.confirm_password && errors.confirm_password && <span className={styles.error}>{errors.confirm_password}</span>}
                    </div>
                    <button className={styles.btn} type="submit">Sign In</button>

                    <Link to='/login' className={styles.signIn}>Already Have Account ?</Link>
                </form>
            </div>
            <ToastContainer />
        </div>
    );
};

export default SignIn;