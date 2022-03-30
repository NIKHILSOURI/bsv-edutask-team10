import React, {useState, useEffect} from 'react'
import './App.css'
import TaskView from './Components/TaskView'
import NavBar from './Components/NavBar'

function App() {
  // create a react state for the list of tasks to display
  const [email, setEmail] = useState('')

  const [user, setUser] = useState({
    "_id": "624442cfa6ba7231cec8f2c2"
  })
  

  const login = (event) => {
    event.preventDefault();
    console.log(email)
    fetch(`http://localhost:5000/users/bymail/${email}`)
      .then(res => res.json())
      .then(u => {
        u['_id'] = u['_id']['$oid']
        setUser(u)
      })
      .catch(function(error) {
        console.error(error)
      });
  }
  
  return (
    <div>
      <NavBar />

      {(user == null) ?
        <div>
          <form onSubmit={login}>
            <div className='inputwrapper'>
              <label>Email </label>
              <input type='text' id='title' name='title' onChange={event => setEmail(event.target.value)}></input>
            </div>

            <button>Login</button>
          </form>
        </div>
        : <div>
          <h1>Tasks</h1>

          <TaskView
            userid={user['_id']}
          />
        </div>}
    </div>
  );
}

export default App