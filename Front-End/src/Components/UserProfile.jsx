import axios from 'axios';
import React, { useEffect, useLayoutEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import AddBlog from './AddBlog';
import Blog from './Blog';
import Follow from './Follow';
import userlogo from './images/Ei-user.svg'
import './styles/userprofile.css'


const UserProfile = (props) => {
    const token = localStorage.getItem('token')
    const myUsername = localStorage.getItem('username')
    const history = useHistory()
    const location = useLocation()
    const userName = props.match.params.user

    const [user, setUser] = useState('')
    const [blogs, setBlogs] = useState([])
    const [refresh, setRefresh] = useState(false)
    const [me, setMe] = useState(false)
    const [isAdd, setIsAdd] = useState(false)
    const [showFollowers, setShowFollowers] = useState(false)
    const [showFollowing, setShowFollowing] = useState(false)
    const isFollow = user && user.followers.find(u => u.username == myUsername)


    useLayoutEffect(() => {
        if (!token) history.push('/login')
    }, [token, history])

    useEffect(() => {
        const get = async () => {
            await axios.get('/accounts/users')
                .then(res => handleFindUser(res.data.results))

            await axios.get('/posts/post/', { headers: { 'Authorization': `Token ${token}` } })
                .then(res => handleFindPost(res.data.results))
        }

        get()



        if (myUsername == userName) {
            setMe(true)
        } else {
            setMe(false)
        }
    }, [refresh, location,history])

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

    const handleFindUser = (users) => {
        const userN = users.find(u => u.username.includes(userName))
        if (userN) setUser(userN)
        else history.push('/usernotfound')

    }

    const handleFindPost = (posts) => {
        const blog = posts.filter(p => p.author == userName)
        setBlogs(blog)
    }

    const Blogs = blogs && blogs.map(i => {
        return (
            <Blog
                key={i.id}
                author={i.author}
                username={user.username}
                img={i.picture}
                title={i.title}
                desc={i.body}
                date={i.created} />
        )
    })

    const handleFollow = async () => {
        if (isFollow) {

            await axios.delete(`/accounts/following/${isFollow.id}`)
            .then(()=>setRefresh(!refresh))

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
        <>
            {user &&
                <div className='container mt-5'>
                    {isAdd && <AddBlog handleCloseModal={() => setIsAdd(false)} handleData={handleData} />}
                    {showFollowers && <Follow type={'Followers'} users={user.followers} handleClose={() => setShowFollowers(false)} />}
                    {showFollowing && <Follow type={'Following'} users={user.following} handleClose={() => setShowFollowing(false)} />}
                    <div className="row justify-content-between">
                        <div className="col-4">
                            <div className="prVk">
                                <header className="gCte d-flex my-3">
                                    <div className="nmU">
                                        <img src={userlogo} alt="" />
                                    </div>
                                    <h3>{user && user.username}</h3>
                                </header>
                                <div className="mUyf d-flex">
                                    <a onClick={() => setShowFollowers(true)} className="mgVj">
                                        <span>{user && user.followers.length}</span>
                                        <p>followers</p>
                                    </a>
                                    <a onClick={() => setShowFollowing(true)} className="mgVj">
                                        <span>{user && user.following.length}</span>
                                        <p>following</p>
                                    </a>
                                </div>
                                <div className="gBqr">
                                    <ul>
                                        <li><span>FirstName:</span> {user && user.first_name}</li>
                                        <li><span>LastName:</span> {user && user.last_name}</li>
                                        <li><span>Email:</span> {user && user.email}</li>
                                    </ul>
                                </div>
                                <div className="bOOb">
                                    {
                                        me ?
                                            <>
                                                <button>Edit Profile</button>
                                                <button onClick={() => setIsAdd(true)}>Add Blog</button>
                                            </>
                                            :
                                            <>
                                                <button onClick={() => handleFollow()}>{isFollow ? 'unFollow' : 'follow'}</button>
                                                <button>message</button>
                                            </>
                                    }
                                </div>
                            </div>
                        </div>
                        <div className="col-8">
                            {Blogs}
                        </div>
                    </div>
                </div>}
        </>
    );
};

export default UserProfile;