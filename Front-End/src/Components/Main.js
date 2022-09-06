import axios from 'axios';
import React, { useEffect, useLayoutEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import './styles/main.css'
import userlogo from './images/Ei-user.svg'
import Blog from './Blog';

const Main = () => {
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')
    const history = useHistory()

    const [user, setUser] = useState({})
    const [posts, setPosts] = useState([])

    useLayoutEffect(() => {
        if (!token) history.push('/login')
    }, [token, history])

    useEffect(() => {
        const get = async () => {
            await axios.get('http://127.0.0.1:8000/posts/post/', { headers: { 'Authorization': `Token ${token}` } })
                .then(res => setPosts(res.data.results))

            await axios.get('http://127.0.0.1:8000/accounts/users/')
                .then((res) => handleUser(res))
        }
        get()
    }, [])
    const handleUser = (res) => {
        const user = res.data.results.find(u => u.username.includes(username))
        setUser(user)
    }

    const Blogs = posts ? posts.map(i => {
        return (
            <Blog
                key={i.id}
                author={i.author}
                img={i.picture}
                title={i.title}
                desc={i.body} 
                date={i.created} />
        )
    }) : <h3> thire is no Blogs.</h3>

    const handleLogout = () => {
        localStorage.removeItem('token')
        history.push('/login')
    }
    return (
        <>
            <div className='main'>
                <div className='container'>
                    <header className='header'>
                        <div className='user d-flex align-items-center'>
                            <div className='userImg'>
                                <img src={userlogo} alt='user' width='100px' />
                            </div>
                            <div className='userInfo'>
                                <h4>{user.username}</h4>
                                <h6>{user.email}</h6>
                                <span onClick={handleLogout}>Log out</span>
                            </div>
                        </div>
                        <h1 className='title'>Blogs</h1>
                        <div className='manageBlog'>
                            <button className='myBlog'>My Blog</button>
                            <button className='addBlog'>Add Blog</button>
                        </div>
                    </header>
                    <main className='blogs d-flex flex-column'>
                        {Blogs}
                    </main>
                </div>
            </div>
        </>

    );
};

export default Main;