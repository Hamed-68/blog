import React from 'react';
import { useState } from 'react';
import './styles/addBlog.css'

const AddBlog = ({ handleCloseModal, handleData }) => {
    const [addPost, setAddPost] = useState({ title: '', body: '', picture: null, status: 'PU' })
    const handleChange = event => {
        setAddPost(prev => {
            return {
                ...prev,
                [event.target.name]: event.target.value
            }
        })
    }
    const handleUpload = event => {
        setAddPost(prev => {
            return {
                ...prev,
                picture: event.target.files[0]
            }
        })
    }
    const handleSendData = (e) => {
        e.preventDefault();
        if (!addPost.title) {
            alert('title can not be empty')
            return;
        }
        if (!addPost.body) {
            alert('body can not be empty')
            return;
        }
        handleData(addPost)
        handleCloseModal()
    }
    return (
        <div className='wXFr'>
            <div className="tab-pane" id="post-object-form">
                <form method='POST' encType='multipart/form-data' className="form-horizontal">

                    <fieldset>

                        <div className="form-group ">
                            <label className="control-label">Title</label>
                            <input name="title" className="form-control" type="text" value={addPost.title} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label className="control-label ">Body</label>
                            <textarea name="body" value={addPost.body} onChange={handleChange} className="form-control"></textarea>
                        </div>
                        <div className="form-group">
                            <label className="control-label">Picture</label>
                            <br />
                            <input name="picture" type="file" onChange={handleUpload} accept='image/jpeg, image/jpg, image/png, image/gif'/>
                        </div>
                        <div className="form-group">
                            <label className="control-label ">Status</label>
                            <select className="form-control" name="status" value={addPost.status} onChange={handleChange}>
                                <option value="PU">Publish</option>
                                {/* <option value="DR">Draft</option> */}
                                {/* <option value="AR">Archive</option> */}
                            </select>
                        </div>
                        <div className="form-actions">
                            <button type='submit' className="js-tooltip" onClick={handleSendData}>POST</button>
                            <button className='closeModal' onClick={handleCloseModal}>CANCLE</button>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>
    );
};

export default AddBlog;