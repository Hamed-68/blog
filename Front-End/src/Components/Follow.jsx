import React from 'react';
import { Link } from 'react-router-dom';
import './styles/follow.css'

const Follow = ({ type, users, handleClose }) => {
    const list = users && users.map(i => {
        return (
            <li key={i.id}><Link to={`/users/${i.username}`} onClick={handleClose}>{i.username}</Link></li>
        )
    })
    return (
        <div className='wXFr'>
            <div className="lGop">
                <header className="Bfou d-flex">
                    <p>{type}</p>
                    <button onClick={handleClose}>X</button>
                </header>
                <ul>
                    {list}
                </ul>
            </div>
        </div>
    );
};

export default Follow;