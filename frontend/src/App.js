import React, {useState} from 'react'
import './App.css'
import TaskView from './Components/TaskView'
import NavBar from './Components/NavBar'
import LoginForm from './Components/LoginForm'

function App() {
  const [user, setUser] = useState({})
  

  const login = (details) => {
    fetch(`http://localhost:5000/users/bymail/${details.email}`)
      .then(res => res.json())
      // check if the user is valid
      .then(u => {
        u['_id'] = u['_id']['$oid']
        setUser(u)
      })
      .catch(function(error) {
        console.error(error)
      });
  }

  const logout = (e) => {
    setUser({});
  }
  
  return (
    <div>
      <NavBar Logout={logout} />
      {(Object.keys(user).length === 0) ?
        <div>
          <h1>Login</h1>
          <LoginForm Login={login}/>
        </div>
        : 
        <div>
          <h1>Tasks</h1>
          <TaskView
            userid={user['_id']}
          />
        </div>}
    </div>
  );
}

export default App