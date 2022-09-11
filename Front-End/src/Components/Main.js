import axios from 'axios';
import React, { useEffect, useLayoutEffect, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import './styles/main.css'
import userlogo from './images/Ei-user.svg'
import Blog from './Blog';
import AddBlog from './AddBlog';

const Main = () => {
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')
    const history = useHistory()

    const [user, setUser] = useState({})
    const [posts, setPosts] = useState([])
    const [isAdd, setIsAdd] = useState(false)
    const [refresh, setRefresh] = useState(false)

    useLayoutEffect(() => {
        if (!token) history.push('/login')
    }, [token, history])

    useEffect(() => {
        const get = async () => {
            await axios.get('/posts/post/', { headers: { 'Authorization': `Token ${token}` } })
                .then(res => setPosts(res.data.results))

            await axios.get('/accounts/users/')
                .then((res) => handleUser(res))
        }
        get()
    }, [refresh,token])
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
    const handleData = async (data) => {
        await axios.post('/posts/post/', {
            "title": data.title,
            "body": data.body,
            "picture": data.picture,
            "status": data.status
        },
            {
                headers:
                {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Token ${token}`
                }
            })
            .then(() => setRefresh(!refresh))
    }
    return (
        <>
            <div className='main'>
                <div className='container'>
                    {isAdd && <AddBlog handleCloseModal={() => setIsAdd(false)} handleData={handleData} />}
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
                            <button className='addBlog' onClick={() => setIsAdd(true)}>Add Blog</button>
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