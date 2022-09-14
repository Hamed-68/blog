import React from 'react';
import './styles/blog.css';
import userlogo from './images/Ei-user.svg'
import { Link } from 'react-router-dom';

const Blog = ({ author, img, title, desc, date }) => {

    return (
        <div className='blog'>
            <div className='blogAuthor'>
                <div className='authorImg'>
                    <img src={userlogo} alt='author' width='60px' />
                </div>
                <Link to={`/users/${author}`}>{author}</Link>
            </div>
            <div className='blogInfo'>
                <div className='blogImg'>
                    {img && <img src={img} alt='blog' />}
                </div>
                <div className='aboutBlog' dir='auto'>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                    <span>{date}</span>
                </div>
            </div>
        </div>
    );
};

export default Blog;