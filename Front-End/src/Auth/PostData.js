import axios from 'axios';

const postNewUser = async (info) => {
    const { username, password, confirm_password, first_name, last_name, email } = info
    const post = await axios.post('/accounts/users/',
        { username, password, confirm_password, first_name, last_name, email },
        {
            headers:
                { 'Content-Type': 'application/json' }
        }).then(res => res)
        .catch(err => err)

    if (await post) {
        if (post.request.status >= 200 && post.request.status < 300) {
            return { status: true, statusMsg: 'Sign In Successfully.' }
        } else {
            return { status: false, statusMsg: post.response.data.username[0] }
        }
    }
}
const postUser = async (info) => {
    const { username, password } = info
    const post = await axios.post('/api-token-auth/',
        { username, password },
        {
            headers:
                { 'Content-Type': 'application/json' }
        }).then(res => res)
        .catch(err => err)

    if (await post) {
        if (post.request.status >= 200 && post.request.status < 300) {
            return { status: true, token: post.data.token, username }
        } else {
            return { status: false, token: '' }
        }
    }
}

export { postNewUser, postUser };