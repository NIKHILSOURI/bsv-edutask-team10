import React, {useState} from 'react'
import './../Styles/Form.css'

function LoginForm({ Login }) {
    const [credentials, setCredentials] = useState({email: ''});

    const submitHandler = e => {
        e.preventDefault();

        Login(credentials);
    }

    return (
        <form className="submit-form" onSubmit={submitHandler}>
            <div className='inputwrapper'>
                <label>Email Address</label>
                <input type='text' id='email' name='email' onChange={e => setCredentials({...credentials, email: e.target.value})} value={credentials.email}></input>
            </div>
            <div className='inputwrapper'>
                <label>Password</label>
                <input type='text' id='password' name='password' disabled></input>
            </div>

            <input type="submit" value="Login" disabled={credentials.email.length === 0}></input>
        </form>
    );
}

export default LoginForm