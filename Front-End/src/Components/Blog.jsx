import React from 'react';
import './styles/blog.css';
import userlogo from './images/Ei-user.svg'


const Blog = ({ author, img, title, desc, date }) => {
    return (
        <div className='blog'>
            <div className='blogAuthor'>
                <div className='authorImg'>
                    <img src={userlogo} alt='author' width='60px' />
                </div>
                <p>{author}</p>
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