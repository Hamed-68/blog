function error(err,type) {
    const error = {}
    // username
    if (!err.username) {
        error.username = 'Please fill out this field !'
    } else if (!/[a-z0-9]/.test(err.username)) {
        error.username = 'Username should have a-z & 0-9 !'
    } else if (err.username.length < 6) {
        error.username = 'Username must more than 5 character.'
    } else {
        delete error.username
    }

    // password 
    if (!err.password) {
        error.password = 'Password is nessessary.'
    } else if (err.password.length < 6) {
        error.password = 'Password must more than 5 character.'
    } else {
        delete error.password
    }
    // confirm password
    if (type === 'signin') {

        if(!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(err.email)) {
            error.email = 'Email is Invalid'
        } else {
            delete error.email
        }


        if (!err.confirm_password) {
            error.confirm_password = 'Enter Password again.'
        } else if (err.confirm_password !== err.password) {
            error.confirm_password = 'Not matched !'
        } else {
            delete error.confirm_password
        }
    }

    return error
}
export default error