import React, { useState } from 'react'
import './App.css'
import TaskView from './Components/TaskView'
import NavBar from './Components/NavBar'
import LoginForm from './Components/LoginForm'

function App() {
  const [user, setUser] = useState({})

  const signup = (details) => {
    const data = new URLSearchParams();
    data.append('email', details.email);
    data.append('firstName', details.firstName);
    data.append('lastName', details.lastName);

    fetch('http://localhost:5000/users/create', {
      method: 'post',
      body: data
    })
      .then(res => res.json())
      .then(userobj => {
        userobj['_id'] = userobj['_id']['$oid'];
        setUser(userobj);
      }).catch(function (error) {
        console.error(error)
      });
  }

  const login = (details) => {
    fetch(`http://localhost:5000/users/bymail/${details.email}`)
      .then(res => res.json())
      .then(userobj => {
        userobj['_id'] = userobj['_id']['$oid'];
        setUser(userobj);
      })
      .catch(function (error) {
        console.error(error)
      });
  }

  const logout = (e) => {
    setUser({});
  }

  return (
    <div>
      <NavBar Logout={logout} />

      <div className='main'>
        {(Object.keys(user).length === 0) ?
          <div>
            <h1>Login</h1>
            <LoginForm Login={login} Signup={signup} />
          </div>
          :
          <div>
            <h1>Your tasks, {user.firstName} {user.lastName}</h1>
            <TaskView user={user} />
          </div>}
      </div>
    </div>
  );
}

export default App