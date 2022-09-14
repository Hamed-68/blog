import React from 'react';
import styles from './NotFound.module.css'

const NotFound = () => {
    return (
        <div className={styles.notFound}>
            <h1 className={styles.text}>sorry this page dosen't exist.</h1>
        </div>
    );
};

export default NotFound;