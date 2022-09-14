import React, { useState } from 'react';
import './styles/blog.css';
import userlogo from './images/Ei-user.svg'
import { useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';


const Blog = ({ author, username, img, title, desc, date }) => {
    const [isMe, setIsMe] = useState(true)
    const token = localStorage.getItem('token')
    const [user, setUser] = useState()
    const [refresh, setRefresh] = useState(false)

    const isFollow = user && user.followers.find(u => u.username == username)


    useEffect(() => {
        if (username == author) {
            setIsMe(false)
        }
        const get = async () => {
            await axios.get('/accounts/users')
                .then(res => handleFindUser(res.data.results))
        }
        get()
    }, [refresh])
    const handleFindUser = (users) => {
        const authorUser = users.find(u => u.username == author)
        setUser(authorUser)
    }

    const handleFollow = async () => {
        if (isFollow) {

            await axios.delete(`/accounts/following/${isFollow.id}`)
                .then(() => setRefresh(!refresh))

        } else {
            await axios.post('/accounts/following/',
                { "following_user_id": user.id },
                {
                    headers:
                    {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`
                    }
                })
                .then(() => setRefresh(!refresh))
        }
    }
    return (
        <div className='blog'>
            <div className='blogAuthor'>
                <div className='authorImg'>
                    <img src={userlogo} alt='author' width='60px' />
                </div>
                <Link to={`/users/${author}`}>{author}</Link>
                {isMe && <button className='Hbci' onClick={handleFollow}>{isFollow ? 'unFollow' : 'follow'}</button>}
            </div>
            <div className='blogInfo'>
                <div className='blogImg'>
                    {img && <img src={img} alt='blog' />}
                </div>
                <div className='aboutBlog'>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                    <span>{date}</span>
                </div>
            </div>
        </div>
    );
};

export default Blog;